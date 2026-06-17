def check_device(tx):
    if tx.get('device') == 'unknown_device':

        return {
            'score': 20,
            'reason': 'Device not listed and is not known...'
        }