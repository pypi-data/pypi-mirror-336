"""
Exchange rates for major world currencies.
This module contains default exchange rates for offline use.
"""

from typing import Dict

class ExchangeRates:

# Default exchange rates
    USD_RATES = {
        # Major currencies
        'EUR': 0.85,
        'GBP': 0.75,
        'JPY': 110.0,
        'CAD': 1.25,
        'AUD': 1.35,
        'CHF': 0.90,
        'CNY': 6.45,
        'INR': 75.0,
        'BRL': 5.20,
        'RUB': 75.0,
        'PLN': 3.90,
        
        # More European currencies
        'SEK': 8.50,  # Swedish Krona
        'NOK': 8.70,  # Norwegian Krone
        'DKK': 6.30,  # Danish Krone
        'CZK': 21.50,  # Czech Koruna
        'HUF': 300.0,  # Hungarian Forint
        'RON': 4.10,  # Romanian Leu
        'BGN': 1.65,  # Bulgarian Lev
        'HRK': 6.40,  # Croatian Kuna
        'ISK': 125.0,  # Icelandic Krona
        
        # Asian currencies
        'HKD': 7.80,  # Hong Kong Dollar
        'SGD': 1.35,  # Singapore Dollar
        'THB': 32.0,  # Thai Baht
        'KRW': 1150.0,  # South Korean Won
        'IDR': 14500.0,  # Indonesian Rupiah
        'PHP': 50.0,  # Philippine Peso
        'MYR': 4.20,  # Malaysian Ringgit
        'VND': 23000.0,  # Vietnamese Dong
        
        # Middle Eastern currencies
        'TRY': 8.50,  # Turkish Lira
        'ILS': 3.30,  # Israeli Shekel
        'AED': 3.67,  # UAE Dirham
        'SAR': 3.75,  # Saudi Riyal
        'QAR': 3.64,  # Qatari Riyal
        
        # North American currencies
        'MXN': 20.0,  # Mexican Peso
        
        # South American currencies
        'ARS': 95.0,  # Argentine Peso
        'CLP': 750.0,  # Chilean Peso
        'COP': 3800.0,  # Colombian Peso
        'PEN': 4.10,  # Peruvian Sol
        
        # African currencies
        'ZAR': 14.50,  # South African Rand
        'EGP': 15.70,  # Egyptian Pound
        'NGN': 410.0,  # Nigerian Naira
        'KES': 108.0,  # Kenyan Shilling
        'MAD': 9.0,  # Moroccan Dirham
        
        # Oceania currencies
        'NZD': 1.45,  # New Zealand Dollar
        'FJD': 2.05,  # Fijian Dollar
        
        # Crypto currencies (for fun)
        'BTC': 0.000025,  # Bitcoin
        'ETH': 0.00035,  # Ethereum
        
        # Base currency
        'USD': 1.0,
    }

    EUR_RATES = {
        # Major currencies
        'USD': 1.18,
        'GBP': 0.88,
        'JPY': 130.0,
        'CAD': 1.47,
        'AUD': 1.59,
        'CHF': 1.06,
        'CNY': 7.60,
        'INR': 88.5,
        'BRL': 6.12,
        'RUB': 88.0,
        'PLN': 4.59,
        
        # More European currencies
        'SEK': 10.0,  # Swedish Krona
        'NOK': 10.2,  # Norwegian Krone
        'DKK': 7.44,  # Danish Krone
        'CZK': 25.3,  # Czech Koruna
        'HUF': 355.0,  # Hungarian Forint
        'RON': 4.92,  # Romanian Leu
        'BGN': 1.96,  # Bulgarian Lev
        'HRK': 7.53,  # Croatian Kuna
        'ISK': 148.0,  # Icelandic Krona
        
        # Asian currencies
        'HKD': 9.2,  # Hong Kong Dollar
        'SGD': 1.59,  # Singapore Dollar
        'THB': 38.0,  # Thai Baht
        'KRW': 1350.0,  # South Korean Won
        'IDR': 17000.0,  # Indonesian Rupiah
        'PHP': 59.0,  # Philippine Peso
        'MYR': 4.95,  # Malaysian Ringgit
        'VND': 27000.0,  # Vietnamese Dong
        
        # Middle Eastern currencies
        'TRY': 10.0,  # Turkish Lira
        'ILS': 3.9,  # Israeli Shekel
        'AED': 4.33,  # UAE Dirham
        'SAR': 4.42,  # Saudi Riyal
        'QAR': 4.3,  # Qatari Riyal
        
        # North American currencies
        'MXN': 23.6,  # Mexican Peso
        
        # South American currencies
        'ARS': 113.0,  # Argentine Peso
        'CLP': 885.0,  # Chilean Peso
        'COP': 4500.0,  # Colombian Peso
        'PEN': 4.83,  # Peruvian Sol
        
        # African currencies
        'ZAR': 17.0,  # South African Rand
        'EGP': 18.5,  # Egyptian Pound
        'NGN': 485.0,  # Nigerian Naira
        'KES': 128.0,  # Kenyan Shilling
        'MAD': 10.6,  # Moroccan Dirham
        
        # Oceania currencies
        'NZD': 1.7,  # New Zealand Dollar
        'FJD': 2.42,  # Fijian Dollar
        
        # Crypto currencies (for fun)
        'BTC': 0.000021,  # Bitcoin
        'ETH': 0.00030,  # Ethereum
        
        # Base currency
        'EUR': 1.0,
    }

    GBP_RATES = {
        # Major currencies
        'USD': 1.33,
        'EUR': 1.14,
        'JPY': 146.67,
        'CAD': 1.67,
        'AUD': 1.80,
        'CHF': 1.20,
        'CNY': 8.60,
        'INR': 100.0,
        'BRL': 6.93,
        'RUB': 100.0,
        'PLN': 5.21,
        
        # More European currencies
        'SEK': 11.33,  # Swedish Krona
        'NOK': 11.60,  # Norwegian Krone
        'DKK': 8.40,  # Danish Krone
        'CZK': 28.67,  # Czech Koruna
        'HUF': 400.0,  # Hungarian Forint
        'RON': 5.47,  # Romanian Leu
        'BGN': 2.20,  # Bulgarian Lev
        'HRK': 8.53,  # Croatian Kuna
        'ISK': 166.67,  # Icelandic Krona
        
        # Asian currencies
        'HKD': 10.40,  # Hong Kong Dollar
        'SGD': 1.80,  # Singapore Dollar
        'THB': 42.67,  # Thai Baht
        'KRW': 1533.33,  # South Korean Won
        'IDR': 19333.33,  # Indonesian Rupiah
        'PHP': 66.67,  # Philippine Peso
        'MYR': 5.60,  # Malaysian Ringgit
        'VND': 30666.67,  # Vietnamese Dong
        
        # Middle Eastern currencies
        'TRY': 11.33,  # Turkish Lira
        'ILS': 4.40,  # Israeli Shekel
        'AED': 4.89,  # UAE Dirham
        'SAR': 5.0,  # Saudi Riyal
        'QAR': 4.85,  # Qatari Riyal
        
        # North American currencies
        'MXN': 26.67,  # Mexican Peso
        
        # South American currencies
        'ARS': 126.67,  # Argentine Peso
        'CLP': 1000.0,  # Chilean Peso
        'COP': 5066.67,  # Colombian Peso
        'PEN': 5.47,  # Peruvian Sol
        
        # African currencies
        'ZAR': 19.33,  # South African Rand
        'EGP': 20.93,  # Egyptian Pound
        'NGN': 546.67,  # Nigerian Naira
        'KES': 144.0,  # Kenyan Shilling
        'MAD': 12.0,  # Moroccan Dirham
        
        # Oceania currencies
        'NZD': 1.93,  # New Zealand Dollar
        'FJD': 2.73,  # Fijian Dollar
        
        # Crypto currencies
        'BTC': 0.000019,  # Bitcoin
        'ETH': 0.00027,  # Ethereum
        
        # Base currency
        'GBP': 1.0,
    }

    JPY_RATES = {
        # Major currencies
        'USD': 0.0091,
        'EUR': 0.0077,
        'GBP': 0.0068,
        'CAD': 0.0114,
        'AUD': 0.0123,
        'CHF': 0.0082,
        'CNY': 0.0586,
        'INR': 0.6818,
        'BRL': 0.0473,
        'RUB': 0.6818,
        'PLN': 0.0355,
        
        # More European currencies
        'SEK': 0.0773,  # Swedish Krona
        'NOK': 0.0791,  # Norwegian Krone
        'DKK': 0.0573,  # Danish Krone
        'CZK': 0.1955,  # Czech Koruna
        'HUF': 2.7273,  # Hungarian Forint
        'RON': 0.0373,  # Romanian Leu
        'BGN': 0.0150,  # Bulgarian Lev
        'HRK': 0.0582,  # Croatian Kuna
        'ISK': 1.1364,  # Icelandic Krona
        
        # Asian currencies
        'HKD': 0.0709,  # Hong Kong Dollar
        'SGD': 0.0123,  # Singapore Dollar
        'THB': 0.2909,  # Thai Baht
        'KRW': 10.4545,  # South Korean Won
        'IDR': 131.8182,  # Indonesian Rupiah
        'PHP': 0.4545,  # Philippine Peso
        'MYR': 0.0382,  # Malaysian Ringgit
        'VND': 209.0909,  # Vietnamese Dong
        
        # Middle Eastern currencies
        'TRY': 0.0773,  # Turkish Lira
        'ILS': 0.0300,  # Israeli Shekel
        'AED': 0.0334,  # UAE Dirham
        'SAR': 0.0341,  # Saudi Riyal
        'QAR': 0.0331,  # Qatari Riyal
        
        # North American currencies
        'MXN': 0.1818,  # Mexican Peso
        
        # South American currencies
        'ARS': 0.8636,  # Argentine Peso
        'CLP': 6.8182,  # Chilean Peso
        'COP': 34.5455,  # Colombian Peso
        'PEN': 0.0373,  # Peruvian Sol
        
        # African currencies
        'ZAR': 0.1318,  # South African Rand
        'EGP': 0.1427,  # Egyptian Pound
        'NGN': 3.7273,  # Nigerian Naira
        'KES': 0.9818,  # Kenyan Shilling
        'MAD': 0.0818,  # Moroccan Dirham
        
        # Oceania currencies
        'NZD': 0.0132,  # New Zealand Dollar
        'FJD': 0.0186,  # Fijian Dollar
        
        # Crypto currencies
        'BTC': 0.00000023,  # Bitcoin
        'ETH': 0.0000032,  # Ethereum
        
        # Base currency
        'JPY': 1.0,
    }

    PLN_RATES = {
        # Major currencies
        'USD': 0.256,
        'EUR': 0.218,
        'GBP': 0.192,
        'JPY': 28.21,
        'CAD': 0.321,
        'AUD': 0.346,
        'CHF': 0.231,
        'CNY': 1.654,
        'INR': 19.23,
        'BRL': 1.33,
        'RUB': 19.23,
        
        # More European currencies
        'SEK': 2.18,  # Swedish Krona
        'NOK': 2.22,  # Norwegian Krone
        'DKK': 1.62,  # Danish Krone
        'CZK': 5.51,  # Czech Koruna
        'HUF': 77.4,  # Hungarian Forint
        'RON': 1.07,  # Romanian Leu
        'BGN': 0.427,  # Bulgarian Lev
        'HRK': 1.64,  # Croatian Kuna
        'ISK': 32.3,  # Icelandic Krona
        
        # Asian currencies
        'HKD': 2.0,  # Hong Kong Dollar
        'SGD': 0.346,  # Singapore Dollar
        'THB': 8.28,  # Thai Baht
        'KRW': 295.0,  # South Korean Won
        'IDR': 3700.0,  # Indonesian Rupiah
        'PHP': 12.86,  # Philippine Peso
        'MYR': 1.08,  # Malaysian Ringgit
        'VND': 5900.0,  # Vietnamese Dong
        
        # Middle Eastern currencies
        'TRY': 2.18,  # Turkish Lira
        'ILS': 0.85,  # Israeli Shekel
        'AED': 0.94,  # UAE Dirham
        'SAR': 0.96,  # Saudi Riyal
        'QAR': 0.935,  # Qatari Riyal
        
        # North American currencies
        'MXN': 5.14,  # Mexican Peso
        
        # South American currencies
        'ARS': 24.6,  # Argentine Peso
        'CLP': 192.5,  # Chilean Peso
        'COP': 980.0,  # Colombian Peso
        'PEN': 1.05,  # Peruvian Sol
        
        # African currencies
        'ZAR': 3.71,  # South African Rand
        'EGP': 4.03,  # Egyptian Pound
        'NGN': 105.5,  # Nigerian Naira
        'KES': 27.85,  # Kenyan Shilling
        'MAD': 2.31,  # Moroccan Dirham
        
        # Oceania currencies
        'NZD': 0.37,  # New Zealand Dollar
        'FJD': 0.526,  # Fijian Dollar
        
        # Crypto currencies (for fun)
        'BTC': 0.0000046,  # Bitcoin
        'ETH': 0.000065,  # Ethereum
        
        # Base currency
        'PLN': 1.0,
    }

    # Complete dictionary of exchange rates
    DEFAULT_RATES = {
        'USD': {
            'base': 'USD',
            'rates': USD_RATES
        },
        'EUR': {
            'base': 'EUR',
            'rates': EUR_RATES
        },
        'GBP': {
            'base': 'GBP',
            'rates': GBP_RATES
        },
        'JPY': {
            'base': 'JPY',
            'rates': JPY_RATES
        },
        'PLN': {
            'base': 'PLN',
            'rates': PLN_RATES
        }
    }


    # Dictionary of currency names
    CURRENCY_NAMES = {
        # Major currencies
        'USD': 'US Dollar',
        'EUR': 'Euro',
        'GBP': 'British Pound',
        'JPY': 'Japanese Yen',
        'CAD': 'Canadian Dollar',
        'AUD': 'Australian Dollar',
        'CHF': 'Swiss Franc',
        'CNY': 'Chinese Yuan',
        'INR': 'Indian Rupee',
        'BRL': 'Brazilian Real',
        'RUB': 'Russian Ruble',
        'PLN': 'Polish Zloty',
        
        # More European currencies
        'SEK': 'Swedish Krona',
        'NOK': 'Norwegian Krone',
        'DKK': 'Danish Krone',
        'CZK': 'Czech Koruna',
        'HUF': 'Hungarian Forint',
        'RON': 'Romanian Leu',
        'BGN': 'Bulgarian Lev',
        'HRK': 'Croatian Kuna',
        'ISK': 'Icelandic Krona',
        
        # Asian currencies
        'HKD': 'Hong Kong Dollar',
        'SGD': 'Singapore Dollar',
        'THB': 'Thai Baht',
        'KRW': 'South Korean Won',
        'IDR': 'Indonesian Rupiah',
        'PHP': 'Philippine Peso',
        'MYR': 'Malaysian Ringgit',
        'VND': 'Vietnamese Dong',
        
        # Middle Eastern currencies
        'TRY': 'Turkish Lira',
        'ILS': 'Israeli Shekel',
        'AED': 'UAE Dirham',
        'SAR': 'Saudi Riyal',
        'QAR': 'Qatari Riyal',
        
        # North American currencies
        'MXN': 'Mexican Peso',
        
        # South American currencies
        'ARS': 'Argentine Peso',
        'CLP': 'Chilean Peso',
        'COP': 'Colombian Peso',
        'PEN': 'Peruvian Sol',
        
        # African currencies
        'ZAR': 'South African Rand',
        'EGP': 'Egyptian Pound',
        'NGN': 'Nigerian Naira',
        'KES': 'Kenyan Shilling',
        'MAD': 'Moroccan Dirham',
        
        # Oceania currencies
        'NZD': 'New Zealand Dollar',
        'FJD': 'Fijian Dollar',
        
        # Crypto currencies (for fun)
        'BTC': 'Bitcoin',
        'ETH': 'Ethereum',
    }


    @staticmethod
    def get_exchange_rate(from_currency: str, to_currency: str) -> float:
        """
        Get the exchange rate between two currencies.
        
        Args:
            from_currency (str): Currency to convert from
            to_currency (str): Currency to convert to
            
        Returns:
            float: Exchange rate (1 unit of from_currency in to_currency)
        """
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()
        
        # Same currency
        if from_currency == to_currency:
            return 1.0
        
        # Direct lookup from our rates
        if from_currency in ExchangeRates.DEFAULT_RATES:
            rates = ExchangeRates.DEFAULT_RATES[from_currency]['rates']
            if to_currency in rates:
                return rates[to_currency]
        
        # Try to calculate using USD as intermediary
        if from_currency in ExchangeRates.DEFAULT_RATES['USD']['rates'] and to_currency in ExchangeRates.DEFAULT_RATES['USD']['rates']:
            usd_from = ExchangeRates.DEFAULT_RATES['USD']['rates'][from_currency]
            usd_to = ExchangeRates.DEFAULT_RATES['USD']['rates'][to_currency]
            if usd_from != 0:  # Prevent division by zero
                return usd_to / usd_from
        
        # If we can't calculate the rate, return 1.0 (no conversion)
        return 1.0


    @staticmethod
    def get_all_currencies() -> Dict[str, str]:
        """
        Get a dictionary of all supported currencies.
        
        Returns:
            Dict[str, str]: Dictionary with currency codes as keys and names as values
        """
        return ExchangeRates.CURRENCY_NAMES.copy()


    @staticmethod
    def get_all_rates(base_currency: str) -> Dict[str, float]:
        """
        Get all exchange rates for a specific base currency.
        
    Args:
        base_currency (str): Base currency code
    
    Returns:
        Dict[str, float]: Dictionary of exchange rates
    """
        base_currency = base_currency.upper()
        
        if base_currency in ExchangeRates.DEFAULT_RATES:
            return ExchangeRates.DEFAULT_RATES[base_currency]['rates'].copy()
        
        # If currency is not directly available, calculate rates using USD as reference
        if base_currency in ExchangeRates.DEFAULT_RATES['USD']['rates']:
            usd_rate = ExchangeRates.DEFAULT_RATES['USD']['rates'][base_currency]
            if usd_rate != 0:  # Prevent division by zero
                rates = {}
                for curr, rate in ExchangeRates.DEFAULT_RATES['USD']['rates'].items():
                    rates[curr] = rate / usd_rate
                return rates
        
        # Fallback to USD rates
        return ExchangeRates.DEFAULT_RATES['USD']['rates'].copy()

