from flask import Flask, render_template, request, send_from_directory
import pandas as pd
import numpy as np
from LSTM_model.recommendations import predict_and_recommend  # Adjust import based on your folder

# Create Flask app
app = Flask(
    __name__,
    template_folder='Frontend/pages',  # HTML files are in Frontend/pages
    static_folder='Frontend/css_files'  # CSS files are in Frontend/css_files
)

@app.route('/')
def index():
    # Render the main index.html page
    return render_template('index.html')

@app.route('/submit-recommendations', methods=['POST'])
def submit_recommendations():
    # Retrieve form data
    alcohol = float(request.form['alcohol'])
    ph = float(request.form['ph'])
    sulphates = float(request.form['sulphates'])
    residual_sugar = float(request.form['residual_sugar'])
    volatile_acidity = float(request.form['volatile_acidity'])
    price = float(request.form['price'])

    # Run the model with user input
    user_features = [alcohol, ph, sulphates, residual_sugar, volatile_acidity]
    predicted_rating, recommendations = predict_and_recommend(user_features, price)

    # Pass the results to results.html
    return render_template(
        'results.html',
        predicted_rating=round(predicted_rating, 2),
        recommendations=recommendations.to_dict(orient='records')
    )

@app.route('/css/<path:filename>')
def css_files(filename):
    # Serve CSS files from the css_files folder
    return send_from_directory('Frontend/css_files', filename)

if __name__ == '__main__':
    app.run(debug=True)