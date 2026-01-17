"""Web UI for viewing scraped data."""
from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from typing import List, Optional
from src.db.connections.mongo_db import get_mongo_client
from src.schema.schemas import PDPDocument

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def read_scraped_data(
    crawl_id: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 100
):
    """Read data from mongo & render it in an attractive web page."""
    mongo_db = get_mongo_client()
    
    # Build query
    query = {}
    if crawl_id:
        query["crawl_id"] = crawl_id
    if category:
        query["category"] = category
    
    # Fetch PDP documents
    pdps = list(mongo_db.pdp_documents.find(query).limit(limit))
    
    # Generate HTML
    html_content = generate_html_page(pdps, crawl_id, category)
    
    return HTMLResponse(content=html_content)


def generate_html_page(pdps: List[dict], crawl_id: Optional[str] = None, 
                      category: Optional[str] = None) -> str:
    """Generate HTML page with scraped data."""
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Scraped Data Viewer</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 10px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                padding: 30px;
            }}
            h1 {{
                color: #333;
                margin-bottom: 10px;
                font-size: 2.5em;
            }}
            .stats {{
                display: flex;
                gap: 20px;
                margin-bottom: 30px;
                flex-wrap: wrap;
            }}
            .stat-card {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 8px;
                flex: 1;
                min-width: 200px;
            }}
            .stat-card h3 {{
                font-size: 0.9em;
                opacity: 0.9;
                margin-bottom: 10px;
            }}
            .stat-card .value {{
                font-size: 2em;
                font-weight: bold;
            }}
            .filters {{
                background: #f5f5f5;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 30px;
            }}
            .filters input, .filters select {{
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                margin-right: 10px;
                font-size: 14px;
            }}
            .filters button {{
                padding: 10px 20px;
                background: #667eea;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 14px;
            }}
            .filters button:hover {{
                background: #5568d3;
            }}
            .pdp-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 20px;
            }}
            .pdp-card {{
                background: #f9f9f9;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 20px;
                transition: transform 0.2s, box-shadow 0.2s;
            }}
            .pdp-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            }}
            .pdp-card h3 {{
                color: #667eea;
                margin-bottom: 10px;
                font-size: 1.2em;
            }}
            .pdp-card .url {{
                color: #666;
                font-size: 0.9em;
                margin-bottom: 15px;
                word-break: break-all;
            }}
            .pdp-card .status {{
                display: inline-block;
                padding: 5px 10px;
                border-radius: 20px;
                font-size: 0.8em;
                font-weight: bold;
                margin-bottom: 15px;
            }}
            .status.completed {{
                background: #4caf50;
                color: white;
            }}
            .status.processing {{
                background: #ff9800;
                color: white;
            }}
            .status.new {{
                background: #2196f3;
                color: white;
            }}
            .status.failed {{
                background: #f44336;
                color: white;
            }}
            .data-section {{
                margin-top: 15px;
            }}
            .data-section h4 {{
                color: #333;
                margin-bottom: 10px;
                font-size: 1em;
            }}
            .data-item {{
                padding: 8px;
                background: white;
                border-left: 3px solid #667eea;
                margin-bottom: 5px;
                border-radius: 3px;
            }}
            .data-item strong {{
                color: #667eea;
            }}
            .no-data {{
                text-align: center;
                padding: 60px 20px;
                color: #999;
            }}
            .no-data h2 {{
                font-size: 2em;
                margin-bottom: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 Scraped Data Viewer</h1>
            <div class="stats">
                <div class="stat-card">
                    <h3>Total PDPs</h3>
                    <div class="value">{len(pdps)}</div>
                </div>
                <div class="stat-card">
                    <h3>Completed</h3>
                    <div class="value">{sum(1 for pdp in pdps if pdp.get('status') == 'completed')}</div>
                </div>
                <div class="stat-card">
                    <h3>Processing</h3>
                    <div class="value">{sum(1 for pdp in pdps if pdp.get('status') == 'processing')}</div>
                </div>
                <div class="stat-card">
                    <h3>Failed</h3>
                    <div class="value">{sum(1 for pdp in pdps if pdp.get('status') == 'failed')}</div>
                </div>
            </div>
            
            <div class="filters">
                <form method="get" action="/">
                    <input type="text" name="crawl_id" placeholder="Crawl ID" value="{crawl_id or ''}">
                    <input type="text" name="category" placeholder="Category" value="{category or ''}">
                    <input type="number" name="limit" placeholder="Limit" value="{limit}" min="1" max="1000">
                    <button type="submit">Filter</button>
                </form>
            </div>
    """
    
    if not pdps:
        html += """
            <div class="no-data">
                <h2>📭 No Data Found</h2>
                <p>No scraped data available for the selected filters.</p>
            </div>
        """
    else:
        html += '<div class="pdp-grid">'
        for pdp in pdps:
            status = pdp.get('status', 'new')
            extracted_data = pdp.get('extracted_data', {})
            
            html += f"""
            <div class="pdp-card">
                <h3>PDP: {pdp.get('pdp_id', 'N/A')[:20]}...</h3>
                <div class="url">🔗 {pdp.get('pdp_url', 'N/A')}</div>
                <span class="status {status}">{status.upper()}</span>
                {f'<div style="margin-top: 10px;"><strong>Category:</strong> {pdp.get("category", "N/A")}</div>' if pdp.get("category") else ''}
            """
            
            if extracted_data:
                html += '<div class="data-section"><h4>Extracted Data:</h4>'
                for key, value in extracted_data.items():
                    html += f'<div class="data-item"><strong>{key}:</strong> {value}</div>'
                html += '</div>'
            
            if pdp.get('error_message'):
                html += f'<div style="margin-top: 10px; color: #f44336;"><strong>Error:</strong> {pdp.get("error_message")}</div>'
            
            html += '</div>'
        
        html += '</div>'
    
    html += """
        </div>
    </body>
    </html>
    """
    
    return html
