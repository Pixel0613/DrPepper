import os
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

# Define file paths
catalog_file_path = 'wines.csv'  # Path to the wine catalog
model_path = 'results/lstm_wine_quality_model.h5'  # Path to the trained model
training_data_path = 'winequality-red.csv'  # Path to the training dataset

# Load the wine catalog
catalog = pd.read_csv(catalog_file_path)

# Debugging: Print catalog columns
print("Catalog Columns:", catalog.columns)

# Clean and convert 'Original Price' to numeric
catalog['Original Price'] = catalog['Original Price'].str.replace('$', '', regex=False)
catalog['Original Price'] = pd.to_numeric(catalog['Original Price'], errors='coerce')

# Handle rows with invalid price values
if catalog['Original Price'].isnull().any():
    print("Warning: Non-numeric values found in 'Original Price'. These rows will be dropped.")
    catalog = catalog.dropna(subset=['Original Price'])

# Ensure all values are now numeric
print("Cleaned and converted 'Original Price' to numeric.")

# Scale catalog ratings by 1.5
catalog['scaled_rating'] = catalog['Rating'] * 1.5

# Load the trained LSTM model
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Trained model not found at {model_path}. Please train the model first.")
model = load_model(model_path)

# Load and prepare the training dataset
training_data = pd.read_csv(training_data_path)
features = ['alcohol', 'pH', 'sulphates', 'residual sugar', 'volatile acidity']
scaler = MinMaxScaler(feature_range=(0, 1))  # Only scale the feature columns
X_scaled = scaler.fit_transform(training_data[features].values)

# Ensure target values (quality) remain in the original scale (1-10)
y = training_data['quality'].values  # Keep original range for training

def predict_and_recommend(user_input, price):
    """
    Predict wine quality and recommend similar wines from the catalog.

    Parameters:
    user_input (list): User-provided features [alcohol, pH, sulphates, residual sugar, volatile acidity].
    price (float): User-provided target price.

    Returns:
    tuple: Predicted rating and a DataFrame with the top 3 recommended wines.
    """
    # Scale the user input
    scaled_input = scaler.transform([user_input])
    scaled_input = np.expand_dims(scaled_input, axis=0)  # Add batch dimension
    
    # Predict the quality
    predicted_scaled_rating = model.predict(scaled_input)[0][0]

    # Reverse the scaling if the model's output is scaled (0-1) to the original range (1-10)
    min_quality = training_data['quality'].min()
    max_quality = training_data['quality'].max()
    predicted_rating = predicted_scaled_rating * (max_quality - min_quality) + min_quality

    # Find the closest matches in the catalog
    catalog['rating_diff'] = abs(catalog['scaled_rating'] - predicted_rating)
    catalog['price_diff'] = abs(catalog['Original Price'] - price)
    recommendations = catalog.sort_values(by=['rating_diff', 'price_diff']).head(3)
    
    return predicted_rating, recommendations[['Name', 'Original Price', 'scaled_rating']]

if __name__ == "__main__":
    # Collect user input
    print("Enter the wine characteristics:")
    try:
        alcohol = float(input("Alcohol: "))
        pH = float(input("pH: "))
        sulphates = float(input("Sulphates: "))
        residual_sugar = float(input("Residual Sugar: "))
        volatile_acidity = float(input("Volatile Acidity: "))
        price = float(input("Target Price: "))
    except ValueError:
        print("Invalid input. Please enter numeric values for all fields.")
        exit(1)
    
    user_features = [alcohol, pH, sulphates, residual_sugar, volatile_acidity]
    
    # Predict and recommend
    predicted_rating, recommendations = predict_and_recommend(user_features, price)
    
    # Display the results
    print(f"\nPredicted Wine Quality (original scale): {predicted_rating:.2f}")
    print("\nRecommended Wines:")
    print(recommendations.to_string(index=False))
