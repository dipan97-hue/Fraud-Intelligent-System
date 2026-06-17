import random
from datetime import datetime

## Generate Amount Based Fraud Rules

def largeamount(tx):
    if tx['amount']> 10000:
        return {
            'score': 50,
            'reason': 'Large Amount Transaction'
        }
    
