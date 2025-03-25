# GWCModel Python SDK

A simple Python SDK for interacting with the GWC India API.

## Installation

```bash
pip install gwcmodel
```

## Usage Example

Here's a quick example demonstrating how to use the `gwcmodel` library:

```python
from gwcmodel.gwc import GWCModel

client = GWCModel(
    api_key="YOUR_API_KEY",
    access_token="YOUR_ACCESS_TOKEN"
)

print("profile")
profile = client.profile()
print(profile)

print("balance")
balance = client.balance()
print(balance)

print("positions")
positions = client.positions()
print(positions)

print("holdings")
holdings = client.holdings()
print(holdings)

print("orderbook")
orderbook = client.orderbook()
print(orderbook)

print("getquote")
getquote = client.getquote({
    "exchange": "NSE",
    "token": "11915"
})
print(getquote)
```
