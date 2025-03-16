from abc import ABC, abstractmethod
from datetime import datetime
from typing import List
from dataclasses import dataclass
import logging

@dataclass
class PriceData:
    """Structure for price data"""
    date: str
    closing_value: str

class DateFilterStrategy(ABC):
    """Abstract interface for date filtering strategies"""
    
    @abstractmethod
    def filter(self, data: List[PriceData], target_date: datetime) -> List[PriceData]:
        """
        Filter price data based on target date
        
        Args:
            data: List of PriceData objects to filter
            target_date: The target date to filter around
            
        Returns:
            Filtered list of PriceData objects
        """
        pass

class LastTenDaysFilter(DateFilterStrategy):
    """Strategy to get last 10 days of data from target date"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def filter(self, data: List[PriceData], target_date: datetime) -> List[PriceData]:
        """
        Filter to get entries from target_date and 9 days before it
        
        Args:
            data: List of PriceData objects to filter
            target_date: The target date to filter around
            
        Returns:
            List of up to 10 PriceData objects
        """
        self.logger.info(f"\n=== Date Filtering Debug ===")
        
        # Convert target_date to Yahoo's format (MMM DD, YYYY)
        target_date_yahoo = target_date.strftime("%b %d, %Y")
        self.logger.info(f"Target date converted to Yahoo format: {target_date_yahoo}")
        self.logger.info(f"Total data points to process: {len(data)}")
        
        # Convert all dates to datetime objects for comparison
        dated_data = []
        self.logger.info("\nConverting and collecting dates:")
        for item in data:
            try:
                self.logger.info(f"\nProcessing data point:")
                self.logger.info(f"Yahoo date string: {item.date}")
                date = datetime.strptime(item.date, "%b %d, %Y")
                self.logger.info(f"Parsed datetime: {date}")
                dated_data.append((date, item))
            except ValueError as e:
                self.logger.warning(f"Failed to parse date {item.date}: {str(e)}")
                continue
        
        if not dated_data:
            self.logger.warning("No valid dates found in the data")
            return []
        
        # Sort by date in descending order (newest first)
        dated_data.sort(key=lambda x: x[0], reverse=True)
        self.logger.info("\nSorted date range:")
        self.logger.info(f"Earliest: {dated_data[-1][0].strftime('%b %d, %Y')}")
        self.logger.info(f"Latest: {dated_data[0][0].strftime('%b %d, %Y')}")
        
        # Convert target_date to datetime for comparison
        target_datetime = datetime.strptime(target_date_yahoo, "%b %d, %Y")
        
        # Find the closest date to target_date
        closest_idx = 0
        for idx, (date, _) in enumerate(dated_data):
            self.logger.info(f"\nComparing dates:")
            self.logger.info(f"Current date: {date.strftime('%b %d, %Y')}")
            self.logger.info(f"Target date: {target_date_yahoo}")
            
            if date <= target_datetime:
                closest_idx = idx
                self.logger.info(f"Found closest date at index {idx}")
                break
        
        # Take up to 10 entries starting from the closest date
        result = [data for _, data in dated_data[closest_idx:closest_idx + 10]]
        self.logger.info("\nFinal results:")
        self.logger.info(f"Retrieved {len(result)} entries")
        for entry in result:
            self.logger.info(f"Date: {entry.date}, Value: {entry.closing_value}")
        
        return result 