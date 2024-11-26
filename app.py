from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
from geopy.distance import great_circle
from category_encoders import WOEEncoder
from sklearn.preprocessing import StandardScaler
import joblib
import boto3
import joblib
import os

app = Flask(__name__)

# S3 Configuration
s3_client = boto3.client('s3')
bucket_name = 'fraud-models-bucket'

# Ensure the folder exists
local_dir = 'C:/Users/Aditya Bhateja/Downloads/Credit Card Fraud/'
os.makedirs(local_dir, exist_ok=True)

# Load the saved models and preprocessing objects
decision_tree_model = joblib.load('decision_tree_saved.joblib')
random_forest_model = joblib.load('random_forest_saved.joblib')
woe_encoder = joblib.load('woe_encoder.joblib')
scaler = joblib.load('standard_scaler.joblib')

def preprocess_single_sample(data):
    # Convert the input data to a DataFrame
    df = pd.DataFrame([data])

    # WOE encoding for categorical variables
    categorical_cols = ['city', 'job', 'merchant', 'category']
    df[categorical_cols] = woe_encoder.transform(df[categorical_cols])

    # Apply log transformation
    df['amt'] = np.log1p(df['amt'])

    # Select and order the required columns
    columns = ['cc_freq', 'cc_freq_class', 'city', 'job', 'age', 'gender_M', 'merchant', 'category',
               'distance_km', 'month', 'day', 'hour', 'hours_diff_bet_trans', 'amt']
    df = df[columns]

    # Scale the features
    df_scaled = scaler.transform(df)

    return df_scaled

@app.route('/')
def home():
    # Render the home.html template
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get data from the form
    data = {
        'cc_freq': int(request.form['cc_freq']),
        'cc_freq_class': int(request.form['cc_freq_class']),  # Ensure form sends integer
        'city': request.form['city'],
        'job': request.form['job'],
        'age': int(request.form['age']),
        'gender_M': int(request.form['gender_M']),
        'merchant': request.form['merchant'],
        'category': request.form['category'],
        'distance_km': float(request.form['distance_km']),
        'month': int(request.form['month']),
        'day': int(request.form['day']),
        'hour': int(request.form['hour']),
        'hours_diff_bet_trans': float(request.form['hours_diff_bet_trans']),
        'amt': float(request.form['amt'])
    }

    # Preprocess the data
    preprocessed_data = preprocess_single_sample(data)

    # Select the model
    model_choice = request.form['model_choice']
    if model_choice == 'Random Forest':
        model = random_forest_model
    else:
        model = decision_tree_model

    # Make prediction
    prediction = model.predict(preprocessed_data)

    # Return the result and render it on the HTML page
    prediction_text = f'Fraud Prediction: {"Fraudulent" if prediction[0] == 1 else "Not Fraudulent"}'
    
    return render_template('home.html', prediction_text=prediction_text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)

