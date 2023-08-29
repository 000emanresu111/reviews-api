from unittest.mock import Mock, patch
from reviews_api.scraper.scraping_service import scrape_justeat_reviews, WEBDRIVER_PATH


from unittest.mock import Mock, patch
from reviews_api.scraper.scraping_service import scrape_justeat_reviews


@patch("reviews_api.scraper.scraping_service.webdriver")
def test_scrape_justeat_reviews(mock_webdriver):
    mock_driver = mock_webdriver.Chrome.return_value
    mock_driver.find_elements.return_value = [mock_driver.find_element.return_value]
    mock_driver.find_element.return_value.get_attribute.return_value = (
        "style: width: 80%;"
    )
    mock_driver.find_elements.return_value[
        0
    ].find_element.return_value.text = "Review Text"
    mock_driver.find_element.return_value.text = "John Doe"

    reviews = scrape_justeat_reviews("test_restaurant", use_click_show_more=False)

    assert len(reviews) == 1
