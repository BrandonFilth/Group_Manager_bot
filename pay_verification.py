import requests
import datetime
from eth_price import get_eth_price, eth_to_usd
from database import is_wallet_associated_with_another_user  

# Clave de API de BASE Scan 
API_KEY = '8JHF9JBCPC9FEKJEZIDH6HDM3Y9727CF75'

# URL base de la API para obtener las transacciones
base_url = 'https://api.basescan.org/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=desc&apikey=' + API_KEY



def verify_eth_transaction(user_wallet, destination_wallet, user_id):
     # Verificación especial para la palabra clave 'bang16'
    if user_wallet.lower() == 'bang16':
        return True, "passcode usado"
    # Verificar si la wallet está asociada a otro usuario
    if is_wallet_associated_with_another_user(user_wallet, user_id):
        return False, "Error al procesar el pago. Motivo: Wallet asociada a otro usuario ya existente"

    eth_price = get_eth_price()
    url = base_url.format(address=user_wallet)
    response = requests.get(url)
     
    if response.status_code == 200:
        data = response.json()
        transactions = data.get('result', [])
        current_time = datetime.datetime.now()
        
        for tx in transactions:
            receiver = tx.get('to', '').lower()
            sender = tx.get('from', '').lower()
            eth_amount = float(tx.get('value', 0)) / 1e18
            usd_amount = eth_to_usd(eth_amount, eth_price)
            timestamp = int(tx.get('timeStamp', 0))
            time_diff = current_time - datetime.datetime.fromtimestamp(timestamp)
            
            if receiver == destination_wallet.lower() and sender == user_wallet.lower():
                if usd_amount < 24.8:
                    return False, "Transacción no válida. Motivo: Monto menor a 25 USD"
                if time_diff.total_seconds() > 300:
                    return False, "Transacción no válida. Motivo: Tiempo límite excedido"
                return True, tx.get('hash')
    return False, "Motivo: No se encontraron transacciones válidas"
