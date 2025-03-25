# BigBank

Really useless library that has no reason to exist !!!

## Installation
pip install bigbank

## Usage
```python
from bigbank import BigBank, CooldownError
import time

bank = BigBank()
while True:
    print(bank.get_balance())  # Check balance
    try:
        print(bank.generate_money())  # Earn money
    except CooldownError as e:
        print(e)
    time.sleep(1)
```