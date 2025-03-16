import os
from flask import Flask, jsonify, render_template, send_file, request
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pandas as pd
import logging

from .config import Config
from .scrapers.yahoo_finance_scraper import YahooFinanceScraper

def create_app():
    """Create and configure the Flask application."""
    # Load environment variables from .env files
    load_dotenv()
    
    # Create data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes
    
    # Configure the Flask application
    app.config.update(
        ENV=os.getenv('FLASK_ENV', 'production'),
        DEBUG=os.getenv('FLASK_DEBUG', '0') == '1',
        DATA_DIR=data_dir
    )

    config = Config()
    scraper = YahooFinanceScraper(config)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

    @app.route('/')
    def index():
        """Serve the main HTML page."""
        return render_template('index.html')

    @app.route('/api/welcome')
    def welcome():
        return jsonify({
            'message': 'Hello from Hot Reload! Try making more changes!',
            'status': 'success',
            'environment': app.config['ENV']
        })

    @app.route('/api/health')
    def health_check():
        """Health check endpoint."""
        return jsonify({
            'status': 'healthy',
            'service': 'python-docker',
            'environment': app.config['ENV']
        })

    @app.route('/api/time')
    def get_time():
        """Return the current day of the year."""
        current_date = datetime.now()
        return jsonify({
            'day': current_date.strftime('%j'),  # Day of year as decimal number (001-366)
            'date': current_date.strftime('%B %d, %Y')  # Month Day, Year format
        })

    @app.route('/api/scrape')
    def scrape():
        """Endpoint for full historical data scraping"""
        try:
            start_date = datetime.now()
            data = scraper.scrape_data(start_date)
            df = pd.DataFrame(data)
            df.to_csv(config.OUTPUT_FILE, index=False)
            
            return jsonify({
                'success': True,
                'message': 'Data scraped successfully'
            })
            
        except Exception as e:
            logger.error(f"Error during scraping: {str(e)}")
            return jsonify({
                'success': False,
                'error': str(e)
            })
        finally:
            scraper.cleanup()

    @app.route('/api/quick-scrape', methods=['POST'])
    def quick_scrape():
        """Endpoint for quick scraping of recent data"""
        try:
            data = request.get_json()
            if not data:
                raise ValueError("No JSON data received")
                
            start_date_str = data.get('start_date')
            logger.info(f"Received quick scrape request for date: {start_date_str}")
            
            if not start_date_str:
                logger.info("No date provided, using current date")
                start_date = None
            else:
                try:
                    # Parse the date string into a datetime object
                    start_date = datetime.strptime(start_date_str, config.DATE_FORMAT)
                    logger.info(f"Parsed date: {start_date}")
                except ValueError as e:
                    logger.error(f"Invalid date format: {str(e)}")
                    return jsonify({
                        'success': False,
                        'error': f"Invalid date format. Expected {config.DATE_FORMAT}"
                    })
            
            result = scraper.quick_scrape(target_date=start_date)
            logger.info(f"Scraping completed with success={result.success}")
            
            if result.success and result.data:
                df = pd.DataFrame(result.data)
                df.to_csv(config.OUTPUT_FILE, index=False)
            
            return jsonify(result.to_dict())
            
        except Exception as e:
            logger.error(f"Error during quick scrape: {str(e)}")
            return jsonify({
                'success': False,
                'error': str(e)
            })
        finally:
            scraper.cleanup()

    @app.route('/api/download')
    def download():
        """Endpoint for downloading scraped data"""
        try:
            return send_file(
                config.OUTPUT_FILE,
                mimetype='text/csv',
                as_attachment=True,
                download_name='btc_eur_history.csv'
            )
        except Exception as e:
            logger.error(f"Error downloading file: {str(e)}")
            return jsonify({
                'success': False,
                'error': str(e)
            })

    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return jsonify({
            'error': 'Not Found',
            'status': 404
        }), 404

    @app.errorhandler(500)
    def server_error(error):
        """Handle 500 errors."""
        return jsonify({
            'error': 'Internal Server Error',
            'status': 500
        }), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        use_reloader=True  # Enable hot reload
    ) 