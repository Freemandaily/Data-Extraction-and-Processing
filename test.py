import requests

moralis = "eyJub25jZSI6IjBmZjJiMGYxLTE4ZDctNDFkMi05OGM1LTllZmYxOTNmZDJmZSIsIm9yZ0lkIjoiMzU3MTg0IiwidXNlcklkIjoiMzY3MDk3IiwidHlwZSI6IlBST0pFQ1QiLCJ0eXBlSWQiOiJmYWQ3ZWQ2ZC0wODk0LTRiZjUtODBhNS0zZTQwYzZkMDZkODciLCJpYXQiOjE2OTQ3MTk5MDYsImV4cCI6NDg1MDQ3OTkwNn0"


url = f"https://solana-gateway.moralis.io/token/mainnet/pairs/{pair}/ohlcv?timeframe=5min&currency=usd&fromDate={from_date}&toDate={to_date}&limit=1000"

headers = {
"Accept": "application/json",
"X-API-Key": f"{moralis}"
}
  
response = requests.request("GET", url, headers=headers)
st.write(response.status_code)
