import joblib

model = joblib.load(r'D:\exercises\Projects\Fraud_Detection_Intelligent\ml\model.pkl')

sample = [[50000, 1, 1, 2]] ## amount, device_flag, country_flag, hour

probability = model.predict_proba(sample)[0][0]

prediction = model.predict(sample)[0]
print(f"Predicted probability of fraud: {probability:.2f}")
print(f"Predicted class: {'Fraud' if prediction == 1 else 'Not Fraud'}")
