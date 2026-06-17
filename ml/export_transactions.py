from pathlib import Path
import pandas as pd
import sys
import os 
import requests
import json

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from config.config import supabase_url, supabase_key

HIGH_RISK = ['Nigeria', 'Russia', 'Ukraine', 'Iran', 'North Korea', 'Sudan']
def export_transactions():
    url = f'{supabase_url}/rest/v1/transactions?select=*'
    headers = {
            'apikey': supabase_key,
            'Authorization':f'Bearer {supabase_key}'
    }   


    response = requests.get(url, headers=headers)
    data = response.json()

    df = pd.DataFrame(data)
    if df.empty:
        print("No transactions returned from the API; nothing was written.")
        return df

    df['country_flag'] = (df['country'].isin(HIGH_RISK).astype(int))
    df['device_flag'] = (df['device'].eq('unknown_device').astype(int))
    df['hour'] = pd.to_datetime(df['created_at']).dt.hour
    print(df['fraud_detected'].value_counts())
    #print(df.head())
    output_path = BASE_DIR / 'Data' / 'transactions.csv'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Transactions exported to {output_path}")
    return df


if __name__ == '__main__':
    export_transactions()
