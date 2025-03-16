from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict

class BaseScraper(ABC):
    """Base class for all scrapers"""
    
    @abstractmethod
    def scrape_data(self, start_date: datetime) -> List[Dict]:
        """
        Scrape data from a source starting from the given date
        
        Args:
            start_date: The date to start scraping from
            
        Returns:
            List of dictionaries containing the scraped data
        """
        pass
    
    @abstractmethod
    def quick_scrape(self) -> List[Dict]:
        """
        Perform a quick scrape of the most recent data
        
        Returns:
            List of dictionaries containing the scraped data
        """
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """Cleanup any resources used by the scraper"""
        pass 