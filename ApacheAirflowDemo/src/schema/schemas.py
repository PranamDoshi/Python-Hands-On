"""Pydantic schemas for data validation."""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class CrawlFrequency(str, Enum):
    """Frequency options for recurring crawls."""
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class CrawlStatus(str, Enum):
    """Status options for crawls."""
    PENDING = "pending"
    STARTED = "started"
    EXTRACTING = "extracting"
    CRAWLING = "crawling"
    COMPLETED = "completed"
    FAILED = "failed"


class PDPStatus(str, Enum):
    """Status options for Product Detail Pages."""
    NEW = "new"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class RecurringCrawl(BaseModel):
    """Schema for recurring crawl configuration."""
    crawl_id: str = Field(..., title="Crawl ID", description="Main ID generated using the website details for this scraper")
    website_url: str = Field(..., description="Base URL of the website to crawl")
    frequency: CrawlFrequency = Field(..., description="Frequency of the crawl")
    categories: List[str] = Field(default_factory=list, description="List of categories to extract")
    xpaths: Dict[str, str] = Field(default_factory=dict, description="XPath mappings for data extraction")
    status: CrawlStatus = Field(default=CrawlStatus.PENDING, description="Current status of the crawl")
    created_at: Optional[datetime] = Field(default=None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(default=None, description="Last update timestamp")
    last_run_at: Optional[datetime] = Field(default=None, description="Last execution timestamp")
    next_run_at: Optional[datetime] = Field(default=None, description="Next scheduled execution timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "crawl_id": "example_com_2024",
                "website_url": "https://example.com",
                "frequency": "daily",
                "categories": ["electronics", "books"],
                "xpaths": {
                    "title": "//h1[@class='product-title']",
                    "price": "//span[@class='price']"
                }
            }
        }


class RecurringCrawlCreate(BaseModel):
    """Schema for creating a new recurring crawl."""
    website_url: str
    frequency: CrawlFrequency
    categories: List[str]
    xpaths: Dict[str, str]


class RecurringCrawlUpdate(BaseModel):
    """Schema for updating a recurring crawl."""
    frequency: Optional[CrawlFrequency] = None
    categories: Optional[List[str]] = None
    xpaths: Optional[Dict[str, str]] = None
    status: Optional[CrawlStatus] = None


class PDPDocument(BaseModel):
    """Schema for Product Detail Page document."""
    pdp_id: str = Field(..., description="Unique identifier for the PDP")
    crawl_id: str = Field(..., description="Associated crawl ID")
    pdp_url: str = Field(..., description="URL of the Product Detail Page")
    category: Optional[str] = Field(default=None, description="Category of the product")
    status: PDPStatus = Field(default=PDPStatus.NEW, description="Current status of the PDP")
    extracted_data: Dict[str, Any] = Field(default_factory=dict, description="Scraped data from the PDP")
    scraper_details: Dict[str, Any] = Field(default_factory=dict, description="Details about the scraping process")
    created_at: Optional[datetime] = Field(default=None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(default=None, description="Last update timestamp")
    error_message: Optional[str] = Field(default=None, description="Error message if scraping failed")


class ExtractionStats(BaseModel):
    """Schema for extraction statistics."""
    crawl_id: str
    total_categories: int = 0
    processed_categories: int = 0
    total_pdps_found: int = 0
    extraction_started_at: Optional[datetime] = None
    extraction_completed_at: Optional[datetime] = None
    plp_stats: Dict[str, Any] = Field(default_factory=dict, description="Stats for each Product Listing Page")


class QueueMessage(BaseModel):
    """Schema for queue messages."""
    crawl_id: str
    task_id: str
    payload: Dict[str, Any]
    created_at: datetime = Field(default_factory=datetime.now)