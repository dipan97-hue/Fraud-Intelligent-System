from datetime import datetime, timezone
import random

def generate_transaction(user):

    amount = random.gauss(
        user['avg_amount'],
        user['avg_amount'] * 0.2
    )

    return {
        'user_id':user['user_id'],
        'amount':round(abs(amount), 2),
        'device': user['preferred_device'],
        'country': user['home_country'],
        'timestamp': datetime.now(timezone.utc).isoformat()
    }