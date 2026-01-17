"""Extractor Worker - processes category-level data extraction."""
import time
import logging
from typing import Dict, Any, List
from datetime import datetime
from src.queues.queue_manager import QueueManager
from src.db.connections.sql_db import get_sql_session
from src.db.connections.mongo_db import get_mongo_client
from src.db.models.recurring_crawl import RecurringCrawlModel
from src.config.settings import settings
from src.schema.schemas import QueueMessage, PDPStatus, CrawlStatus, ExtractionStats

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExtractorWorker:
    """Worker for extracting category-level data and creating PDP documents."""
    
    def __init__(self):
        self.queue_manager = QueueManager()
        self.mongo_db = get_mongo_client()
        self.poll_interval = settings.EXTRACTOR_WORKER_POLL_INTERVAL
        self.running = False
    
    def poll_extractor_queue(self) -> QueueMessage:
        """Poll the extractor queue for new tasks."""
        return self.queue_manager.pop_from_extractor_queue(timeout=self.poll_interval)
    
    def process_categories(self, crawl_id: str, categories: List[str], xpaths: Dict[str, str]) -> Dict[str, Any]:
        """Process all categories set in recurring crawl config."""
        logger.info(f"Processing {len(categories)} categories for crawl {crawl_id}")
        
        stats = {
            "total_categories": len(categories),
            "processed_categories": 0,
            "total_pdps_found": 0,
            "plp_stats": {}
        }
        
        for category in categories:
            try:
                logger.info(f"Processing category: {category}")
                
                # TODO: Implement actual category extraction logic
                # This should:
                # 1. Navigate to category page (PLP - Product Listing Page)
                # 2. Extract all PDP URLs from the listing
                # 3. Create PDP documents in MongoDB
                
                pdp_urls = self._extract_pdp_urls_from_category(category, crawl_id)
                
                # Create PDP documents
                for pdp_url in pdp_urls:
                    self._create_pdp_document(crawl_id, category, pdp_url)
                    stats["total_pdps_found"] += 1
                
                stats["processed_categories"] += 1
                stats["plp_stats"][category] = {
                    "pdps_found": len(pdp_urls),
                    "status": "completed"
                }
                
                logger.info(f"Category {category} processed: {len(pdp_urls)} PDPs found")
                
            except Exception as e:
                logger.error(f"Error processing category {category}: {e}")
                stats["plp_stats"][category] = {
                    "pdps_found": 0,
                    "status": "failed",
                    "error": str(e)
                }
        
        return stats
    
    def _extract_pdp_urls_from_category(self, category: str, crawl_id: str) -> List[str]:
        """Extract PDP URLs from a category page (PLP)."""
        # TODO: Implement actual extraction logic
        # This should use the crawl configuration to navigate to the category page
        # and extract all product URLs
        
        # Placeholder implementation
        logger.info(f"Extracting PDP URLs from category: {category}")
        pdp_urls = []
        
        # Example: Use playwright or selenium to navigate and extract
        # from playwright.sync_api import sync_playwright
        # with sync_playwright() as p:
        #     browser = p.chromium.launch()
        #     page = browser.new_page()
        #     page.goto(category_url)
        #     # Extract PDP URLs using selectors
        #     pdp_urls = page.query_selector_all('a.product-link')
        #     browser.close()
        
        return pdp_urls
    
    def _create_pdp_document(self, crawl_id: str, category: str, pdp_url: str) -> None:
        """Create a PDP document in MongoDB."""
        from bson import ObjectId
        
        pdp_id = str(ObjectId())
        pdp_doc = {
            "pdp_id": pdp_id,
            "crawl_id": crawl_id,
            "pdp_url": pdp_url,
            "category": category,
            "status": PDPStatus.NEW.value,
            "extracted_data": {},
            "scraper_details": {},
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        self.mongo_db.pdp_documents.insert_one(pdp_doc)
        logger.debug(f"Created PDP document: {pdp_id} for URL: {pdp_url}")
    
    def update_db_with_status_and_stats(self, crawl_id: str, stats: Dict[str, Any]) -> None:
        """Update SQL DB with status & stats."""
        try:
            with get_sql_session() as session:
                crawl = session.query(RecurringCrawlModel).filter_by(crawl_id=crawl_id).first()
                if crawl:
                    # Update status
                    crawl.status = CrawlStatus.EXTRACTING
                    session.commit()
                    logger.info(f"Updated crawl {crawl_id} status in SQL DB")
        except Exception as e:
            logger.error(f"Error updating SQL DB: {e}")
        
        # Update MongoDB with extraction stats
        try:
            extraction_stats = ExtractionStats(
                crawl_id=crawl_id,
                total_categories=stats["total_categories"],
                processed_categories=stats["processed_categories"],
                total_pdps_found=stats["total_pdps_found"],
                extraction_completed_at=datetime.now(),
                plp_stats=stats["plp_stats"]
            )
            
            self.mongo_db.recurring_crawls.update_one(
                {"crawl_id": crawl_id},
                {
                    "$set": {
                        "extraction_status": "completed",
                        "extraction_stats": extraction_stats.model_dump(),
                        "status": CrawlStatus.CRAWLING.value,
                        "updated_at": datetime.now()
                    }
                }
            )
            logger.info(f"Updated extraction stats for crawl {crawl_id} in MongoDB")
        except Exception as e:
            logger.error(f"Error updating MongoDB: {e}")
    
    def process_task(self, message: QueueMessage) -> None:
        """Process a single extraction task."""
        crawl_id = message.crawl_id
        logger.info(f"Processing extraction task for crawl: {crawl_id}")
        
        try:
            # Get crawl configuration from SQL DB
            with get_sql_session() as session:
                crawl = session.query(RecurringCrawlModel).filter_by(crawl_id=crawl_id).first()
                if not crawl:
                    logger.error(f"Crawl {crawl_id} not found in SQL DB")
                    return
                
                categories = crawl.categories or []
                xpaths = crawl.xpaths or {}
            
            # Process all categories
            stats = self.process_categories(crawl_id, categories, xpaths)
            
            # Update DB with status and stats
            self.update_db_with_status_and_stats(crawl_id, stats)
            
            logger.info(f"Extraction task completed for crawl: {crawl_id}")
            
        except Exception as e:
            logger.error(f"Error processing extraction task: {e}", exc_info=True)
            # Update status to failed
            self.mongo_db.recurring_crawls.update_one(
                {"crawl_id": crawl_id},
                {
                    "$set": {
                        "status": CrawlStatus.FAILED.value,
                        "error": str(e),
                        "updated_at": datetime.now()
                    }
                }
            )
    
    def run(self):
        """Main worker loop - continuously poll and process tasks."""
        logger.info("Extractor Worker started")
        self.running = True
        
        while self.running:
            try:
                message = self.poll_extractor_queue()
                if message:
                    self.process_task(message)
                else:
                    time.sleep(self.poll_interval)
            except KeyboardInterrupt:
                logger.info("Extractor Worker stopped by user")
                self.running = False
            except Exception as e:
                logger.error(f"Error in worker loop: {e}", exc_info=True)
                time.sleep(self.poll_interval)
    
    def stop(self):
        """Stop the worker."""
        self.running = False
        logger.info("Extractor Worker stopping...")


if __name__ == "__main__":
    worker = ExtractorWorker()
    try:
        worker.run()
    except KeyboardInterrupt:
        worker.stop()
