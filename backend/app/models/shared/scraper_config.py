from dataclasses import dataclass
from typing import Dict

@dataclass
class ScraperConfig:
    headers: Dict[str, str]
    verify_ssl: bool
    timeout: int
    
    @classmethod
    def default_browser_config(cls) -> 'ScraperConfig':
        return cls(
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            },
            verify_ssl=False,
            timeout=30
        )