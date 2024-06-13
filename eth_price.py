import requests

def get_eth_price():
    response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd')
    if response.status_code == 200:
        data = response.json()
        return data['ethereum']['usd']
    else:
        print("Error al obtener el precio de ETH")
        return None

def eth_to_usd(eth_amount, eth_price):
    return eth_amount * eth_price
