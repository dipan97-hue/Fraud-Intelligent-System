import joblib
model = joblib.load(r'D:\exercises\Projects\Fraud_Detection_Intelligent\ml\model.pkl')

def predict_fraud(features):
    probability = model.predict_proba([features])[0][1]

    return float(probability)

