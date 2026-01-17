# Project Structure Overview

This document provides a detailed overview of the codebase structure and what needs to be implemented.

## 📂 Directory Structure

```
ApacheAirflowDemo/
├── src/                          # Main source code
│   ├── config/                   # Configuration management
│   │   ├── __init__.py
│   │   └── settings.py           # Application settings (✅ Complete)
│   │
│   ├── dags/                     # Airflow DAG definitions
│   │   ├── __init__.py
│   │   ├── main_dag.py          # Main crawl orchestration DAG (✅ Complete)
│   │   └── tasks/               # DAG task modules
│   │       ├── __init__.py
│   │       ├── extractor_tasks.py  # Extraction phase tasks (✅ Complete)
│   │       └── crawler_tasks.py    # Crawling phase tasks (✅ Complete)
│   │
│   ├── workers/                  # Worker processes
│   │   ├── __init__.py
│   │   ├── extractor/           # Extractor worker
│   │   │   ├── __init__.py
│   │   │   └── extractor_worker.py  # ⚠️ TODO: Implement _extract_pdp_urls_from_category
│   │   └── crawler/             # Crawler worker
│   │       ├── __init__.py
│   │       └── crawler_worker.py   # ⚠️ TODO: Implement scrape_pdp method
│   │
│   ├── schedulers/               # Scheduler processes
│   │   ├── __init__.py
│   │   ├── main_scheduler.py    # Main crawl scheduler (✅ Complete)
│   │   └── pdp_crawling_scheduler.py  # PDP queue scheduler (✅ Complete)
│   │
│   ├── api/                      # FastAPI application
│   │   ├── __init__.py
│   │   ├── main.py              # API endpoints (✅ Complete)
│   │   └── routes/               # Additional API routes
│   │       └── __init__.py
│   │
│   ├── ui/                       # Web UI components
│   │   ├── __init__.py
│   │   └── web_ui.py            # Web interface (✅ Complete)
│   │
│   ├── db/                       # Database layer
│   │   ├── __init__.py
│   │   ├── models/              # SQL models
│   │   │   ├── __init__.py
│   │   │   └── recurring_crawl.py  # RecurringCrawlModel (✅ Complete)
│   │   └── connections/         # DB connection handlers
│   │       ├── __init__.py
│   │       ├── sql_db.py        # PostgreSQL connection (✅ Complete)
│   │       └── mongo_db.py      # MongoDB connection (✅ Complete)
│   │
│   ├── queues/                   # Queue management
│   │   ├── __init__.py
│   │   └── queue_manager.py     # Redis queue handler (✅ Complete)
│   │
│   ├── schema/                   # Pydantic schemas
│   │   └── schemas.py           # Data validation schemas (✅ Complete)
│   │
│   └── utils/                    # Utility functions
│       ├── __init__.py
│       └── helpers.py           # Helper functions (✅ Complete)
│
├── airflow/                      # Airflow configuration
│   └── dags/                    # Airflow DAG files
│       └── main_crawl_dag.py    # DAG entry point (✅ Complete)
│
├── scripts/                      # Startup scripts
│   ├── start_api.py             # Start API server (✅ Complete)
│   ├── start_extractor_worker.py  # Start extractor worker (✅ Complete)
│   ├── start_crawler_worker.py    # Start crawler worker (✅ Complete)
│   ├── start_main_scheduler.py    # Start main scheduler (✅ Complete)
│   ├── start_pdp_scheduler.py     # Start PDP scheduler (✅ Complete)
│   └── init_db.py               # Initialize database (✅ Complete)
│
├── docs/                         # Documentation
│   └── AirflowDemoDesign.png    # System design diagram
│
├── .env.example                  # Environment variables template (✅ Complete)
├── .gitignore                   # Git ignore file (✅ Complete)
├── requirements.txt             # Python dependencies (✅ Complete)
├── setup.py                     # Package setup (✅ Complete)
└── README.md                    # Project documentation (✅ Complete)

```

## ✅ Completed Components

All boilerplate code has been created. The following components are ready to use:

1. **Configuration System** - Environment-based settings
2. **Database Layer** - SQL and MongoDB connections
3. **Queue Management** - Redis-based queue handlers
4. **Main DAG** - Complete workflow orchestration
5. **Schedulers** - Both main and PDP schedulers
6. **API** - RESTful endpoints for crawl management
7. **Web UI** - Beautiful interface for viewing data
8. **Schemas** - Complete Pydantic models
9. **Utility Functions** - Helper functions for common operations

## ⚠️ Implementation Required

The following methods need actual implementation:

### 1. Extractor Worker (`src/workers/extractor/extractor_worker.py`)

**Method:** `_extract_pdp_urls_from_category(category: str, crawl_id: str) -> List[str]`

**What to implement:**
- Navigate to the category page (Product Listing Page - PLP)
- Extract all Product Detail Page (PDP) URLs from the listing
- Return list of PDP URLs

**Example approach:**
```python
from playwright.sync_api import sync_playwright

def _extract_pdp_urls_from_category(self, category: str, crawl_id: str) -> List[str]:
    # Get category URL from crawl configuration
    category_url = f"{base_url}/{category}"
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(category_url)
        
        # Extract PDP URLs using selectors
        pdp_links = page.query_selector_all('a.product-link')
        pdp_urls = [link.get_attribute('href') for link in pdp_links]
        
        browser.close()
        return pdp_urls
```

### 2. Crawler Worker (`src/workers/crawler/crawler_worker.py`)

**Method:** `scrape_pdp(pdp_url: str, xpaths: Dict[str, str]) -> Dict[str, Any]`

**What to implement:**
- Navigate to the PDP URL
- Extract data using the provided xpaths
- Return extracted data dictionary

**Example approach:**
```python
from playwright.sync_api import sync_playwright

def scrape_pdp(self, pdp_url: str, xpaths: Dict[str, str]) -> Dict[str, Any]:
    extracted_data = {}
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(pdp_url)
        
        for field_name, xpath in xpaths.items():
            try:
                element = page.query_selector(xpath)
                if element:
                    extracted_data[field_name] = element.inner_text()
            except Exception as e:
                logger.warning(f"Failed to extract {field_name}: {e}")
        
        browser.close()
    
    return {"extracted_data": extracted_data, "scraper_details": {...}}
```

## 🚀 Next Steps

1. **Set up infrastructure:**
   - Install PostgreSQL, MongoDB, and Redis
   - Configure environment variables in `.env`
   - Run `python scripts/init_db.py` to create tables

2. **Implement scraping logic:**
   - Add your website-specific extraction logic in the Extractor Worker
   - Add your XPath-based scraping logic in the Crawler Worker

3. **Test the system:**
   - Start all services (workers, schedulers, API)
   - Create a test crawl via API
   - Monitor the workflow in Airflow UI

4. **Customize as needed:**
   - Adjust polling intervals
   - Add error handling
   - Implement retry logic
   - Add monitoring and logging

## 📝 Notes

- All imports use `from src.` which requires the `src` directory to be in the Python path
- Scripts automatically add `src` to the path
- Airflow DAGs also add `src` to the path
- The system is designed to be scalable - you can run multiple workers
- All components are decoupled and can be run independently
