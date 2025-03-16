import pytest
from datetime import datetime
from src.config import Config
from src.scrapers.yahoo_finance_scraper import YahooFinanceScraper

@pytest.fixture
def config():
    """Fixture for test configuration"""
    return Config(
        YAHOO_FINANCE_URL="https://test.url",
        DATA_DIR="/tmp/test_data",
        OUTPUT_FILE="/tmp/test_data/output.csv",
        MAX_RETRIES=1,
        TIMEOUT=5,
        MAX_DAYS=10,
        DATE_FORMAT="%Y-%m-%d"
    )

@pytest.fixture
def mock_driver():
    """Mock Selenium WebDriver"""
    class MockElement:
        def __init__(self, text):
            self.text = text
        
        def find_elements(self, by, value):
            return [MockElement("test")]
    
    class MockDriver:
        def __init__(self):
            self.current_url = None
        
        def get(self, url):
            self.current_url = url
        
        def quit(self):
            pass
        
        def find_element(self, by, value):
            return MockElement("test")
        
        def find_elements(self, by, value):
            return [MockElement("test")]
    
    return MockDriver()

@pytest.fixture
def sample_scrape_data():
    """Sample scraping data for tests"""
    return [
        {"Date": "2025-03-16", "BTC Closing Value": "45000"},
        {"Date": "2025-03-15", "BTC Closing Value": "44500"}
    ] 