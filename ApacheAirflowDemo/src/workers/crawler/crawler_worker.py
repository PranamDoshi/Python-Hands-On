"""Crawling Worker - scrapes Product Detail Pages (PDPs)."""
import time
import logging
from typing import Dict, Any
from datetime import datetime
from src.queues.queue_manager import QueueManager
from src.db.connections.mongo_db import get_mongo_client
from src.config.settings import settings
from src.schema.schemas import QueueMessage, PDPStatus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CrawlerWorker:
    """Worker for scraping Product Detail Pages."""
    
    def __init__(self):
        self.queue_manager = QueueManager()
        self.mongo_db = get_mongo_client()
        self.poll_interval = settings.CRAWLER_WORKER_POLL_INTERVAL
        self.running = False
    
    def poll_crawler_queue(self) -> QueueMessage:
        """Poll the crawler queue for new tasks."""
        return self.queue_manager.pop_from_crawler_queue(timeout=self.poll_interval)
    
    def scrape_pdp(self, pdp_url: str, xpaths: Dict[str, str]) -> Dict[str, Any]:
        """Scrape PDP using the xPaths set in recurring crawl config."""
        logger.info(f"Scraping PDP: {pdp_url}")
        
        extracted_data = {}
        scraper_details = {
            "scraped_at": datetime.now().isoformat(),
            "xpaths_used": list(xpaths.keys())
        }
        
        try:
            # TODO: Implement actual scraping logic
            # This should:
            # 1. Navigate to the PDP URL
            # 2. Extract data using the provided xpaths
            # 3. Return the extracted data
            
            # Placeholder implementation
            # from playwright.sync_api import sync_playwright
            # with sync_playwright() as p:
            #     browser = p.chromium.launch()
            #     page = browser.new_page()
            #     page.goto(pdp_url)
            #     
            #     for field_name, xpath in xpaths.items():
            #         try:
            #             element = page.query_selector(xpath)
            #             if element:
            #                 extracted_data[field_name] = element.inner_text()
            #         except Exception as e:
            #             logger.warning(f"Failed to extract {field_name}: {e}")
            #     
            #     browser.close()
            
            # Example extracted data structure
            for field_name in xpaths.keys():
                extracted_data[field_name] = f"Extracted value for {field_name}"
            
            scraper_details["status"] = "success"
            scraper_details["fields_extracted"] = len(extracted_data)
            
            logger.info(f"Successfully scraped {len(extracted_data)} fields from {pdp_url}")
            
        except Exception as e:
            logger.error(f"Error scraping PDP {pdp_url}: {e}")
            scraper_details["status"] = "failed"
            scraper_details["error"] = str(e)
            raise
        
        return {
            "extracted_data": extracted_data,
            "scraper_details": scraper_details
        }
    
    def update_mongo_db_doc(self, pdp_id: str, crawl_id: str, extracted_data: Dict[str, Any], 
                           scraper_details: Dict[str, Any], status: PDPStatus, 
                           error_message: str = None) -> None:
        """Update Mongo DB doc with scraper details & ending PDP Status."""
        update_data = {
            "extracted_data": extracted_data,
            "scraper_details": scraper_details,
            "status": status.value,
            "updated_at": datetime.now()
        }
        
        if error_message:
            update_data["error_message"] = error_message
        
        self.mongo_db.pdp_documents.update_one(
            {"pdp_id": pdp_id, "crawl_id": crawl_id},
            {"$set": update_data}
        )
        
        logger.info(f"Updated PDP document {pdp_id} with status {status.value}")
    
    def process_task(self, message: QueueMessage) -> None:
        """Process a single crawling task."""
        pdp_id = message.task_id
        pdp_url = message.payload.get("pdp_url")
        crawl_id = message.crawl_id
        
        if not pdp_url:
            logger.error(f"No pdp_url in message payload for task {pdp_id}")
            return
        
        logger.info(f"Processing crawling task for PDP: {pdp_id} ({pdp_url})")
        
        try:
            # Get crawl configuration to retrieve xpaths
            crawl_doc = self.mongo_db.recurring_crawls.find_one({"crawl_id": crawl_id})
            if not crawl_doc:
                logger.error(f"Crawl {crawl_id} not found in MongoDB")
                return
            
            xpaths = crawl_doc.get("xpaths", {})
            
            # Update PDP status to processing
            self.mongo_db.pdp_documents.update_one(
                {"pdp_id": pdp_id},
                {"$set": {"status": PDPStatus.PROCESSING.value, "updated_at": datetime.now()}}
            )
            
            # Scrape the PDP
            result = self.scrape_pdp(pdp_url, xpaths)
            
            # Update MongoDB document with scraped data
            self.update_mongo_db_doc(
                pdp_id=pdp_id,
                crawl_id=crawl_id,
                extracted_data=result["extracted_data"],
                scraper_details=result["scraper_details"],
                status=PDPStatus.COMPLETED
            )
            
            logger.info(f"Crawling task completed for PDP: {pdp_id}")
            
        except Exception as e:
            logger.error(f"Error processing crawling task: {e}", exc_info=True)
            # Update status to failed
            self.update_mongo_db_doc(
                pdp_id=pdp_id,
                crawl_id=crawl_id,
                extracted_data={},
                scraper_details={"error": str(e)},
                status=PDPStatus.FAILED,
                error_message=str(e)
            )
    
    def run(self):
        """Main worker loop - continuously poll and process tasks."""
        logger.info("Crawler Worker started")
        self.running = True
        
        while self.running:
            try:
                message = self.poll_crawler_queue()
                if message:
                    self.process_task(message)
                else:
                    time.sleep(self.poll_interval)
            except KeyboardInterrupt:
                logger.info("Crawler Worker stopped by user")
                self.running = False
            except Exception as e:
                logger.error(f"Error in worker loop: {e}", exc_info=True)
                time.sleep(self.poll_interval)
    
    def stop(self):
        """Stop the worker."""
        self.running = False
        logger.info("Crawler Worker stopping...")


if __name__ == "__main__":
    worker = CrawlerWorker()
    try:
        worker.run()
    except KeyboardInterrupt:
        worker.stop()
