import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
import yfinance as yf
from utils import create_sequences, split_data
import os

# Create 'results' directory if it doesn't exist
results_dir = 'results'
os.makedirs(results_dir, exist_ok=True)

# Download stock data
stock_data = yf.download('AAPL', start='2010-01-01', end='2023-10-01')

# Scale the data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(stock_data['Close'].values.reshape(-1, 1))

# Prepare the sequence data
seq_length = 60  # Sequence length for LSTM
X, y = create_sequences(scaled_data, seq_length)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = split_data(X, y, train_size=0.8)

# Define the path to save the trained model in the 'results' directory
model_path = os.path.join(results_dir, 'lstm_stock_model.h5')

# Check if a trained model already exists
if os.path.exists(model_path):
    print("Loading the trained model...")
    model = load_model(model_path)
else:
    print("Training a new model...")
    # Define the LSTM model
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
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
predictions = scaler.inverse_transform(predictions)  # Rescale predictions

# Rescale the actual test data
y_test_rescaled = scaler.inverse_transform(y_test)

# Plot the actual vs predicted stock prices
plt.plot(stock_data.index[len(stock_data) - len(y_test):], y_test_rescaled, color='blue', label='Actual Prices')
plt.plot(stock_data.index[len(stock_data) - len(predictions):], predictions, color='red', label='Predicted Prices')
plt.title('Stock Price Prediction')
plt.xlabel('Date')
plt.ylabel('Stock Price')
plt.legend()

# Save the plot in the 'results' directory
plot_path = os.path.join(results_dir, 'prediction_vs_actual.png')
plt.savefig(plot_path)
print(f"Plot saved to {plot_path}")
plt.show()