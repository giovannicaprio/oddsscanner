// API endpoints
const API_BASE_URL = '/api';
const ENDPOINTS = {
    welcome: `${API_BASE_URL}/welcome`,
    health: `${API_BASE_URL}/health`,
    time: `${API_BASE_URL}/time`,
    scrape: `${API_BASE_URL}/scrape`,
    download: `${API_BASE_URL}/download`
};

// Initial updates
updateWelcome();
updateHealth();

function updateWelcome() {
    document.getElementById('welcome-message').textContent = 'Welcome to BTC-EUR Price Tracker';
}

function updateHealth() {
    document.getElementById('health-status').textContent = 'System is healthy';
}

let isScrapingInProgress = false;

async function startScraping() {
    if (isScrapingInProgress) return;
    
    isScrapingInProgress = true;
    const scrapeButton = document.getElementById('scrape-button');
    const downloadButton = document.getElementById('download-button');
    const spinner = document.getElementById('loading-spinner');
    const progressContainer = document.getElementById('scraper-progress');
    const progressFill = document.getElementById('progress-fill');
    const progressText = document.getElementById('progress-text');
    const errorMessage = document.getElementById('error-message');
    const successMessage = document.getElementById('success-message');
    const previewContainer = document.getElementById('preview-container');
    const scraperMessage = document.getElementById('scraper-message');

    // Reset UI
    scrapeButton.disabled = true;
    downloadButton.disabled = true;
    spinner.style.display = 'block';
    progressContainer.style.display = 'block';
    errorMessage.style.display = 'none';
    successMessage.style.display = 'none';
    previewContainer.style.display = 'none';
    scraperMessage.textContent = 'Initializing scraper...';

    try {
        // Simulate progress
        let progress = 0;
        const progressInterval = setInterval(() => {
            if (progress < 90) {
                progress += 10;
                progressFill.style.width = `${progress}%`;
                progressText.textContent = `Processing... ${progress}%`;
            }
        }, 500);

        // Start scraping
        const response = await fetch('/api/scrape');
        const data = await response.json();

        clearInterval(progressInterval);

        if (data.success) {
            // Complete progress bar
            progressFill.style.width = '100%';
            progressText.textContent = 'Processing... 100%';
            
            // Show success message
            successMessage.textContent = 'Data successfully scraped!';
            successMessage.style.display = 'block';
            
            // Enable download button
            downloadButton.disabled = false;
            
            // Preview the data
            await updateDataPreview();
        } else {
            throw new Error(data.message || 'Failed to scrape data');
        }
    } catch (error) {
        console.error('Scraping error:', error);
        errorMessage.textContent = `Error: ${error.message}`;
        errorMessage.style.display = 'block';
        progressFill.style.backgroundColor = '#dc3545';
    } finally {
        isScrapingInProgress = false;
        scrapeButton.disabled = false;
        spinner.style.display = 'none';
        scraperMessage.textContent = 'Ready to scrape BTC-EUR data';
    }
}

async function updateDataPreview() {
    try {
        const response = await fetch('/api/download');
        const data = await response.text();
        
        // Parse CSV data
        const rows = data.split('\n').filter(row => row.trim());
        const headers = rows[0].split(',');
        const values = rows.slice(1);

        // Update preview table
        const tbody = document.querySelector('#data-preview tbody');
        tbody.innerHTML = '';
        
        values.forEach(row => {
            const [date, close] = row.split(',');
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${date}</td>
                <td>${close}</td>
            `;
            tbody.appendChild(tr);
        });

        document.getElementById('preview-container').style.display = 'block';
    } catch (error) {
        console.error('Error updating preview:', error);
    }
}

function downloadCSV() {
    const link = document.createElement('a');
    link.href = '/api/download';
    link.download = 'eur_btc_rates.csv';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Set up automatic refresh and event listeners
document.addEventListener('DOMContentLoaded', () => {
    // Initial update
    updateWelcome();
    updateHealth();
    
    // Set up scrape and download buttons
    document.getElementById('scrape-button').addEventListener('click', startScraping);
    document.getElementById('download-button').addEventListener('click', downloadCSV);
    
    // Initially disable download button until data is scraped
    document.getElementById('download-button').disabled = true;
}); 