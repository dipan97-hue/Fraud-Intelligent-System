import pandas as pd

HIGH_RISK = ['Nigeria', 'Russia', 'Ukraine', 'Iran', 'North Korea', 'Sudan']

def build_features(tx):

    country_flag = (1 if tx['country'] in HIGH_RISK else 0)
    
    device_flag = (1 if tx['device'] == 'unknown_device' else 0)

    hour = (pd.to_datetime(tx['timestamp']).hour)

    return [tx['amount'], device_flag, country_flag, hour]
