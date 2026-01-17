"""Helper utility functions."""
from datetime import datetime, timedelta
from typing import Optional
from urllib.parse import urlparse
from src.schema.schemas import CrawlFrequency


def generate_crawl_id(website_url: str) -> str:
    """Generate a unique crawl ID from website URL."""
    parsed = urlparse(website_url)
    domain = parsed.netloc.replace("www.", "").replace(".", "_")
    timestamp = datetime.now().strftime("%Y%m%d")
    return f"{domain}_{timestamp}"


def calculate_next_run_time(frequency: CrawlFrequency, last_run: Optional[datetime] = None) -> datetime:
    """Calculate the next run time based on frequency."""
    if last_run is None:
        return datetime.now()
    
    if frequency == CrawlFrequency.HOURLY:
        return last_run + timedelta(hours=1)
    elif frequency == CrawlFrequency.DAILY:
        return last_run + timedelta(days=1)
    elif frequency == CrawlFrequency.WEEKLY:
        return last_run + timedelta(weeks=1)
    elif frequency == CrawlFrequency.MONTHLY:
        return last_run + timedelta(days=30)
    else:
        return last_run + timedelta(days=1)
