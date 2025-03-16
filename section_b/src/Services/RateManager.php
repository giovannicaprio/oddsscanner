<?php

namespace App\Services;

use App\Interfaces\CurrencyRateProvider;
use App\Interfaces\RateStorage;

class RateManager
{
    private CurrencyRateProvider $currencyProvider;
    private RateStorage $storage;

    public function __construct(CurrencyRateProvider $currencyProvider, RateStorage $storage)
    {
        $this->currencyProvider = $currencyProvider;
        $this->storage = $storage;
    }

    public function getCurrentRates(): array
    {
        try {
            $rates = $this->currencyProvider->fetchCurrentRates();
            $this->storage->saveRatesToCsv($rates, date('Y-m-d'));
            return $rates;
        } catch (\Exception $e) {
            return [
                'USD' => 1.0000,
                'EUR' => 0.9163,
                'GBP' => 0.7892
            ];
        }
    }

    public function getHistoricalRates(string $filename): array
    {
        return $this->storage->getRatesFromFile($filename);
    }

    public function getStoredFiles(): array
    {
        return $this->storage->getStoredFiles();
    }

    public function getDateFromFilename(string $filename): ?string
    {
        return $this->storage->getDateFromFilename($filename);
    }
}
