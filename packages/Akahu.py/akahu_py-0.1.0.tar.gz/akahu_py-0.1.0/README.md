# akahu.py - An OOP wrapper for Akahu

An *unofficial* simple object oriented wrapper written in python for the Akahu open banking API.

# A simple example

```python
from akahu import akahu

akahu_client = akahu.Client("app_token", "user_token")

# Grabs all clients connected to your account
accounts = akahu_client.get_all_accounts()

# Look for chequing and savings accounts
for account in accounts:
    if account.name == "Chequing":
        chequing = account
    elif account.name == "Savings":
        savings = account

# Transfer money from chequing to savings
transfer = chequing.make_transfer(account.id, 100)
```

# Todo

- 100% API coverage. Currently Akahu.py doesn't support everything available via the Akahu API.
- Non-personal app support. I have only implemented support for personal "sandbox" accounts. This will do for most people wanting to play with Akahu, however limits scalability if you make something really cool and get an accredited Akahu app.
- Guardrails. Dealing with money programatically can be scary, implementing checks and balances is something that is certainly needed.
- Async.

# Contributing

All contributions are appreciated. Just make sure to try and stick to the OOP approach and everything will be sweet as!
