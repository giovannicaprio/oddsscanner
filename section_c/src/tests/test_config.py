import os
import pytest
from src.config import Config

def test_config_initialization():
    """Test Config class initialization with default values"""
    config = Config()
    assert config.YAHOO_FINANCE_URL == "https://finance.yahoo.com/quote/BTC-EUR/history"
    assert "data" in config.DATA_DIR
    assert config.MAX_RETRIES == 3
    assert config.TIMEOUT == 30
    assert config.MAX_DAYS == 355
    assert config.DATE_FORMAT == "%Y-%m-%d"

def test_config_custom_values():
    """Test Config class initialization with custom values"""
    custom_config = Config(
        YAHOO_FINANCE_URL="https://test.url",
        DATA_DIR="/custom/path",
        OUTPUT_FILE="/custom/path/output.csv",
        MAX_RETRIES=5,
        TIMEOUT=60,
        MAX_DAYS=100,
        DATE_FORMAT="%d-%m-%Y"
    )
    
    assert custom_config.YAHOO_FINANCE_URL == "https://test.url"
    assert custom_config.DATA_DIR == "/custom/path"
    assert custom_config.OUTPUT_FILE == "/custom/path/output.csv"
    assert custom_config.MAX_RETRIES == 5
    assert custom_config.TIMEOUT == 60
    assert custom_config.MAX_DAYS == 100
    assert custom_config.DATE_FORMAT == "%d-%m-%Y"

def test_data_directory_creation(tmp_path):
    """Test that data directory is created if it doesn't exist"""
    test_dir = tmp_path / "test_data"
    config = Config(DATA_DIR=str(test_dir))
    assert os.path.exists(test_dir)

def test_output_file_path(tmp_path):
    """Test output file path construction"""
    test_dir = tmp_path / "test_data"
    config = Config(
        DATA_DIR=str(test_dir),
        OUTPUT_FILE=str(test_dir / "output.csv")
    )
    assert config.OUTPUT_FILE.endswith("output.csv")
    assert os.path.dirname(config.OUTPUT_FILE) == str(test_dir) 