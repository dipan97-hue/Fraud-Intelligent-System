import json
from datetime import datetime
import time
from pathlib import Path
from kafka import KafkaProducer
import os 
from engine.user_profile import create_profile
from simulator.transaction_generator import generate_transaction 
import random
import sys 

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

users = create_profile()
producer = KafkaProducer(bootstrap_servers = 'localhost:9092', value_serializer=lambda x: json.dumps(x).encode('utf-8'))


### For testing purposes, we can generate a transaction that will trigger the fraud rules.
    # def generate_test_fraud(user):

    # return {
    # "user_id": user["user_id"],
    # "amount": 20000,
    # "country": "Nigeria",
    # "device": "unknown_device"
    # }
counter = 0

while True:

    user = random.choice(users)

    #user = users[0]  # For testing, we can use a specific user to generate predictable fraud patterns.

    counter += 1

    # Behavior Fraud
    if counter % 20 == 0:

        transaction = {

            "user_id": user["user_id"],

            "amount": random.choice([
                25000,
                35000,
                50000
            ]),

            "country": user["home_country"],

            "device": user["preferred_device"],

            "timestamp": datetime.now().isoformat(),

            "fraud_type": "behavior_spike"
        }

        print(" GENERATED BEHAVIOR FRAUD")

    # Country + Geo Fraud
    elif counter % 15 == 0:

        transaction = {

            "user_id": user["user_id"],

            "amount": random.randint(100, 1000),

            "country": random.choice([
                "Nigeria",
                "Sudan",
                "Iran",
                "kenya"
            ]),

            "device":user["preferred_device"],

            "timestamp":datetime.now().isoformat(),

            "fraud_type":"country_fraud"
        }

        print(" GENERATED COUNTRY FRAUD")

    # Device Fraud
    elif counter % 10 == 0:

        transaction = {

            "user_id": user["user_id"],

            "amount":random.randint(100,1000),

            "country": user["home_country"],

            "device": "unknown_device",

            "timestamp":datetime.now().isoformat(),

            "fraud_type":"device_fraud"
        }

        print(" GENERATED DEVICE FRAUD")

    else:

        transaction = generate_transaction(user)

    producer.send("transactions",transaction)

    print(f"Sent: {transaction}")

    time.sleep(1)