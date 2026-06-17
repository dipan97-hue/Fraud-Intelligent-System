from config.config import supabase_key, supabase_url
import requests
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
## Storing the fraud alerts in database
def save_data(tx, score, reasons):
    url = f'{supabase_url}/rest/v1/alerts'

    headers = {
    "apikey": supabase_key,
    "Authorization": f"Bearer {supabase_key}",
    "Content-Type": "application/json",
    'Prefer':'return-minimal'}

    payload = {
        'user_id': tx.get('user_id'),
        'amount': tx.get('amount') or tx['amount'],
        'country': tx.get('country') or tx.get('home_country'),
        'score': score,
        'reasons': ','.join(map(str,reasons))
    }

    response = requests.post(url, headers=headers, json=payload)
    print(f'Response: {response.status_code} for alert save')

    if response.status_code not in [200,201]:
        print(response.text)

def save_transactions(tx,score,reasons, probability, final_score):
    url = f'{supabase_url}/rest/v1/transactions'

    headers = {
    "apikey": supabase_key,
    "Authorization": f"Bearer {supabase_key}",
    "Content-Type": "application/json", 
    'Prefer':'return-minimal'}

    payload = {
        'user_id': tx.get('user_id'),
        'amount': tx.get('amount') or tx['amount'],
        'country': tx.get('country') or tx.get('home_country'),
        'device': tx.get('device') or tx.get('preferred_device'),
        'risk_score': score,
        'fraud_detected': score >= 60,
        'reasons': ','.join(map(str,reasons)),
        'ml_probability': probability,
        'final_score': final_score

    }


    response = requests.post(url, headers=headers, json=payload)
    print(f'Response: {response.status_code} for transaction save')

    if response.status_code not in [200,201]:
        print(response.text)