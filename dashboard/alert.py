import os 
from pathlib import Path
import json
import sys
from urllib import response
import requests
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from config.config import supabase_url, supabase_key




def get_alert():
    url = f'{supabase_url}/rest/v1/alerts?select=*'
    headers = {
            'apikey': supabase_key,
            'Authorization':f'Bearer {supabase_key}' 
    }
    #print(url)
    
    response = requests.get(url, headers=headers)
    # print(response.status_code)
    # print(response.text)
    return response.json()

def extract_transactions():
        url = f'{supabase_url}/rest/v1/transactions?select=*'
        headers = {
            'apikey': supabase_key,
            'Authorization':f'Bearer {supabase_key}' 
    }
    #print(url)
    
        response = requests.get(url, headers=headers)
    # print(response.status_code)
    # print(response.text)
        return response.json()


    