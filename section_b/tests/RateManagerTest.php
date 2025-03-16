<?php

namespace Tests;

use PHPUnit\Framework\TestCase;
use App\Services\RateManager;
use App\Interfaces\CurrencyRateProvider;
use App\Interfaces\RateStorage;

class RateManagerTest extends TestCase
{
    private $mockCurrencyProvider;
    private $mockStorage;
    private $rateManager;
    
    protected function setUp(): void
    {
        // Create mock objects
        $this->mockCurrencyProvider = $this->createMock(CurrencyRateProvider::class);
        $this->mockStorage = $this->createMock(RateStorage::class);
        
        // Create RateManager instance with mocks
        $this->rateManager = new RateManager(
            $this->mockCurrencyProvider,
            $this->mockStorage
        );
    }
    
    /**
     * @test
     */
    public function getCurrentRates_HappyPath_ReturnsCurrentRates()
    {
        // Arrange
        $expectedRates = [
            'USD' => 1.0000,
            'EUR' => 0.9163,
            'GBP' => 0.7892
        ];
        
        $this->mockCurrencyProvider
            ->expects($this->once())
            ->method('fetchCurrentRates')
            ->willReturn($expectedRates);
            
        $this->mockStorage
            ->expects($this->once())
            ->method('saveRatesToCsv')
            ->with($expectedRates, date('Y-m-d'))
            ->willReturn('usd_currency_rates_' . date('Y-m-d') . '.csv');
            
        // Act
        $actualRates = $this->rateManager->getCurrentRates();
        
        // Assert
        $this->assertEquals($expectedRates, $actualRates);
    }
    
    /**
     * @test
     */
    public function getHistoricalRates_WhenFileExists_ReturnsHistoricalRates()
    {
        // Arrange
        $filename = 'usd_currency_rates_2024-03-15.csv';
        $expectedRates = [
            'USD' => 1.0000,
            'EUR' => 0.9163,
            'GBP' => 0.7892
        ];
        
        $this->mockStorage
            ->expects($this->once())
            ->method('getRatesFromFile')
            ->with($filename)
            ->willReturn($expectedRates);
            
        // Act
        $actualRates = $this->rateManager->getHistoricalRates($filename);
        
        // Assert
        $this->assertEquals($expectedRates, $actualRates);
    }
    
    /**
     * @test
     */
    public function getCurrentRates_WhenExternalServiceFails_ReturnsSampleRates()
    {
        // Arrange
        $sampleRates = [
            'USD' => 1.0000,
            'EUR' => 0.9163,
            'GBP' => 0.7892
        ];
        
        $this->mockCurrencyProvider
            ->expects($this->once())
            ->method('fetchCurrentRates')
            ->willThrowException(new \Exception('External service error'));
            
        $this->mockStorage
            ->expects($this->never())
            ->method('saveRatesToCsv');
            
        // Act
        $actualRates = $this->rateManager->getCurrentRates();
        
        // Assert
        $this->assertIsArray($actualRates);
        $this->assertNotEmpty($actualRates);
        $this->assertArrayHasKey('USD', $actualRates);
        $this->assertEquals(1.0000, $actualRates['USD']);
    }
    
    /**
     * @test
     */
    public function getHistoricalRates_WhenFileNotFound_ThrowsException()
    {
        // Arrange
        $filename = 'non_existent_file.csv';
        
        $this->mockStorage
            ->expects($this->once())
            ->method('getRatesFromFile')
            ->with($filename)
            ->willThrowException(new \Exception('File not found'));
            
        // Assert & Act
        $this->expectException(\Exception::class);
        $this->rateManager->getHistoricalRates($filename);
    }
} 