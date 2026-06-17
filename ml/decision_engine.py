def decision(rule_score, probability):

    ml_score = probability * 100

    final_score =(rule_score * 0.6 + ml_score * 0.4)

    return round(final_score, 2)
