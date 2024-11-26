Project Overview
The project is a web-based API that detects fraudulent credit card transactions. It uses a trained decision tree model to predict whether a given transaction is fraudulent or not based on transaction features like merchant, amount, category, and other relevant data.

Technologies Used
Flask: Web framework to create the API
Scikit-learn: For building and training the decision tree model
Joblib: For saving and loading the model, scaler, and encoder
Docker: Containerization of the application
Project Structure
bash
Copy code
├── templates/                  # HTML templates for the web interface
├── Dockerfile                  # Docker configuration file
├── app.py                      # Main Flask app for serving the API
├── decision_tree_saved.joblib   # Trained decision tree model
├── standard_scaler.joblib       # Scaler for feature normalization
├── woe_encoder.joblib           # Encoder for categorical features
├── requirements.txt            # Python dependencies
└── .gitattributes               # Git configuration file
Setup Instructions
Local Setup
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/credit-card-fraud-detection-api.git](https://github.com/nagarnikunj/Credit-Card-Fraud-Detection.git
cd credit-card-fraud-detection-api
Install dependencies: Make sure you have Python 3.8+ installed. Then, create a virtual environment and install the required packages:

bash
Copy code
python3 -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate     # For Windows
pip install -r requirements.txt
Run the app:

bash
Copy code
python app.py
Open your browser and go to http://127.0.0.1:5000 to access the API.

Using Docker
Build the Docker image:

bash
Copy code
docker build -t fraud-detection-api .
Run the Docker container:

bash
Copy code
docker run -p 5000:5000 fraud-detection-api
Open your browser and go to http://localhost:5000.

API Endpoints
1. POST /predict
This endpoint accepts transaction details as input and returns whether the transaction is fraudulent.

Input format (JSON):

json
Copy code
{
    "cc_num": "1234567812345678",
    "merchant": "fraud_Kirlin and Sons",
    "category": "personal_care",
    "amt": 2.86,
    "city": "Columbia",
    "job": "Mechanical engineer",
    "lat": 33.9659,
    "long": -80.9355,
    "merch_lat": 33.986391,
    "merch_long": -81.200714
}
Response:

json
Copy code
{
    "fraudulent": true,
    "confidence": 0.92
}
Example Usage
You can test the API using tools like curl or Postman:

bash
Copy code
curl -X POST http://localhost:5000/predict \
    -H "Content-Type: application/json" \
    -d '{"cc_num": "1234567812345678", "merchant": "fraud_Kirlin and Sons", "category": "personal_care", "amt": 2.86, "city": "Columbia", "job": "Mechanical engineer", "lat": 33.9659, "long": -80.9355, "merch_lat": 33.986391, "merch_long": -81.200714}'
Contributing
If you'd like to contribute to this project, please fork the repository and create a pull request.

License
This project is licensed under the EXL Company.
