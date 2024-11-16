import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
import os
from utils import create_sequences, split_data

# Create 'results' directory if it doesn't exist
results_dir = 'results'
os.makedirs(results_dir, exist_ok=True)

# Load the red wine quality dataset
file_path = 'winequality-red.csv'  # Ensure the file is in the same directory or provide the full path
data = pd.read_csv(file_path)

# Select relevant features and the target variable
features = ['alcohol', 'pH', 'sulphates', 'residual sugar', 'volatile acidity']
X = data[features].values
y = data['quality'].values

# Scale the features
scaler = MinMaxScaler(feature_range=(0, 1))
X_scaled = scaler.fit_transform(X)

# Prepare the sequence data
seq_length = 5  # Sequence length for LSTM
X_seq, y_seq = create_sequences(X_scaled, y, seq_length)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = split_data(X_seq, y_seq, train_size=0.8)

# Define the path to save the trained model in the 'results' directory
model_path = os.path.join(results_dir, 'lstm_wine_quality_model.h5')

# Check if a trained model already exists
if os.path.exists(model_path):
    print("Loading the trained model...")
    model = load_model(model_path)
else:
    print("Training a new model...")
    # Define the LSTM model
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
    model.add(Dropout(0.2))

    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dropout(0.2))

    model.add(Dense(units=1))

    # Compile the model
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Train the model
    model.fit(X_train, y_train, epochs=20, batch_size=32)

    # Save the trained model in the 'results' directory
    model.save(model_path)
    print(f"Model saved to {model_path}")

# Make predictions
predictions = model.predict(X_test)

# Plot the actual vs predicted wine quality
plt.plot(range(len(y_test)), y_test, color='blue', label='Actual Quality')
plt.plot(range(len(predictions)), predictions, color='red', label='Predicted Quality')
plt.title('Wine Quality Prediction (Using Selected Features)')
plt.xlabel('Samples')
plt.ylabel('Quality')
plt.legend()

# Save the plot in the 'results' directory
plot_path = os.path.join(results_dir, 'wine_quality_prediction_selected_features.png')
plt.savefig(plot_path)
print(f"Plot saved to {plot_path}")
plt.show()
