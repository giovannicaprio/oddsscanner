from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
import logging

class WebDriver(ABC):
    """Abstract interface for web drivers"""
    
    @abstractmethod
    def initialize(self) -> None:
        """Initialize the web driver"""
        pass
    
    @abstractmethod
    def get(self, url: str) -> None:
        """Navigate to URL"""
        pass
    
    @abstractmethod
    def quit(self) -> None:
        """Quit the driver"""
        pass
    
    @abstractmethod
    def get_driver(self) -> webdriver.Chrome:
        """Get the underlying driver instance"""
        pass

class ChromeDriver(WebDriver):
    """Chrome WebDriver implementation"""
    
    def __init__(self):
        self.driver = None
        self.logger = logging.getLogger(__name__)
    
    def initialize(self) -> None:
        """Initialize Chrome driver with appropriate settings"""
        try:
            self.logger.info("Starting Chromium driver setup")
            options = webdriver.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--headless')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            
            chrome_binary = os.getenv('CHROMIUM_PATH', '/usr/bin/chromium')
            chrome_driver = os.getenv('CHROME_DRIVER_PATH', '/usr/bin/chromedriver')
            
            options.binary_location = chrome_binary
            
            self.logger.info(f"Using Chromium binary at: {chrome_binary}")
            self.logger.info(f"Using Chromium driver at: {chrome_driver}")
            
            service = Service(executable_path=chrome_driver)
            self.driver = webdriver.Chrome(
                service=service,
                options=options
            )
            self.logger.info("Chromium driver initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize Chrome driver: {str(e)}")
            raise RuntimeError("Chrome driver initialization failed") from e
    
    def get(self, url: str) -> None:
        """Navigate to the specified URL"""
        if not self.driver:
            self.initialize()
        self.driver.get(url)
    
    def quit(self) -> None:
        """Quit the driver and cleanup resources"""
        if self.driver:
            try:
                self.driver.quit()
                self.driver = None
                self.logger.info("Chrome driver closed successfully")
            except Exception as e:
                self.logger.error(f"Error during cleanup: {str(e)}")
    
    def get_driver(self) -> webdriver.Chrome:
        """Get the underlying Chrome driver instance"""
        if not self.driver:
            self.initialize()
        return self.driver 