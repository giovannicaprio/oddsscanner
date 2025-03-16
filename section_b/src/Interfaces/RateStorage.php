<?php namespace App\Interfaces;

interface RateStorage
{
    /**
     * Save rates to a CSV file
     * @param array $rates Currency rates to save
     * @param string $date Date string for the filename
     * @return string The filename where rates were saved
     */
    public function saveRatesToCsv(array $rates, string $date): string;

    /**
     * Get rates from a specific file
     * @param string $filename The file to read rates from
     * @return array The rates from the file
     */
    public function getRatesFromFile(string $filename): array;

    public function getStoredFiles(): array;

    public function getDateFromFilename(string $filename): ?string;
}
