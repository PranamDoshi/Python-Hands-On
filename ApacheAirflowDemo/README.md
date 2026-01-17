# Apache Airflow Web Crawling Pipeline

A comprehensive web crawling and data extraction system built with Apache Airflow, featuring automated recurring crawls, distributed workers, and a modern web interface.

## 🏗️ Architecture Overview

This project implements a distributed web scraping pipeline with the following components:

- **Main DAG**: Orchestrates the entire crawl workflow
- **Extractor Worker**: Processes category-level data extraction
- **Crawler Worker**: Scrapes Product Detail Pages (PDPs)
- **Schedulers**: Manage recurring crawls and PDP queue processing
- **API**: RESTful API for crawl management
- **Web UI**: Beautiful interface for viewing scraped data

## 📁 Project Structure

```
ApacheAirflowDemo/
├── src/
│   ├── config/              # Configuration settings
│   ├── dags/                # Airflow DAG definitions
│   │   ├── tasks/           # DAG task modules
│   │   └── main_dag.py     # Main crawl orchestration DAG
│   ├── workers/             # Worker processes
│   │   ├── extractor/       # Extractor worker
│   │   └── crawler/         # Crawler worker
│   ├── schedulers/          # Scheduler processes
│   ├── api/                 # FastAPI application
│   ├── ui/                  # Web UI components
│   ├── db/                  # Database models and connections
│   │   ├── models/          # SQL models
│   │   └── connections/     # DB connection handlers
│   ├── queues/              # Queue management
│   ├── schema/              # Pydantic schemas
│   └── utils/               # Utility functions
├── airflow/                 # Airflow configuration
│   └── dags/                # Airflow DAG files
├── scripts/                 # Startup scripts
└── docs/                    # Documentation

```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL
- MongoDB
- Redis
- Apache Airflow

### Installation

1. **Clone the repository and install dependencies:**

```bash
pip install -r requirements.txt
```

2. **Set up environment variables:**

```bash
cp .env.example .env
# Edit .env with your database and configuration settings
```

3. **Initialize the database:**

```bash
python scripts/init_db.py
```

4. **Start Airflow:**

```bash
# Initialize Airflow database
airflow db init

# Create an Airflow user
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin

# Start Airflow webserver
airflow webserver --port 8080

# Start Airflow scheduler (in another terminal)
airflow scheduler
```

5. **Start the workers and schedulers:**

```bash
# Terminal 1: Main Scheduler
python scripts/start_main_scheduler.py

# Terminal 2: PDP Crawling Scheduler
python scripts/start_pdp_scheduler.py

# Terminal 3: Extractor Worker
python scripts/start_extractor_worker.py

# Terminal 4: Crawler Worker
python scripts/start_crawler_worker.py
```

6. **Start the API server:**

```bash
python scripts/start_api.py
```

## 📖 Usage

### Creating a Recurring Crawl

Use the API to create a new recurring crawl:

```bash
curl -X POST "http://localhost:8000/api/crawls" \
  -H "Content-Type: application/json" \
  -d '{
    "website_url": "https://example.com",
    "frequency": "daily",
    "categories": ["electronics", "books"],
    "xpaths": {
      "title": "//h1[@class='product-title']",
      "price": "//span[@class='price']"
    }
  }'
```

### Viewing Scraped Data

Access the web UI at `http://localhost:8000/` to view scraped data with filtering options.

### API Endpoints

- `GET /api/crawls` - List all recurring crawls
- `GET /api/crawls/{crawl_id}` - Get a specific crawl
- `POST /api/crawls` - Create a new recurring crawl
- `PUT /api/crawls/{crawl_id}` - Update a crawl
- `DELETE /api/crawls/{crawl_id}` - Delete a crawl

## 🔄 Workflow

1. **Crawl Creation**: A recurring crawl is created via API and stored in SQL DB
2. **Scheduling**: Main Scheduler checks for due crawls and triggers the Main DAG
3. **Extraction**: Main DAG pushes tasks to Extractor Queue, Extractor Worker processes categories and creates PDP documents
4. **Crawling**: PDP Crawling Scheduler pushes new PDPs to Crawler Queue, Crawler Worker scrapes each PDP
5. **Completion**: Main DAG waits for all tasks to complete and updates status

## 🛠️ Development

### Implementing Extraction Logic

Edit `src/workers/extractor/extractor_worker.py` and implement the `_extract_pdp_urls_from_category` method with your scraping logic.

### Implementing Crawling Logic

Edit `src/workers/crawler/crawler_worker.py` and implement the `scrape_pdp` method with your XPath-based extraction logic.

## 📝 Configuration

All configuration is managed through environment variables (see `.env.example`). Key settings:

- Database connections (PostgreSQL, MongoDB)
- Queue settings (Redis)
- API host and port
- Scheduler intervals
- Worker poll intervals

## 🧪 Testing

```bash
pytest
```

## 📄 License

This is a demo project for educational purposes.

## 🤝 Contributing

This is a boilerplate structure. Implement the actual scraping logic based on your specific requirements.
