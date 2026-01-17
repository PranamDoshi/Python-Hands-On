"""FastAPI application for crawl management."""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from typing import List
from sqlalchemy.orm import Session
from src.db.connections.sql_db import get_sql_session
from src.db.models.recurring_crawl import RecurringCrawlModel
from src.schema.schemas import (
    RecurringCrawl,
    RecurringCrawlCreate,
    RecurringCrawlUpdate
)
from src.utils.helpers import generate_crawl_id, calculate_next_run_time
from src.config.settings import settings
from src.ui.web_ui import router as ui_router
from datetime import datetime

app = FastAPI(
    title="Crawl Management API",
    description="API for managing recurring web crawls",
    version="1.0.0"
)

# Include UI router
app.include_router(ui_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Crawl Management API", "version": "1.0.0"}


@app.post("/api/crawls", response_model=RecurringCrawl)
async def create_recurring_crawl(
    crawl_data: RecurringCrawlCreate,
    session: Session = Depends(get_sql_session)
):
    """Create new recurring crawl via API."""
    try:
        crawl_id = generate_crawl_id(crawl_data.website_url)
        next_run = calculate_next_run_time(crawl_data.frequency)
        
        crawl = RecurringCrawlModel(
            crawl_id=crawl_id,
            website_url=crawl_data.website_url,
            frequency=crawl_data.frequency.value,
            categories=crawl_data.categories,
            xpaths=crawl_data.xpaths,
            next_run_at=next_run,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        session.add(crawl)
        session.commit()
        session.refresh(crawl)
        
        return RecurringCrawl(**crawl.to_dict())
        
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating crawl: {str(e)}")


@app.get("/api/crawls", response_model=List[RecurringCrawl])
async def list_recurring_crawls(session: Session = Depends(get_sql_session)):
    """List all recurring crawls."""
    try:
        crawls = session.query(RecurringCrawlModel).all()
        return [RecurringCrawl(**crawl.to_dict()) for crawl in crawls]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing crawls: {str(e)}")


@app.get("/api/crawls/{crawl_id}", response_model=RecurringCrawl)
async def get_recurring_crawl(
    crawl_id: str,
    session: Session = Depends(get_sql_session)
):
    """Get a specific recurring crawl."""
    try:
        crawl = session.query(RecurringCrawlModel).filter_by(crawl_id=crawl_id).first()
        if not crawl:
            raise HTTPException(status_code=404, detail="Crawl not found")
        return RecurringCrawl(**crawl.to_dict())
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting crawl: {str(e)}")


@app.put("/api/crawls/{crawl_id}", response_model=RecurringCrawl)
async def update_recurring_crawl(
    crawl_id: str,
    crawl_data: RecurringCrawlUpdate,
    session: Session = Depends(get_sql_session)
):
    """Update a recurring crawl."""
    try:
        crawl = session.query(RecurringCrawlModel).filter_by(crawl_id=crawl_id).first()
        if not crawl:
            raise HTTPException(status_code=404, detail="Crawl not found")
        
        if crawl_data.frequency:
            crawl.frequency = crawl_data.frequency.value
        if crawl_data.categories is not None:
            crawl.categories = crawl_data.categories
        if crawl_data.xpaths is not None:
            crawl.xpaths = crawl_data.xpaths
        if crawl_data.status:
            crawl.status = crawl_data.status.value
        
        crawl.updated_at = datetime.now()
        session.commit()
        session.refresh(crawl)
        
        return RecurringCrawl(**crawl.to_dict())
        
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating crawl: {str(e)}")


@app.delete("/api/crawls/{crawl_id}")
async def delete_recurring_crawl(
    crawl_id: str,
    session: Session = Depends(get_sql_session)
):
    """Delete a recurring crawl."""
    try:
        crawl = session.query(RecurringCrawlModel).filter_by(crawl_id=crawl_id).first()
        if not crawl:
            raise HTTPException(status_code=404, detail="Crawl not found")
        
        session.delete(crawl)
        session.commit()
        
        return {"message": f"Crawl {crawl_id} deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting crawl: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)
