<?php

namespace App\Controllers;

use App\Core\Controller;
use App\Services\CurrencyService;
use App\Services\FileStorageService;
use App\Services\RateManager;

class HomeController extends Controller {
    private $rateManager;

    public function __construct() {
        $currencyService = new CurrencyService();
        $fileStorage = new FileStorageService(__DIR__ . '/..');
        $this->rateManager = new RateManager($currencyService, $fileStorage);
    }

    public function index() {
        $selectedFile = $_GET['file'] ?? null;
        $rates = [];
        $rateDate = 'Current';
        
        if ($selectedFile) {
            try {
                $rates = $this->rateManager->getHistoricalRates($selectedFile);
                $rateDate = $this->rateManager->getDateFromFilename($selectedFile);
            } catch (Exception $e) {
                $rates = $this->rateManager->getCurrentRates();
            }
        } else {
            $rates = $this->rateManager->getCurrentRates();
        }
        
        $storedFiles = $this->rateManager->getStoredFiles();
        
        $data = [
            'title' => 'Currency Rates (USD Base)',
            'rates' => $rates,
            'rateDate' => $rateDate,
            'lastUpdate' => date('Y-m-d H:i:s'),
            'storedFiles' => $storedFiles,
            'selectedFile' => $selectedFile
        ];
        
        $this->render('home/index', $data);
    }
} 