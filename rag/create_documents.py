import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import requests
import json
from config.config import supabase_url, supabase_key


headers = {
    "apikey": supabase_key,
    "Authorization": f"Bearer {supabase_key}"}

response = requests.get(f'{supabase_url}/rest/v1/alerts?select=*', headers=headers)

#print(response.status_code)
# if response.status_code == 200:
#     transactions = response.json()
#     #print(transactions)
# else:  pass #  print(f"Failed to fetch transactions: {response.status_code} - {response.text}")

transactions = response.json()
docs  = []
#'final_score':{tx['final_score']} or {tx.get('final_score')},
for tx in transactions:
    documents = f"""
        'transaction_amount': {tx['amount']},
        'country' : {tx.get('country')},
        'risk_score':{tx['score']} or {tx.get('score')},
         
        'reasons': {tx.get('reasons',0)}
    
    """

    docs.append(documents)
    
path = r'D:\exercises\Projects\Fraud_Detection_Intelligent\rag'
json_file = 'fraud_docs.json'
joinig_path = os.path.join(path, json_file)
print(joinig_path)
with open(joinig_path, 'w') as r:
    json.dump(docs, r, indent=2)

print(f'{len(docs)} created successfully ')
