from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from app.models.schemas import ReviewInfo, ReviewSentiment


def get_normalized_rating(percentage: float) -> float:
    return round((percentage / 100) * 5, 1)


def get_text_element(element, selector) -> str:
    try:
        element = element.find_element(By.CSS_SELECTOR, selector)
        return element.text
    except NoSuchElementException:
        return None


def scrape_review_element(review_element):
    rating_percentage_element = review_element.find_element(
        By.CSS_SELECTOR, ".RatingMultiStarVariant_c-rating-mask_1c0Q3"
    )
    rating_percentage_style = rating_percentage_element.get_attribute("style")
    percentage = float(rating_percentage_style.split(":")[-1].strip().replace("%;", ""))
    normalized_rating = get_normalized_rating(percentage)

    review_text = get_text_element(review_element, '[data-test-id="review-text"]')
    reviewer = get_text_element(review_element, '[data-test-id="review-author"]')
    review_date = get_text_element(review_element, '[data-test-id="review-date"]')

    return ReviewInfo(
        review_date=review_date,
        review_reviewer=reviewer,
        review_text=review_text,
        review_sentiment=ReviewSentiment.NONE,
        review_rating=normalized_rating,
    )
