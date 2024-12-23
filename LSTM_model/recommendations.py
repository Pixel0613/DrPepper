import os
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

# Base Directory (Project Root) 
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # Go up one directory
LSTM_DIR = os.path.join(BASE_DIR, 'LSTM_model')  # Path to LSTM_model folder

# file paths for the trained data and wine catalogue
catalog_file_path = os.path.join(LSTM_DIR, 'wines.csv')  
training_data_path = os.path.join(LSTM_DIR, 'winequality-red.csv')
model_path = os.path.join(LSTM_DIR, 'results', 'lstm_wine_quality_model.h5')

# Load the wine catalog
if not os.path.exists(catalog_file_path):
    raise FileNotFoundError(f"Catalog file not found at {catalog_file_path}. Please check the file path.")
catalog = pd.read_csv(catalog_file_path)

# Clean and convert 'Current Price' to numeric values 
catalog['Current Price'] = pd.to_numeric(catalog['Current Price'], errors='coerce')

# Handle rows with invalid price values
if catalog['Current Price'].isnull().any():
    print("Warning: Non-numeric values found in 'Current Price'. These rows will be dropped.")
    catalog = catalog.dropna(subset=['Current Price'])

# Scale catalog ratings by 1.5 to match with the scales for the red wine data quality values
catalog['scaled_rating'] = catalog['Rating'] * 1.5

# Load the trained LSTM model
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Trained model not found at {model_path}. Please train the model first.")
model = load_model(model_path)

# Load and prepare the training dataset
if not os.path.exists(training_data_path):
    raise FileNotFoundError(f"Training data not found at {training_data_path}. Please check the file path.")
training_data = pd.read_csv(training_data_path)

features = ['alcohol', 'pH', 'sulphates', 'residual sugar', 'volatile acidity']
scaler = MinMaxScaler(feature_range=(0, 1))  # We'll only scale the columns of the features that we are using. 
X_scaled = scaler.fit_transform(training_data[features].values)

# Ensure target values (quality) remain in the original scale (1-10)
y = training_data['quality'].values  # Keep original range for training

def predict_and_recommend(user_input, price):
    """
    Predict the wine quality the user wants and recommend wines from the catalog.

    Parameters:
    user_input (list): User-provided features (alcohol, pH, sulphates, residual sugar, volatile acidity)
    price (float): User-provided target price --> Will find wines with the closest price 

    Returns:
    tuple: Predicted rating and a DataFrame with the top 3 recommended wines. --> Tie breakers are in the order of closest ratings, closest price, order in catalogue list
    """
    # Scale the user input
    scaled_input = scaler.transform([user_input])
    scaled_input = np.expand_dims(scaled_input, axis=0) 
    
    # Predict the quality of the wine 
    predicted_scaled_rating = model.predict(scaled_input)[0][0]

    # Reverse the scaling if the model's output is scaled (0-1) to the original range (1-10)
    min_quality = training_data['quality'].min()
    max_quality = training_data['quality'].max()
    predicted_rating = predicted_scaled_rating * (max_quality - min_quality) + min_quality

    # Find the closest matches in the catalog --> order of tie breakers are closest rating, closest price, and then order in list
    catalog['rating_diff'] = abs(catalog['scaled_rating'] - predicted_rating)
    catalog['price_diff'] = abs(catalog['Current Price'] - price)
    recommendations = catalog.sort_values(by=['rating_diff', 'price_diff']).head(3) #Recommend the top 3 values
    recommendations['scaled_rating'] = recommendations['scaled_rating'].round(2)  # Round rating value to the second decimal point 
    
    return predicted_rating, recommendations[['Wine Name', 'Current Price', 'scaled_rating']]

if __name__ == "__main__":
    # Example
    user_input = [9.3, 3.3, 1.08, 2.3, 0.43]  # Sample user input 
    target_price = 100.0
    predicted_rating, recommendations = predict_and_recommend(user_input, target_price)
    print(f"Predicted Rating: {predicted_rating}")
    print("Recommendations:")
    print(recommendations)
