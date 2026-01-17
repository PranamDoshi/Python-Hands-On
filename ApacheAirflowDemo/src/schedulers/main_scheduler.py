"""Main Scheduler - checks recurring crawls and triggers DAGs."""
import time
import logging
from datetime import datetime
from typing import List
from airflow.api.client.local_client import Client
from src.db.connections.sql_db import get_sql_session
from src.db.models.recurring_crawl import RecurringCrawlModel
from src.config.settings import settings
from src.schema.schemas import CrawlStatus, CrawlFrequency
from src.utils.helpers import calculate_next_run_time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MainScheduler:
    """Scheduler that checks recurring crawls and triggers DAGs."""
    
    def __init__(self):
        self.airflow_client = Client(None, None)
        self.poll_interval = settings.SCHEDULER_INTERVAL_SECONDS
        self.running = False
    
    def check_recurring_crawls(self) -> List[RecurringCrawlModel]:
        """Check all recurring crawls & their frequency for scheduling time."""
        now = datetime.now()
        due_crawls = []
        
        try:
            with get_sql_session() as session:
                crawls = session.query(RecurringCrawlModel).filter(
                    RecurringCrawlModel.status != CrawlStatus.COMPLETED.value
                ).all()
                
                for crawl in crawls:
                    # Check if it's time to run
                    if crawl.next_run_at and crawl.next_run_at <= now:
                        due_crawls.append(crawl)
                    elif crawl.next_run_at is None:
                        # First run - schedule immediately
                        due_crawls.append(crawl)
                
                logger.info(f"Found {len(due_crawls)} due crawls out of {len(crawls)} total")
                return due_crawls
                
        except Exception as e:
            logger.error(f"Error checking recurring crawls: {e}", exc_info=True)
            return []
    
    def trigger_dag_for_crawl(self, crawl: RecurringCrawlModel) -> bool:
        """For each recurring crawl start the DAG as per the frequency set for the crawl."""
        try:
            dag_id = "main_crawl_dag"
            conf = {
                "crawl_id": crawl.crawl_id
            }
            
            # Trigger the DAG
            self.airflow_client.trigger_dag(
                dag_id=dag_id,
                conf=conf,
                run_id=f"{crawl.crawl_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )
            
            logger.info(f"Triggered DAG for crawl: {crawl.crawl_id}")
            
            # Update next_run_at
            with get_sql_session() as session:
                db_crawl = session.query(RecurringCrawlModel).filter_by(crawl_id=crawl.crawl_id).first()
                if db_crawl:
                    db_crawl.last_run_at = datetime.now()
                    db_crawl.next_run_at = calculate_next_run_time(
                        CrawlFrequency(db_crawl.frequency),
                        db_crawl.last_run_at
                    )
                    session.commit()
                    logger.info(f"Updated next_run_at for crawl: {crawl.crawl_id}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error triggering DAG for crawl {crawl.crawl_id}: {e}", exc_info=True)
            return False
    
    def run(self):
        """Main scheduler loop."""
        logger.info("Main Scheduler started")
        self.running = True
        
        while self.running:
            try:
                # Check all recurring crawls & their frequency for scheduling time
                due_crawls = self.check_recurring_crawls()
                
                # For each recurring crawl start the DAG as per the frequency set for the crawl
                for crawl in due_crawls:
                    self.trigger_dag_for_crawl(crawl)
                
                # Sleep until next check
                time.sleep(self.poll_interval)
                
            except KeyboardInterrupt:
                logger.info("Main Scheduler stopped by user")
                self.running = False
            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}", exc_info=True)
                time.sleep(self.poll_interval)
    
    def stop(self):
        """Stop the scheduler."""
        self.running = False
        logger.info("Main Scheduler stopping...")


if __name__ == "__main__":
    scheduler = MainScheduler()
    try:
        scheduler.run()
    except KeyboardInterrupt:
        scheduler.stop()
