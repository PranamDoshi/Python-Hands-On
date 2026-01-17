"""Tasks related to extraction phase."""
from airflow import DAG
from airflow.operators.python import PythonOperator
from typing import Dict, Any
from src.queues.queue_manager import QueueManager
from src.db.connections.mongo_db import get_mongo_client
from src.schema.schemas import CrawlStatus, PDPStatus


def add_to_extractor_queue_task(**context) -> None:
    """Add crawl task to extractor queue."""
    dag_run = context['dag_run']
    crawl_id = dag_run.conf.get('crawl_id')
    
    if not crawl_id:
        raise ValueError("crawl_id must be provided in DAG run configuration")
    
    queue_manager = QueueManager()
    payload = {
        "crawl_id": crawl_id,
        "triggered_at": context['ts']
    }
    
    success = queue_manager.push_to_extractor_queue(crawl_id, payload)
    if not success:
        raise Exception("Failed to push to extractor queue")
    
    print(f"Successfully added crawl {crawl_id} to extractor queue")


def wait_for_extractor_complete_task(**context) -> None:
    """Wait for extractor to complete and create/update PDP docs."""
    dag_run = context['dag_run']
    crawl_id = dag_run.conf.get('crawl_id')
    
    if not crawl_id:
        raise ValueError("crawl_id must be provided in DAG run configuration")
    
    mongo_db = get_mongo_client()
    max_wait_time = 3600  # 1 hour max wait
    poll_interval = 30  # Poll every 30 seconds
    elapsed_time = 0
    
    while elapsed_time < max_wait_time:
        # Check if extraction is completed
        crawl_doc = mongo_db.recurring_crawls.find_one({"crawl_id": crawl_id})
        
        if crawl_doc and crawl_doc.get("extraction_status") == "completed":
            print(f"Extraction completed for crawl {crawl_id}")
            return
        
        # Check if all PDPs are processed
        total_pdps = mongo_db.pdp_documents.count_documents({"crawl_id": crawl_id})
        new_pdps = mongo_db.pdp_documents.count_documents({
            "crawl_id": crawl_id,
            "status": PDPStatus.NEW.value
        })
        
        if total_pdps > 0 and new_pdps == 0:
            # All PDPs have been processed by extractor
            print(f"All PDPs processed for crawl {crawl_id}")
            return
        
        import time
        time.sleep(poll_interval)
        elapsed_time += poll_interval
        print(f"Waiting for extractor to complete... ({elapsed_time}s elapsed)")
    
    raise TimeoutError(f"Extractor did not complete within {max_wait_time} seconds")


def create_update_pdp_docs_task(**context) -> None:
    """Create or update PDP documents in MongoDB storage."""
    # This task is typically handled by the extractor worker
    # but can be used for initial setup if needed
    dag_run = context['dag_run']
    crawl_id = dag_run.conf.get('crawl_id')
    
    if not crawl_id:
        raise ValueError("crawl_id must be provided in DAG run configuration")
    
    mongo_db = get_mongo_client()
    
    # Update recurring crawl status to extracting
    mongo_db.recurring_crawls.update_one(
        {"crawl_id": crawl_id},
        {
            "$set": {
                "status": CrawlStatus.EXTRACTING.value,
                "extraction_status": "started",
                "updated_at": context['ts']
            }
        },
        upsert=True
    )
    
    print(f"Updated crawl {crawl_id} status to extracting")
