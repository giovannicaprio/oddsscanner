<?php

namespace App\Services;

use App\Interfaces\RateStorage;

class FileStorageService implements RateStorage
{
    private string $storageDir;

    public function __construct(string $baseDir)
    {
        $this->storageDir = $baseDir . '/storage/rates/';
        if (!is_dir($this->storageDir)) {
            mkdir($this->storageDir, 0777, true);
        }
    }

    public function saveRatesToCsv(array $rates, string $date): string
    {
        $filename = "usd_currency_rates_{$date}.csv";
        $filepath = $this->storageDir . $filename;
        
        $file = fopen($filepath, 'w');
        fputcsv($file, ['Currency', 'Rate']);
        
        foreach ($rates as $currency => $rate) {
            fputcsv($file, [$currency, $rate]);
        }
        
        fclose($file);
        return $filename;
    }

    public function getRatesFromFile(string $filename): array
    {
        $filepath = $this->storageDir . $filename;
        if (!file_exists($filepath)) {
            throw new \Exception("File not found: {$filename}");
        }

        $rates = [];
        $file = fopen($filepath, 'r');
        
        // Skip header
        fgetcsv($file);
        
        while (($row = fgetcsv($file)) !== false) {
            $rates[$row[0]] = (float)$row[1];
        }
        
        fclose($file);
        return $rates;
    }

    public function getStoredFiles(): array
    {
        $files = glob($this->storageDir . "usd_currency_rates_*.csv");
        return array_map('basename', $files);
    }

    public function getDateFromFilename(string $filename): ?string
    {
        if (preg_match('/usd_currency_rates_(\d{4}-\d{2}-\d{2})\.csv/', $filename, $matches)) {
            return $matches[1];
        }
        return null;
    }
}
