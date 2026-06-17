from datetime import datetime, timedelta, timezone
import random


def _to_utc(dt):
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)

def velocity_rule(tx, history):

    current_time = _to_utc(datetime.fromisoformat(tx['timestamp']))

    history = history.get(tx['user_id'])

    if not history:
        return None

    recent = []

    for past_tx in history:

        if isinstance(past_tx, str):
            try:
                past_tx = datetime.fromisoformat(past_tx)
            except ValueError:
                continue

        if not isinstance(past_tx,datetime):
            continue

        past_tx = _to_utc(past_tx)

        if (current_time - past_tx < timedelta(minutes=1)):

            recent.append(past_tx)

    if len(recent)> 5:
        return {
            'score':30,
            'reason': 'Too many transactions in a short period of time'
        }
    return None