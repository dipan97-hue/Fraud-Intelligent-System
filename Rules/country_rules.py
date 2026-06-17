high_risk_countries = ['Nigeria', 'Russia', 'Ukraine', 'Iran', 'North Korea', 'Sudan']

def check_country(tx, user_locations):
    current_country = tx.get('country') or tx.get('home_country')
    user_id = tx.get('user_id')
    previous_countries = user_locations.get(user_id)
    score = 0
    reasons = []
    if not current_country:
        return None
    # Rule 1 : High risk countries
    if current_country in high_risk_countries:
        score += 30
        reasons.append(f"Transaction from high risk country: {current_country}")

       
    # Rule 2: Geo Change - If the user has a history of transactions from one country and suddenly there's a transaction from a different country, it could be a sign of fraud.
    elif previous_countries!= current_country and previous_countries is not None:
        score += 20
        reasons.append(f"Transaction from new country: {current_country} (previous: {previous_countries})") 

    if score> 0:
        return {
            'score': score,
            'reason': (reasons)
        }
    return None