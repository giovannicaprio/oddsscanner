import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock
from selenium.webdriver.common.by import By
from src.scrapers.yahoo_finance_scraper import YahooFinanceScraper

def test_scraper_initialization(config):
    """Test YahooFinanceScraper initialization"""
    scraper = YahooFinanceScraper(config)
    assert scraper.config == config
    assert scraper.driver is None

@patch('src.scrapers.yahoo_finance_scraper.webdriver')
def test_driver_initialization(mock_webdriver, config):
    """Test Chrome driver initialization"""
    mock_chrome = MagicMock()
    mock_webdriver.Chrome.return_value = mock_chrome
    
    scraper = YahooFinanceScraper(config)
    scraper._init_driver()
    
    assert mock_webdriver.ChromeOptions.called
    assert mock_webdriver.Chrome.called
    assert scraper.driver == mock_chrome

def test_get_table_data(config, mock_driver):
    """Test table data extraction"""
    scraper = YahooFinanceScraper(config)
    scraper.driver = mock_driver
    
    data = scraper._get_table_data()
    assert isinstance(data, list)
    assert len(data) > 0
    assert all(isinstance(item, dict) for item in data)

def test_scrape_data(config, mock_driver):
    """Test full data scraping"""
    scraper = YahooFinanceScraper(config)
    scraper.driver = mock_driver
    
    start_date = datetime.now()
    data = scraper.scrape_data(start_date)
    
    assert isinstance(data, list)
    assert len(data) > 0
    assert all(isinstance(item, dict) for item in data)
    assert mock_driver.current_url == config.YAHOO_FINANCE_URL

def test_quick_scrape(config, mock_driver):
    """Test quick scrape functionality"""
    scraper = YahooFinanceScraper(config)
    scraper.driver = mock_driver
    
    data = scraper.quick_scrape()
    
    assert isinstance(data, list)
    assert len(data) > 0
    assert all(isinstance(item, dict) for item in data)
    assert mock_driver.current_url == config.YAHOO_FINANCE_URL

def test_cleanup(config, mock_driver):
    """Test cleanup method"""
    scraper = YahooFinanceScraper(config)
    scraper.driver = mock_driver
    
    scraper.cleanup()
    assert scraper.driver is None

@pytest.mark.parametrize("error_condition", [
    "driver_error",
    "network_error",
    "parse_error"
])
def test_error_handling(config, error_condition):
    """Test error handling in different scenarios"""
    scraper = YahooFinanceScraper(config)
    
    with pytest.raises(Exception):
        if error_condition == "driver_error":
            scraper.driver = None
            scraper.scrape_data(datetime.now())
        elif error_condition == "network_error":
            scraper.driver = MagicMock()
            scraper.driver.get.side_effect = Exception("Network error")
            scraper.scrape_data(datetime.now())
        elif error_condition == "parse_error":
            scraper.driver = MagicMock()
            scraper.driver.find_elements.side_effect = Exception("Parse error")
            scraper.scrape_data(datetime.now()) 