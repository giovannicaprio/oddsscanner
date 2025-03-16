# Currency Exchange Rate Service

A PHP-based web application that fetches, stores, and displays currency exchange rates. The application uses the European Central Bank's daily reference rates and provides both current and historical exchange rate data.

## Features

- Fetches real-time currency exchange rates from ECB's XML feed
- Converts all rates to USD base for consistency
- Stores historical rates in CSV format
- Provides a clean web interface to view current and historical rates
- Handles API failures gracefully with fallback rates
- Includes comprehensive test coverage

## Requirements

- PHP 8.1 or higher
- Docker and Docker Compose
- SimpleXML PHP extension
- Composer (PHP package manager)

## Installation

1. Clone this repository:
2. Build and start the Docker containers:
```bash
docker-compose up -d --build
```

The application will be available at http://localhost:8080

## Project Structure

```
.
├── src/
│   ├── Core/           # Core framework classes
│   ├── Controllers/    # Application controllers
│   ├── Interfaces/     # Interface definitions
│   ├── Models/         # Data models
│   ├── Services/       # Business logic services
│   ├── Storage/        # Data storage handling
│   └── views/          # View templates
├── tests/              # PHPUnit test files
├── vendor/             # Composer dependencies
├── Dockerfile         
├── docker-compose.yml
└── composer.json
```

## Key Components

- `CurrencyService`: Fetches and processes exchange rates from ECB
- `FileStorageService`: Handles CSV storage of historical rates
- `RateManager`: Coordinates between services and provides rate management
- `HomeController`: Handles web interface and user interactions

## Running Tests

To run the test suite:

```bash
# Inside the Docker container
docker-compose exec php ./vendor/bin/phpunit

# Or from your local machine if PHP and dependencies are installed
./vendor/bin/phpunit
```

## API Integration

The application integrates with the European Central Bank's daily reference rates:
- Source: https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml
- Updates: Daily (except weekends and ECB holidays)
- Base Currency: EUR (converted to USD in application)

## Error Handling

The application includes robust error handling:
- API connection failures
- XML parsing errors
- Missing or invalid data
- File system errors

In case of API failures, the system falls back to sample rates to ensure continuous operation.

## Data Storage

Historical rates are stored in CSV format:
- Location: `storage/rates/`
- Format: `usd_currency_rates_YYYY-MM-DD.csv`
- Fields: Currency, Rate

## Development

To contribute to the project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write or update tests
5. Submit a pull request

## License

[Your License Here]

## Contact

[Your Contact Information] 