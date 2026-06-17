from Rules.amount_rules import largeamount
from Rules.country_rules import check_country
from Rules.device_rules import check_device
from Rules.velocity_rules import velocity_rule
from Rules.behaviour_rules import behaviour_rule

def calculate_score(tx, history, user_locations, user_stats):

    score = 0
    reasons = []

    checks  = [
        largeamount(tx),
        check_country(tx, user_locations),
        check_device(tx),
        velocity_rule(tx, history),
        behaviour_rule(tx, user_stats)

    ]

    for result in checks:
        if result:
            score += result['score']

            reasons.append(result['reason'])
    return score, reasons