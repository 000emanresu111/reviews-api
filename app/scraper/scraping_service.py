from shutil import which
from time import sleep
from typing import List

from fastapi import HTTPException
from fastapi.logger import logger as fastapi_logger
from selenium import webdriver
from selenium.common.exceptions import (NoSuchAttributeException,
                                        NoSuchElementException)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from app.models.schemas import RestaurantInfo, RestaurantReview
from app.scraper.scraping_utils import (get_normalized_rating,
                                        scrape_review_element)
from app.utils.exceptions import (RestaurantNotFoundError,
                                  ReviewsNotFoundWarning)

WEBDRIVER_PATH = which("chromedriver")


def click_show_more(driver):
    try:
        show_more_button = driver.find_element(
            By.CSS_SELECTOR, '[data-test-id="review-show-more-button"]'
        )
        show_more_button.click()
        sleep(2)
        click_show_more(driver)
    except NoSuchElementException:
        return


def scrape_justeat_reviews(
    restaurant_name: str, use_click_show_more: bool = True
) -> List[RestaurantReview]:
    service = Service(WEBDRIVER_PATH)

    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=service, options=chrome_options)

    url = f"https://www.justeat.it/restaurants-{restaurant_name}/reviews"
    fastapi_logger.info(f"Scraping URL: {url}")

    driver.get(url)
    sleep(2)

    try:
        restaurant_rating_element = driver.find_element(
            By.CLASS_NAME, "c-overall-ratingStarsHeader"
        )
    except NoSuchElementException:
        error_message = f"Restaurant '{restaurant_name}' not found"
        fastapi_logger.error(error_message)
        raise RestaurantNotFoundError(error_message)

    try:
        restaurant_rating_percentage_element = restaurant_rating_element.find_element(
            By.CSS_SELECTOR, ".RatingMultiStarVariant_c-rating-mask_1c0Q3"
        )
    except NoSuchElementException:
        error_message = f"There are still no reviews for this restaurant"
        fastapi_logger.error(error_message)
        raise ReviewsNotFoundWarning(error_message)

    try:
        restaurant_rating_percentage_style = restaurant_rating_percentage_element.get_attribute("style")
    except NoSuchAttributeException as e:
        raise HTTPException(status_code=404, detail=str(e))
        

    percentage = float(
            restaurant_rating_percentage_style.split(":")[-1].strip().replace("%;", "")
        )
    restaurant_normalized_rating = get_normalized_rating(percentage)


    restaurant_info = RestaurantInfo(
        restaurant_name=url.split("/")[-2],
        restaurant_rating=restaurant_normalized_rating,
    )

    try:
        if use_click_show_more:
            click_show_more(driver)

        review_elements = driver.find_elements(
            By.CSS_SELECTOR, '[data-test-id="review-container"]'
        )
        if not review_elements:
            raise ReviewsNotFoundWarning(restaurant_name)

        fastapi_logger.info(f"Found {len(review_elements)} review elements")

        reviews = [
            scrape_review_element(review_element) for review_element in review_elements
        ]

        driver.quit()

        return [
            RestaurantReview(restaurant=restaurant_info, review=review)
            for review in reviews
        ]
    # except Exception as e:
    #     error_message = f"An error occurred during scraping: {str(e)}"
    #     fastapi_logger.error(error_message)
    #     raise HTTPException(status_code=500, detail=error_message)
    except (RestaurantNotFoundError, ReviewsNotFoundWarning) as custom_exception:
        raise HTTPException(status_code=custom_exception.status_code, detail=custom_exception.detail)
