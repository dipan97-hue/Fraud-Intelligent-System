import pandas as pd
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix
from pathlib import Path
import joblib
from sklearn.model_selection import train_test_split
import sys
import os
import warnings

warnings.filterwarnings('ignore')

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

df = pd.read_csv(r'D:\exercises\Projects\Fraud_Detection_Intelligent\Data\transactions.csv')
print(df.head())

features = ['amount','device_flag','country_flag','hour']
x = df[features]
y = df['fraud_detected']

X_train, X_test,y_train,y_test = train_test_split(x, y, random_state=42, stratify=y)
fraud = sum(y_train)
normals = len(y_train) - fraud
weight = normals / fraud
print(f"Class weight (normal/fraud): {weight}")


model = XGBClassifier(n_estimators = 100, max_depth = 4, learning_rate = 0.1, random_state = 42, eval_metric='logloss', scale_pos_weight=weight)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("Classification report!!!")

print(classification_report(y_test,predictions))
print('Confusion Matrix !!!')
print(confusion_matrix(y_test, predictions))

importance = pd.DataFrame({
    'Features': features,
    'Importance': model.feature_importances_ })

print("\nFeature Importance:\n")

print(importance.sort_values("Importance",ascending=False))

path = BASE_DIR / 'ml' / 'model.pkl'
path.parent.mkdir(parents=True, exist_ok=True)
joblib.dump(model, path)
print("Model saved!!!")
