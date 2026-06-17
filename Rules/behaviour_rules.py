def behaviour_rule(tx, user_stats):
    user_id = tx.get('user_id')
    stats = user_stats.get(user_id)
    amount = stats['total_amount']
    count_stats = stats['count']

    if count_stats < 5:
        return None
    avg_amount = amount / count_stats
    if tx['amount'] > avg_amount * 10.0:
        return {
            'score': 40,
            'reason': 'Sudden hike in the transaction which is suspicious...'
        }

    return None
