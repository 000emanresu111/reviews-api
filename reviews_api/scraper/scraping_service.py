from typing import List
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from reviews_api.models.schemas import (
    RestaurantInfo,
    RestaurantReview,
    ReviewInfo,
    ReviewSentiment,
)
from shutil import which
from time import sleep

WEBDRIVER_PATH = which("chromedriver")


def get_normalized_rating(percentage: float) -> float:
    return round((percentage / 100) * 5, 1)


def get_text_element(review, selector):
    try:
        element = review.find_element(By.CSS_SELECTOR, selector)
        return element.text
    except NoSuchElementException:
        return None


def scrape_review_elements(review_elements):
    reviews = []
    for review in review_elements:
        rating_percentage_element = review.find_element(
            By.CSS_SELECTOR, ".RatingMultiStarVariant_c-rating-mask_1c0Q3"
        )
        rating_percentage_style = rating_percentage_element.get_attribute("style")
        percentage = float(
            rating_percentage_style.split(":")[-1].strip().replace("%;", "")
        )
        normalized_rating = get_normalized_rating(percentage)

        review_text = get_text_element(review, '[data-test-id="review-text"]')
        reviewer = get_text_element(review, '[data-test-id="review-author"]')
        review_date = get_text_element(review, '[data-test-id="review-date"]')

        review_info = ReviewInfo(
            review_date=review_date,
            review_reviewer=reviewer,
            review_text=review_text,
            review_sentiment=ReviewSentiment.NONE,
            review_rating=normalized_rating,
        )

        reviews.append(review_info)

    return reviews


def scrape_justeat_reviews(restaurant_name: str) -> List[RestaurantReview]:
    service = Service(WEBDRIVER_PATH)

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")

    driver = webdriver.Chrome(service=service, options=chrome_options)

    url = f"https://www.justeat.it/restaurants-{restaurant_name}/reviews"
    print("Scraping URL:", url)
    print("\n")

    driver.get(url)
    sleep(2)

    restaurant_normalized_rating: float = 1.0
    try:
        restaurant_rating_elements = driver.find_elements(
            By.CLASS_NAME, "c-overall-ratingStarsHeader"
        )
        for element in restaurant_rating_elements:
            restaurant_rating_percentage_element = element.find_element(
                By.CSS_SELECTOR, ".RatingMultiStarVariant_c-rating-mask_1c0Q3"
            )
            restaurant_rating_percentage_style = (
                restaurant_rating_percentage_element.get_attribute("style")
            )
            percentage = float(
                restaurant_rating_percentage_style.split(":")[-1]
                .strip()
                .replace("%;", "")
            )
            restaurant_normalized_rating = get_normalized_rating(percentage)
    except:
        restaurant_normalized_rating = None

    restaurant_info = RestaurantInfo(
        restaurant_name=url.split("/")[-2],
        restaurant_rating=restaurant_normalized_rating,
    )

    review_elements = driver.find_elements(
        By.CSS_SELECTOR, '[data-test-id="review-container"]'
    )
    print("Found", len(review_elements), "review elements")
    print("\n")

    reviews = scrape_review_elements(review_elements)

    driver.quit()

    restaurant_reviews = [
        RestaurantReview(restaurant=restaurant_info, review=review)
        for review in reviews
    ]
    return restaurant_reviews
