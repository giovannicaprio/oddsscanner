<?php

namespace App\Interfaces;

interface CurrencyRateProvider
{
    /**
     * Fetches current currency rates
     * @return array Associative array of currency rates
     * @throws \Exception When unable to fetch rates
     */
    public function fetchCurrentRates(): array;
}
