"""Main DAG for orchestrating crawl workflow."""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from src.dags.tasks.extractor_tasks import (
    add_to_extractor_queue_task,
    wait_for_extractor_complete_task,
    create_update_pdp_docs_task
)
from src.dags.tasks.crawler_tasks import wait_for_crawlers_complete_task
from src.db.connections.mongo_db import get_mongo_client
from src.schema.schemas import CrawlStatus


default_args = {
    'owner': 'crawl_team',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


def start_crawl_task(**context) -> None:
    """Start of the crawl - update status to Started."""
    dag_run = context['dag_run']
    crawl_id = dag_run.conf.get('crawl_id')
    
    if not crawl_id:
        raise ValueError("crawl_id must be provided in DAG run configuration")
    
    mongo_db = get_mongo_client()
    
    # Update recurring crawl to Started
    mongo_db.recurring_crawls.update_one(
        {"crawl_id": crawl_id},
        {
            "$set": {
                "status": CrawlStatus.STARTED.value,
                "started_at": context['ts'],
                "updated_at": context['ts']
            }
        },
        upsert=True
    )
    
    print(f"Crawl {crawl_id} started at {context['ts']}")


def end_crawl_task(**context) -> None:
    """End of the crawl - final status update."""
    dag_run = context['dag_run']
    crawl_id = dag_run.conf.get('crawl_id')
    
    if not crawl_id:
        raise ValueError("crawl_id must be provided in DAG run configuration")
    
    mongo_db = get_mongo_client()
    
    # Update recurring crawl to Completed
    mongo_db.recurring_crawls.update_one(
        {"crawl_id": crawl_id},
        {
            "$set": {
                "status": CrawlStatus.COMPLETED.value,
                "completed_at": context['ts'],
                "updated_at": context['ts']
            }
        }
    )
    
    print(f"Crawl {crawl_id} completed at {context['ts']}")


# Define the DAG
dag = DAG(
    'main_crawl_dag',
    default_args=default_args,
    description='Main DAG for orchestrating web crawl workflow',
    schedule_interval=None,  # Triggered manually by scheduler
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['crawl', 'extraction', 'scraping'],
)

# Task 1: Start of the Crawl
start_task = PythonOperator(
    task_id='start_of_crawl',
    python_callable=start_crawl_task,
    dag=dag,
)

# Task 2: Create/Update PDP Docs
create_pdp_docs_task = PythonOperator(
    task_id='create_update_pdp_docs',
    python_callable=create_update_pdp_docs_task,
    dag=dag,
)

# Task 3: Add to Extractor Queue
add_to_extractor_queue = PythonOperator(
    task_id='add_to_extractor_queue',
    python_callable=add_to_extractor_queue_task,
    dag=dag,
)

# Task 4: Wait for Extractor to Complete
wait_for_extractor = PythonOperator(
    task_id='wait_for_extractor_to_complete',
    python_callable=wait_for_extractor_complete_task,
    dag=dag,
)

# Task 5: Wait for Crawlers to process extractor PDPs
wait_for_crawlers = PythonOperator(
    task_id='wait_for_crawlers_to_process_extractor_pdps',
    python_callable=wait_for_crawlers_complete_task,
    dag=dag,
)

# Task 6: End of the crawl
end_task = PythonOperator(
    task_id='end_of_crawl',
    python_callable=end_crawl_task,
    dag=dag,
)

# Define task dependencies
start_task >> create_pdp_docs_task >> add_to_extractor_queue >> wait_for_extractor >> wait_for_crawlers >> end_task
