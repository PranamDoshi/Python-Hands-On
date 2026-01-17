"""PDP Crawling Scheduler - polls MongoDB for new PDPs and pushes to crawler queue."""
import time
import logging
from datetime import datetime
from typing import List
from src.db.connections.mongo_db import get_mongo_client
from src.queues.queue_manager import QueueManager
from src.config.settings import settings
from src.schema.schemas import PDPStatus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDPCrawlingScheduler:
    """Scheduler that polls MongoDB for new PDP documents and pushes them to crawler queue."""
    
    def __init__(self):
        self.mongo_db = get_mongo_client()
        self.queue_manager = QueueManager()
        self.poll_interval = settings.PDP_SCHEDULER_INTERVAL_SECONDS
        self.running = False
    
    def poll_mongo_for_new_pdps(self) -> List[dict]:
        """Poll Mongo for PDP Docs with New Status."""
        try:
            pdps = list(self.mongo_db.pdp_documents.find({
                "status": PDPStatus.NEW.value
            }).limit(100))  # Process in batches
            
            logger.info(f"Found {len(pdps)} new PDPs to process")
            return pdps
            
        except Exception as e:
            logger.error(f"Error polling MongoDB for new PDPs: {e}", exc_info=True)
            return []
    
    def push_pdp_to_crawling_queue(self, pdp_doc: dict) -> bool:
        """Push PDP Doc with their ID & pdp_url to crawling queue."""
        try:
            pdp_id = pdp_doc.get("pdp_id")
            pdp_url = pdp_doc.get("pdp_url")
            crawl_id = pdp_doc.get("crawl_id")
            
            if not pdp_id or not pdp_url or not crawl_id:
                logger.warning(f"Invalid PDP document: missing required fields")
                return False
            
            success = self.queue_manager.push_to_crawler_queue(
                crawl_id=crawl_id,
                pdp_id=pdp_id,
                pdp_url=pdp_url
            )
            
            if success:
                # Update PDP status to processing (will be updated by worker when it starts)
                self.mongo_db.pdp_documents.update_one(
                    {"pdp_id": pdp_id},
                    {"$set": {"status": PDPStatus.PROCESSING.value, "updated_at": datetime.now()}}
                )
                logger.debug(f"Pushed PDP {pdp_id} to crawler queue")
            
            return success
            
        except Exception as e:
            logger.error(f"Error pushing PDP to queue: {e}", exc_info=True)
            return False
    
    def run(self):
        """Main scheduler loop."""
        logger.info("PDP Crawling Scheduler started")
        self.running = True
        
        while self.running:
            try:
                # Poll Mongo for PDP Docs with New Status
                new_pdps = self.poll_mongo_for_new_pdps()
                
                # Push PDP Doc with their ID & pdp_url to crawling queue
                for pdp_doc in new_pdps:
                    self.push_pdp_to_crawling_queue(pdp_doc)
                
                # Sleep until next check
                time.sleep(self.poll_interval)
                
            except KeyboardInterrupt:
                logger.info("PDP Crawling Scheduler stopped by user")
                self.running = False
            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}", exc_info=True)
                time.sleep(self.poll_interval)
    
    def stop(self):
        """Stop the scheduler."""
        self.running = False
        logger.info("PDP Crawling Scheduler stopping...")


if __name__ == "__main__":
    scheduler = PDPCrawlingScheduler()
    try:
        scheduler.run()
    except KeyboardInterrupt:
        scheduler.stop()
