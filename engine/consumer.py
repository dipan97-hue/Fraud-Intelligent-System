from datetime import datetime
import json
from pathlib import Path
from kafka import KafkaConsumer
from Rules.scoring import calculate_score
from engine.user_history import user_history, user_locations
from engine.user_stats import user_stats
from storage.db import save_data, save_transactions
from ml.decision_engine import decision
from ml.fraud_model import predict_fraud
from ml.features import build_features

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

def safe_json_loads(payload):
    if payload is None:
        return None

    decoded = payload.decode('utf-8').strip()
    if not decoded:
        return None

    try:
        return json.loads(decoded)
    except json.JSONDecodeError:
        return None



consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='fraud_detection_group',
    value_deserializer=safe_json_loads,
)

for messages in consumer:
    if messages.value is None:
        continue
    tx = messages.value

    user_id = tx['user_id']

    timestamp = datetime.fromisoformat(tx['timestamp'])


    user_history[user_id].append(timestamp)
    #print(f"Received: {messages.value}")

    user_stats[user_id]['count'] += 1
    user_stats[user_id]['total_amount'] += tx['amount']

    score, reasons = calculate_score(tx, user_history, user_locations, user_stats)
    user_locations[user_id] = tx.get('country') or tx.get('home_country')

    features = build_features(tx)
    probability = predict_fraud(features)
    final_score = decision(score, probability)


    if final_score >= 60:

        print('\n Fraud Alert! \n')
        print(f"Transaction: {tx}")
        print(f"Fraud Score: {final_score}")
        print(f"Reasons: {reasons}\n")
        print('-----------------------------')

        save_data(tx, final_score, reasons)
    else:
        print("Normal Transaction")
        print("Thank you!!!")

    save_transactions(tx, score, reasons, probability, final_score)