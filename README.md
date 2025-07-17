# SEO Scraper API

A FastAPI-based SEO scraper that extracts metadata from websites using Scrapy and BeautifulSoup.

## Features

- **FastAPI** for the API interface
- **Scrapy** for crawling webpages
- **BeautifulSoup4** for HTML parsing
- **mysql-connector-python** for future database integration
- **scrapy-fake-useragent** for random user-agent rotation

## SEO Data Extracted

- Page title
- Meta description
- Meta keywords
- Canonical URL
- H1 tag count
- Total word count
- Total image count
- Images without alt text count

## Installation

1. **Clone or download the project**
2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the FastAPI Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

### API Endpoints

#### 1. Root Endpoint
```
GET /
```
Returns a simple status message.

#### 2. Scrape Endpoint
```
GET /scrape?url=https://example.com
```

**Parameters:**
- `url` (required): The website URL to scrape

**Response:**
```json
{
  "message": "Scraping started for https://example.com",
  "url": "https://example.com",
  "timestamp": "2023-11-15T10:30:00.123456"
}
```

#### 3. Health Check
```
GET /health
```
Returns the API health status.

### Running the Spider Directly

You can also run the spider directly from the command line:

```bash
python start_scraper.py https://example.com
```

## Project Structure

```
seo_scraper/
│
├── app/
│   └── main.py              # FastAPI entry point
│
├── scraper/
│   ├── __init__.py          # Package initialization
│   ├── items.py             # Scrapy item definition
│   └── seo_spider.py        # Scrapy spider logic
│
├── start_scraper.py         # Script to run spider from FastAPI
├── requirements.txt         # All required dependencies
├── .gitignore              # Git ignore file
└── README.md               # This file
```

## Example Usage

1. **Start the server:**
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Make a request:**
   ```bash
   curl "http://127.0.0.1:8000/scrape?url=https://example.com"
   ```

3. **View API documentation:**
   Visit `http://127.0.0.1:8000/docs` for interactive API documentation.

## Configuration

The spider is configured with:
- Random user-agent rotation
- 1-second download delay
- Cookies disabled
- Robots.txt compliance disabled

## Future Enhancements

- Database integration with MySQL
- Batch URL processing
- Export results to CSV/JSON
- Rate limiting
- Authentication
- Caching

## Troubleshooting

### Common Issues

1. **Import errors:** Make sure you're in the correct directory and virtual environment is activated.

2. **Permission errors:** On Windows, you might need to run PowerShell as Administrator.

3. **Port already in use:** Change the port in the uvicorn command:
   ```bash
   uvicorn app.main:app --reload --port 8001
   ```

### Dependencies

All required packages are listed in `requirements.txt`:
- fastapi==0.104.1
- uvicorn==0.24.0
- scrapy==2.11.0
- beautifulsoup4==4.12.2
- mysql-connector-python==8.2.0
- scrapy-fake-useragent==1.4.4
- lxml==4.9.3

## License

This project is open source and available under the MIT License. 