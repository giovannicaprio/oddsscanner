from dataclasses import dataclass, field
from typing import Optional
import os
from pathlib import Path

@dataclass
class Config:
    """
    Application configuration for BTC-EUR price scraper
    
    Attributes:
        YAHOO_FINANCE_URL: URL for Yahoo Finance BTC-EUR historical data
        DATA_DIR: Directory for storing scraped data
        OUTPUT_FILE: File path for storing BTC price history
        MAX_RETRIES: Maximum number of retry attempts for failed operations
        TIMEOUT: Maximum time in seconds to wait for web elements
        MAX_DAYS: Maximum number of days of historical data to fetch
        DATE_FORMAT: Format string for date parsing/formatting
    """
    
    # URLs and endpoints
    YAHOO_FINANCE_URL: str = "https://finance.yahoo.com/quote/BTC-EUR/history"
    
    # File system paths
    DATA_DIR: str = field(default_factory=lambda: os.path.join(
        os.path.dirname(__file__), "..", "data"
    ))
    OUTPUT_FILE: Optional[str] = None
    
    # Scraping settings
    MAX_RETRIES: int = 3
    TIMEOUT: int = 30
    MAX_DAYS: int = 355
    DATE_FORMAT: str = "%Y-%m-%d"
    
    def __post_init__(self):
        """
        Post-initialization setup:
        1. Create data directory if it doesn't exist
        2. Set default output file path if not provided
        3. Validate configuration values
        
        Raises:
            ValueError: If configuration values are invalid
        """
        # Create data directory
        Path(self.DATA_DIR).mkdir(parents=True, exist_ok=True)
        
        # Set default output file path if not provided
        if not self.OUTPUT_FILE:
            self.OUTPUT_FILE = os.path.join(self.DATA_DIR, "btc_eur_history.csv")
        
        # Validate configuration
        self._validate_config()
    
    def _validate_config(self) -> None:
        """
        Validate configuration values
        
        Raises:
            ValueError: If any configuration value is invalid
        """
        if not self.YAHOO_FINANCE_URL.startswith("https://"):
            raise ValueError("YAHOO_FINANCE_URL must be a secure HTTPS URL")
        
        if self.MAX_RETRIES < 1:
            raise ValueError("MAX_RETRIES must be at least 1")
        
        if self.TIMEOUT < 1:
            raise ValueError("TIMEOUT must be at least 1 second")
        
        if self.MAX_DAYS < 1:
            raise ValueError("MAX_DAYS must be at least 1")
        
        try:
            # Verify date format is valid
            from datetime import datetime
            datetime.now().strftime(self.DATE_FORMAT)
        except ValueError as e:
            raise ValueError(f"Invalid DATE_FORMAT: {str(e)}")
    
    @property
    def output_file_path(self) -> Path:
        """Get output file as a Path object"""
        return Path(self.OUTPUT_FILE) 