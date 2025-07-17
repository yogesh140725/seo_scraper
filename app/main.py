from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import os
from datetime import datetime

# Add the parent directory to Python path to import scraper modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from start_scraper import run_spider

app = FastAPI(
    title="SEO Scraper API",
    description="A FastAPI-based SEO scraper that extracts metadata from websites",
    version="1.0.0"
)


class ScrapeResponse(BaseModel):
    message: str
    url: str
    timestamp: str
    results: list = []


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "SEO Scraper API is running"}


@app.get("/scrape", response_model=ScrapeResponse)
async def scrape_website(url: str):
    """
    Scrape a website for SEO data
    
    Args:
        url: The URL to scrape (query parameter)
    
    Returns:
        JSON response with scraping status
    """
    if not url:
        raise HTTPException(status_code=400, detail="URL parameter is required")
    
    # Validate URL format (basic validation)
    if not url.startswith(('http://', 'https://')):
        raise HTTPException(status_code=400, detail="URL must start with http:// or https://")
    
    try:
        # Run the scraper directly (no longer async since we're not using Scrapy)
        results = run_spider(url)
        
        return ScrapeResponse(
            message=f"Scraping completed for {url}",
            url=url,
            timestamp=datetime.now().isoformat(),
            results=results
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 