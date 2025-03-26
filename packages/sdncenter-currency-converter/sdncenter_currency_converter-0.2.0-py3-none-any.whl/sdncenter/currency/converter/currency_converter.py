from sdncenter.currency.repositories.exchange_rates import ExchangeRates

class CurrencyConverter:
    
    @staticmethod
    def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
        if amount < 0:
            raise ValueError("Amount must be a positive number")
        rate = ExchangeRates.get_exchange_rate(from_currency, to_currency)
        return amount * rate






