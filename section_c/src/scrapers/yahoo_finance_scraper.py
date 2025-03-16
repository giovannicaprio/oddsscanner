from datetime import datetime
from typing import List, Dict, Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

from .base_scraper import BaseScraper
from .web_driver import WebDriver, ChromeDriver
from .date_filter import PriceData, DateFilterStrategy, LastTenDaysFilter
from .models import ScrapingResult
from ..config import Config

class YahooFinanceScraper(BaseScraper):
    """Scraper for Yahoo Finance BTC-EUR price data"""
    
    def __init__(self, config: Config, web_driver: Optional[WebDriver] = None,
                 filter_strategy: Optional[DateFilterStrategy] = None):
        """
        Initialize the scraper with configuration and dependencies
        
        Args:
            config: Configuration object containing scraping settings
            web_driver: WebDriver implementation (defaults to ChromeDriver)
            filter_strategy: DateFilterStrategy implementation (defaults to LastTenDaysFilter)
        """
        self.config = config
        self.web_driver = web_driver or ChromeDriver()
        self.filter_strategy = filter_strategy or LastTenDaysFilter()
        self.logger = logging.getLogger(__name__)
    
    def _handle_cookie_consent(self) -> None:
        """Handle cookie consent popup if present"""
        try:
            consent_button = WebDriverWait(self.web_driver.get_driver(), 5).until(
                EC.presence_of_element_located((By.NAME, "agree"))
            )
            consent_button.click()
            self.logger.info("Cookie consent handled")
        except TimeoutException:
            self.logger.info("No cookie consent needed")
    
    def _extract_price_data(self) -> List[PriceData]:
        """
        Extract BTC-EUR price data from the loaded page
        
        Returns:
            List of PriceData objects containing date and closing values
            
        Raises:
            NoSuchElementException: If required elements are not found
            TimeoutException: If page takes too long to load
        """
        table = WebDriverWait(self.web_driver.get_driver(), self.config.TIMEOUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table"))
        )
        rows = table.find_elements(By.TAG_NAME, "tr")
        self.logger.info(f"Found {len(rows)} rows in the table")
        
        data = []
        
        for row in rows[1:]:  # Skip header row
            try:
                cols = row.find_elements(By.TAG_NAME, "td")
                if cols:
                    yahoo_date = cols[0].text
                    self.logger.info(f"Extracted date from Yahoo: {yahoo_date}")
                    
                    data.append(PriceData(
                        date=yahoo_date,
                        closing_value=cols[4].text
                    ))
            except Exception as e:
                self.logger.warning(f"Failed to process row: {str(e)}")
                continue
        
        return data
    
    def scrape_data(self, start_date: datetime) -> ScrapingResult:
        """
        Scrape historical BTC-EUR price data from Yahoo Finance
        
        Args:
            start_date: The date to start scraping from
            
        Returns:
            ScrapingResult containing success status and data/error
        """
        try:
            self.web_driver.initialize()
            self.logger.info(f"Accessing URL: {self.config.YAHOO_FINANCE_URL}")
            self.web_driver.get(self.config.YAHOO_FINANCE_URL)
            
            self._handle_cookie_consent()
            price_data = self._extract_price_data()
            
            result_data = [{"Date": data.date, "BTC Closing Value": data.closing_value} 
                          for data in price_data]
            
            return ScrapingResult(success=True, data=result_data)
            
        except Exception as e:
            self.logger.error(f"Error scraping data: {str(e)}")
            return ScrapingResult(success=False, error=str(e))
        finally:
            self.cleanup()
    
    def quick_scrape(self, target_date: Optional[datetime] = None) -> ScrapingResult:
        """
        Perform a quick scrape of BTC-EUR prices around the target date
        
        Args:
            target_date: The target date to get prices for. If None, returns most recent prices.
            
        Returns:
            ScrapingResult containing success status and data/error
        """
        try:
            self.web_driver.initialize()
            self.logger.info(f"Starting quick scrape for date: {target_date.strftime(self.config.DATE_FORMAT) if target_date else 'most recent'}")
            self.web_driver.get(self.config.YAHOO_FINANCE_URL)
            
            self._handle_cookie_consent()
            price_data = self._extract_price_data()
            self.logger.info(f"Extracted {len(price_data)} price data entries")
            
            if target_date:
                price_data = self.filter_strategy.filter(price_data, target_date)
            else:
                price_data = price_data[:10]
            
            result_data = [{"Date": data.date, "BTC Closing Value": data.closing_value} 
                          for data in price_data]
            
            self.logger.info(f"Returning {len(result_data)} filtered entries")
            return ScrapingResult(success=True, data=result_data)
            
        except Exception as e:
            self.logger.error(f"Error during quick scrape: {str(e)}")
            return ScrapingResult(success=False, error=str(e))
        finally:
            self.cleanup()
    
    def cleanup(self) -> None:
        """Close the browser and cleanup resources"""
        self.web_driver.quit() 