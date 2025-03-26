"""
Tests for the exchange_rates module.
"""

import unittest
import sys
import os
from pathlib import Path

# Add the parent directory to sys.path to import the package
parent_dir = str(Path(__file__).parent.parent)
sys.path.insert(0, parent_dir)

from currency_converter.repositories.exchange_rates import ExchangeRates
from currency_converter.converter.currency_converter import CurrencyConverter

class TestExchangeRates(unittest.TestCase):
    """Test cases for the exchange_rates module."""
    
    def test_get_exchange_rate_same_currency(self):
        """Test getting exchange rate between the same currency."""
        self.assertEqual(ExchangeRates.get_exchange_rate("USD", "USD"), 1.0)
        self.assertEqual(ExchangeRates.get_exchange_rate("EUR", "EUR"), 1.0)
        self.assertEqual(ExchangeRates.get_exchange_rate("PLN", "PLN"), 1.0)
    
    def test_get_exchange_rate_direct(self):
        """Test getting exchange rate with direct lookup."""
        # USD to other currencies
        self.assertEqual(ExchangeRates.get_exchange_rate("USD", "EUR"), 0.85)
        self.assertEqual(ExchangeRates.get_exchange_rate("USD", "PLN"), 3.90)
        
        # EUR to other currencies
        self.assertEqual(ExchangeRates.get_exchange_rate("EUR", "USD"), 1.18)
        self.assertEqual(ExchangeRates.get_exchange_rate("EUR", "PLN"), 4.59)
        
        # PLN to other currencies
        self.assertEqual(ExchangeRates.get_exchange_rate("PLN", "USD"), 0.256)
        self.assertEqual(ExchangeRates.get_exchange_rate("PLN", "EUR"), 0.218)
    
    def test_get_exchange_rate_case_insensitive(self):
        """Test that currency codes are case-insensitive."""
        self.assertEqual(ExchangeRates.get_exchange_rate("usd", "eur"), 0.85)
        self.assertEqual(ExchangeRates.get_exchange_rate("USD", "Eur"), 0.85)
        self.assertEqual(ExchangeRates.get_exchange_rate("pLn", "USD"), 0.256)
    
    def test_get_exchange_rate_via_usd(self):
        """Test getting exchange rate via USD as intermediary."""
        # Get the actual rate from the module
        aud_to_gbp_rate = ExchangeRates.get_exchange_rate("AUD", "GBP")
        
        # Check it's a reasonable value
        self.assertGreater(aud_to_gbp_rate, 0)
        self.assertLess(aud_to_gbp_rate, 10)
        
        # Verify we get the same value when calling it multiple times
        self.assertEqual(aud_to_gbp_rate, ExchangeRates.get_exchange_rate("AUD", "GBP"))
    
    def test_convert_currency_basic(self):
        """Test basic currency conversion."""
        # Same currency
        self.assertEqual(CurrencyConverter.convert_currency(100, "USD", "USD"), 100)
        
        # Different currencies
        self.assertEqual(CurrencyConverter.convert_currency(100, "USD", "EUR"), 85)
        self.assertEqual(CurrencyConverter.convert_currency(100, "EUR", "USD"), 118)
        self.assertEqual(CurrencyConverter.convert_currency(100, "PLN", "USD"), 25.6)
    
    def test_convert_currency_negative_amount(self):
        """Test conversion with negative amount raises ValueError."""
        with self.assertRaises(ValueError):
            CurrencyConverter.convert_currency(-100, "USD", "EUR")
    
    def test_get_all_currencies(self):
        """Test getting all supported currencies."""
        currencies = ExchangeRates.get_all_currencies()
        
        # Check it returns a copy, not the original reference
        self.assertIsNot(currencies, ExchangeRates.CURRENCY_NAMES)
        
        # Check some currency codes are present
        for code in ["USD", "EUR", "GBP", "PLN", "JPY", "BTC"]:
            self.assertIn(code, currencies)
        
        # Check some currency names are correct
        self.assertEqual(currencies["PLN"], "Polish Zloty")
        self.assertEqual(currencies["USD"], "US Dollar")
        self.assertEqual(currencies["BTC"], "Bitcoin")
    
    def test_get_all_rates_direct(self):
        """Test getting all rates for a currency that is directly available."""
        # Get rates for USD
        usd_rates = ExchangeRates.get_all_rates("USD")
        
        # Check it returns a copy, not the original reference
        self.assertIsNot(usd_rates, ExchangeRates.DEFAULT_RATES["USD"]["rates"])
        
        # Check some rates are correct
        self.assertEqual(usd_rates["EUR"], 0.85)
        self.assertEqual(usd_rates["PLN"], 3.90)
        self.assertEqual(usd_rates["USD"], 1.0)
        
        # Check PLN rates
        pln_rates = ExchangeRates.get_all_rates("PLN")
        self.assertEqual(pln_rates["USD"], 0.256)
        self.assertEqual(pln_rates["EUR"], 0.218)
        self.assertEqual(pln_rates["PLN"], 1.0)
    
    def test_get_all_rates_calculated(self):
        """Test getting all rates for a currency that needs calculation via USD."""
        # SGD is not a base currency, so rates should be calculated via USD
        sgd_rates = ExchangeRates.get_all_rates("SGD")
        
        # 1 SGD = 1/1.35 USD = 0.7407... USD
        # So 1 SGD = 0.7407... * 0.85 = 0.63 EUR
        expected_eur_rate = ExchangeRates.DEFAULT_RATES["USD"]["rates"]["EUR"] / ExchangeRates.DEFAULT_RATES["USD"]["rates"]["SGD"]
        self.assertAlmostEqual(sgd_rates["EUR"], expected_eur_rate, places=4)
        
        # SGD to USD should be 1/1.35 = 0.7407...
        expected_usd_rate = 1.0 / ExchangeRates.DEFAULT_RATES["USD"]["rates"]["SGD"]
        self.assertAlmostEqual(sgd_rates["USD"], expected_usd_rate, places=4)
        
        # SGD to SGD should always be 1.0
        self.assertEqual(sgd_rates["SGD"], 1.0)
    
    def test_get_all_rates_fallback(self):
        """Test getting rates for unknown currency falls back to USD rates."""
        # Make up a currency code that doesn't exist
        fake_rates = ExchangeRates.get_all_rates("XYZ")
        
        # Should fallback to USD rates
        self.assertEqual(fake_rates, ExchangeRates.DEFAULT_RATES["USD"]["rates"])
    
    def test_round_trip_conversion(self):
        """Test converting currency back and forth results in approximately the same amount."""
        original_amount = 100.0
        # USD -> EUR -> USD
        eur_amount = CurrencyConverter.convert_currency(original_amount, "USD", "EUR")
        usd_amount = CurrencyConverter.convert_currency(eur_amount, "EUR", "USD")
        # Allow for slight differences due to rate discrepancies
        self.assertAlmostEqual(usd_amount, original_amount, delta=1.0)
        
        # PLN -> USD -> PLN
        usd_amount = CurrencyConverter.convert_currency(original_amount, "PLN", "USD")
        pln_amount = CurrencyConverter.convert_currency(usd_amount, "USD", "PLN")
        self.assertAlmostEqual(pln_amount, original_amount, delta=1.0)


if __name__ == "__main__":
    unittest.main() 