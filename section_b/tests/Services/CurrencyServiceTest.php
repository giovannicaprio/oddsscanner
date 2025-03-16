<?php

namespace Tests\Services;

use PHPUnit\Framework\TestCase;
use App\Services\CurrencyService;

class CurrencyServiceTest extends TestCase
{
    private CurrencyService $currencyService;

    protected function setUp(): void
    {
        $this->currencyService = new class extends CurrencyService {
            protected function fetchXmlFromApi()
            {
                $sampleXml = <<<XML
<?xml version="1.0" encoding="UTF-8"?>
<gesmes:Envelope xmlns:gesmes="http://www.gesmes.org/xml/2002-08-01" xmlns="http://www.ecb.int/vocabulary/2002-08-01/eurofxref">
    <gesmes:subject>Reference rates</gesmes:subject>
    <gesmes:Sender>
        <gesmes:name>European Central Bank</gesmes:name>
    </gesmes:Sender>
    <Cube>
        <Cube time="2024-03-19">
            <Cube currency="USD" rate="1.0867"/>
            <Cube currency="JPY" rate="162.65"/>
            <Cube currency="GBP" rate="0.85520"/>
            <Cube currency="CHF" rate="0.9667"/>
            <Cube currency="AUD" rate="1.6573"/>
            <Cube currency="CAD" rate="1.4734"/>
        </Cube>
    </Cube>
</gesmes:Envelope>
XML;
                return simplexml_load_string($sampleXml);
            }
        };
    }

    public function testFetchCurrentRatesReturnsExpectedFormat()
    {
        $rates = $this->currencyService->fetchCurrentRates();

        $this->assertIsArray($rates);
        $this->assertArrayHasKey('USD', $rates);
        $this->assertEquals(1.0000, $rates['USD']);
        
        // Test other currencies are present and properly converted to USD base
        $expectedCurrencies = ['AUD', 'CAD', 'CHF', 'GBP', 'JPY', 'USD'];
        foreach ($expectedCurrencies as $currency) {
            $this->assertArrayHasKey($currency, $rates);
            $this->assertIsFloat($rates[$currency]);
        }
    }

    public function testFetchCurrentRatesCalculatesCorrectRates()
    {
        $rates = $this->currencyService->fetchCurrentRates();
        
        // Calculate expected rates based on EUR/USD rate of 1.0867
        $this->assertEquals(1.0000, $rates['USD']);
        $this->assertEqualsWithDelta(0.7870, $rates['GBP'], 0.001);
        $this->assertEqualsWithDelta(0.8896, $rates['CHF'], 0.001);
        $this->assertEqualsWithDelta(1.5251, $rates['AUD'], 0.001);
        $this->assertEqualsWithDelta(1.3558, $rates['CAD'], 0.001);
        $this->assertEqualsWithDelta(149.6735, $rates['JPY'], 0.001);
    }

    public function testFetchCurrentRatesWithApiFailure()
    {
        $currencyService = new class extends CurrencyService {
            protected function fetchXmlFromApi()
            {
                throw new \Exception("API failure");
            }
        };

        $rates = $currencyService->fetchCurrentRates();
        
        // Verify fallback to sample rates
        $this->assertIsArray($rates);
        $this->assertArrayHasKey('USD', $rates);
        $this->assertEquals(1.0000, $rates['USD']);
        $this->assertArrayHasKey('EUR', $rates);
        $this->assertArrayHasKey('GBP', $rates);
    }

    public function testFetchCurrentRatesWithMissingUsdRate()
    {
        $currencyService = new class extends CurrencyService {
            protected function fetchXmlFromApi()
            {
                $sampleXml = <<<XML
<?xml version="1.0" encoding="UTF-8"?>
<gesmes:Envelope xmlns:gesmes="http://www.gesmes.org/xml/2002-08-01" xmlns="http://www.ecb.int/vocabulary/2002-08-01/eurofxref">
    <Cube>
        <Cube time="2024-03-19">
            <Cube currency="JPY" rate="162.65"/>
            <Cube currency="GBP" rate="0.85520"/>
        </Cube>
    </Cube>
</gesmes:Envelope>
XML;
                return simplexml_load_string($sampleXml);
            }
        };

        $rates = $currencyService->fetchCurrentRates();
        
        // Verify fallback to sample rates when USD rate is missing
        $this->assertIsArray($rates);
        $this->assertArrayHasKey('USD', $rates);
        $this->assertEquals(1.0000, $rates['USD']);
    }
} 