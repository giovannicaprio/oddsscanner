# BTC-EUR Price Scraper

A web application that scrapes Bitcoin to Euro (BTC-EUR) price data from Yahoo Finance, providing both historical and recent price information through a user-friendly interface.

## Features

- Real-time BTC-EUR price data scraping from Yahoo Finance
- Quick scrape functionality for recent prices (last 10 days)
- Historical data scraping capability
- Date-based filtering
- CSV export functionality
- Modern web interface with date picker
- RESTful API endpoints
- Docker containerization for easy deployment

## Prerequisites

- Docker and Docker Compose
- Python 3.8 or higher (if running without Docker)
- Chrome/Chromium browser (for the web driver)
- Node.js and npm (for frontend development)

## Installation

### Using Docker (Recommended)

1. Clone the repository:

2. Create a `.env` file in the project root:
```bash
FLASK_ENV=development
FLASK_DEBUG=1
PORT=5000
CHROMIUM_PATH=/usr/bin/chromium
CHROME_DRIVER_PATH=/usr/bin/chromedriver
```

3. Build and start the containers:
```bash
docker-compose up --build
```

The application will be available at `http://localhost:5000`

### Manual Installation

1. Clone the repository and create a virtual environment:
```bash
git clone <repository-url>
cd <project-directory>
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
export PORT=5000
export CHROMIUM_PATH=/path/to/chromium
export CHROME_DRIVER_PATH=/path/to/chromedriver
```

4. Run the application:
```bash
python -m flask run
```

## Project Structure

```
.
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── src/
│   ├── app.py                 # Flask application
│   ├── config.py              # Configuration settings
│   ├── templates/             # HTML templates
│   ├── static/                # Static files (CSS, JS)
│   └── scrapers/             # Scraping modules
│       ├── base_scraper.py
│       ├── web_driver.py
│       ├── date_filter.py
│       ├── models.py
│       └── yahoo_finance_scraper.py
└── data/                      # Scraped data storage
```

## API Endpoints

- `GET /`: Main web interface
- `GET /api/health`: Health check endpoint
- `GET /api/time`: Current time information
- `POST /api/quick-scrape`: Quick scrape for recent prices
- `GET /api/scrape`: Full historical data scrape
- `GET /api/download`: Download scraped data as CSV

## Usage

1. Access the web interface at `http://localhost:5000`
2. Use the date picker to select a target date
3. Click "Quick Scrape" to fetch the last 10 days of prices from the selected date
4. Click "Download CSV" to export the data
5. Use "Full Scrape" for historical data (may take longer)

## Error Handling

- The application includes comprehensive error handling and logging
- Check the console/logs for detailed information about any issues
- Common errors (invalid dates, connection issues) are handled gracefully

## Development

- The project uses Flask's debug mode for development
- Hot reload is enabled for quick development iterations
- Logs provide detailed information about the scraping process
- CORS is enabled for frontend development

## Security Notes

- The application runs in a containerized environment
- Sensitive configurations should be managed through environment variables
- API endpoints include basic error handling and input validation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Add your license information here]