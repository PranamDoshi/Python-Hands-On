"""SQL model for recurring crawls."""
from sqlalchemy import Column, String, DateTime, JSON, Enum as SQLEnum
from sqlalchemy.sql import func
from datetime import datetime
from src.db.connections.sql_db import Base
from src.schema.schemas import CrawlStatus, CrawlFrequency


class RecurringCrawlModel(Base):
    """SQL model for recurring crawl configuration."""
    
    __tablename__ = "recurring_crawls"
    
    crawl_id = Column(String, primary_key=True, index=True)
    website_url = Column(String, nullable=False)
    frequency = Column(SQLEnum(CrawlFrequency), nullable=False)
    categories = Column(JSON, default=list)
    xpaths = Column(JSON, default=dict)
    status = Column(SQLEnum(CrawlStatus), default=CrawlStatus.PENDING)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    last_run_at = Column(DateTime, nullable=True)
    next_run_at = Column(DateTime, nullable=True)
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "crawl_id": self.crawl_id,
            "website_url": self.website_url,
            "frequency": self.frequency.value,
            "categories": self.categories,
            "xpaths": self.xpaths,
            "status": self.status.value,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_run_at": self.last_run_at.isoformat() if self.last_run_at else None,
            "next_run_at": self.next_run_at.isoformat() if self.next_run_at else None,
        }
