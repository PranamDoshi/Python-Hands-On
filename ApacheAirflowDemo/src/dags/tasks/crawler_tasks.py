"""Tasks related to crawling phase."""
from airflow import DAG
from airflow.operators.python import PythonOperator
from typing import Dict, Any
from src.db.connections.mongo_db import get_mongo_client
from src.schema.schemas import CrawlStatus, PDPStatus


def wait_for_crawlers_complete_task(**context) -> None:
    """Wait for crawlers to process all extracted PDPs."""
    dag_run = context['dag_run']
    crawl_id = dag_run.conf.get('crawl_id')
    
    if not crawl_id:
        raise ValueError("crawl_id must be provided in DAG run configuration")
    
    mongo_db = get_mongo_client()
    max_wait_time = 7200  # 2 hours max wait
    poll_interval = 60  # Poll every minute
    elapsed_time = 0
    
    while elapsed_time < max_wait_time:
        # Check if all PDPs are completed
        total_pdps = mongo_db.pdp_documents.count_documents({"crawl_id": crawl_id})
        completed_pdps = mongo_db.pdp_documents.count_documents({
            "crawl_id": crawl_id,
            "status": {"$in": [PDPStatus.COMPLETED.value, PDPStatus.FAILED.value]}
        })
        
        if total_pdps > 0 and completed_pdps == total_pdps:
            print(f"All PDPs processed for crawl {crawl_id}")
            
            # Update crawl status
            mongo_db.recurring_crawls.update_one(
                {"crawl_id": crawl_id},
                {
                    "$set": {
                        "status": CrawlStatus.COMPLETED.value,
                        "updated_at": context['ts']
                    }
                }
            )
            return
        
        # Check for extraction completion status
        crawl_doc = mongo_db.recurring_crawls.find_one({"crawl_id": crawl_id})
        if crawl_doc and crawl_doc.get("extraction_status") == "completed":
            # Extraction is done, now wait for crawlers
            print(f"Extraction completed, waiting for crawlers... ({completed_pdps}/{total_pdps} PDPs completed)")
        
        import time
        time.sleep(poll_interval)
        elapsed_time += poll_interval
    
    raise TimeoutError(f"Crawlers did not complete within {max_wait_time} seconds")
