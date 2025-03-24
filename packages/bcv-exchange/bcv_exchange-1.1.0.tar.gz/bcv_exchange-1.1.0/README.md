# BCV_EXCHANGE

[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PyPI Version](https://img.shields.io/pypi/v/bcv-exchange)](https://pypi.org/project/bcv-exchange/)

Unofficial Python package to retrieve official exchange rates from the Central Bank of Venezuela (BCV) website.

## Features
- 📊 Real-time exchange rate data
- 🌐 Supports multiple currencies: USD, EUR, CNY, TRY, RUB
- 📅 Includes official update timestamp
- 🔄 Structured JSON output
- ⚠️ Automatic structure validation

## Installation
```bash
pip install bcv_exchange
```

## Usage
```python
from bcv_exchange import get_exchange_rate

try:
    exchange_data = get_exchange_rate()
    print(f"Source: {exchange_data['source']}")
    print(f"Last update: {exchange_data['date_of_change']}")
    print("Exchange Rates:")
    for currency, rate in exchange_data['exchange_rates'].items():
        print(f"{currency}: {rate:.2f} Bs")
except Exception as e:
    print(f"Error: {str(e)}")
```

## Output Example
```
Fecha de actualización: 2025-03-10 00:00:00-04:00
Tasas de cambio:
EUR: 70.91 Bs
CNY: 9.02 Bs
TRY: 1.79 Bs
RUB: 0.73 Bs
USD: 65.27 Bs
```

## License
This project is licensed under the MIT License - see the LICENSE file for details