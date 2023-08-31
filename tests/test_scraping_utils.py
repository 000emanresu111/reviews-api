from app.scraper.scraping_utils import scrape_review_element
from app.scraper.scraping_utils import get_normalized_rating


def test_get_normalized_rating():
    percentage = 80.0
    expected_result = 4.0

    result = get_normalized_rating(percentage)

    assert result == expected_result


class MockWebElement:
    def __init__(self, text_selector, text):
        self.text_selector = text_selector
        self.text = text

    def find_element(self, by, value):
        return self

    def get_attribute(self, attr):
        if attr == "style":
            return "width: 80%;"
        elif attr == "data-test-id":
            return self.text_selector


def test_scrape_review_element():
    review_element = MockWebElement("review-text", "Great review text")

    result = scrape_review_element(review_element)

    assert len(result.__dict__) == 5
