from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class ScrapingResult:
    """Data transfer object for scraping results"""
    success: bool
    data: List[dict]
    error: Optional[str] = None
    timestamp: datetime = datetime.now()

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'success': self.success,
            'data': {
                'rows': self.data
            } if self.success else None,
            'error': self.error,
            'timestamp': self.timestamp.isoformat()
        } 