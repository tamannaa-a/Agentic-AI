# train_fraud_model.py
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

os.makedirs('models', exist_ok=True)

# Synthetic dataset
np.random.seed(42)
N = 2000
claim_amount = np.random.exponential(scale=5000, size=N)
num_prior_claims = np.random.poisson(0.3, size=N)
days_since_policy_start = np.random.exponential(scale=365, size=N)
suspicious_keyword_count = np.random.poisson(0.2, size=N)

fraud_prob = (0.00005 * claim_amount) + (0.2 * suspicious_keyword_count) + (0.15 * (num_prior_claims>1).astype(float))
labels = (fraud_prob > 0.25).astype(int)

X = pd.DataFrame({
    'claim_amount': claim_amount,
    'num_prior_claims': num_prior_claims,
    'days_since_policy_start': days_since_policy_start,
    'suspicious_keyword_count': suspicious_keyword_count
})
y = labels

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = RandomForestClassifier(n_estimators=200, random_state=42)
clf.fit(X_train, y_train)

pred = clf.predict(X_test)
print(classification_report(y_test, pred))

joblib.dump(clf, 'models/fraud_model.joblib')
print('Saved model to models/fraud_model.joblib')
