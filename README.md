# \[Cantina Bella] 🍷
: Beautiful Cellar, Lovely Wine Cellar

### Team Members
- Alex Lee (Project Lead)
- Yuna Shin
- Donghyun Kim

### Project Description

Happy early Thanksgiving and Christmas 🥧🎄! With the holiday season approaching to us, our goal is to make a smart and personalized wine recommendation system that helps you to find the perfect bottle for your Thanksgiving gatherings, Christmas dinner, or festival celebrations! By using ML LSTM model and actual data from the vivino.com, our Cantina Bella recommends wine based on your taste preferences and budget, ensuring your holiday gatherings are unforgettable.

Whether you're hosting a Thanksgiving feast or searching for the perfect gift for a wine lover this Christmas, our Cantina Bella makes it easy to find the best wines tailored to your needs. Simply input your preferences for six key factors:

- Alcohol (%)
- pH Level
- Sulphates
- Residual Sugar (g/L)
- Volatile Acidity
- Target Price ($)

Based on your inputs, our system predicts your ideal wine quality score and provides three highly-rated wine recommendations, including names, prices, and ratings sourced from Vivino.


### Built With

- Python: The core logic and backend of our wine recommendation system are built using Python, leveraging its robust libraries and frameworks.
- HTML & CSS: The user interface is crafted using HTML and CSS to provide a clean and user-friendly experience, making it easy for users to input their preferences and view wine recommendations.
- LSTM Model: We utilized a Long Short-Term Memory (LSTM) model for the machine learning process to predict wine quality based on user inputs. This deep learning model excels in identifying patterns and delivering accurate quality scores.
- Flask: The Flask framework serves as the web application backend, seamlessly connecting the Python logic with the frontend. It handles user inputs, prediction processing, and dynamically displays results in the web interface.
- Playwright Web Scraper: For real-time wine recommendations, we use Playwright to scrape Vivino.com for wine details, including names, prices, and ratings, ensuring users receive the most relevant and up-to-date suggestions.


## Getting Started
All the steps you need to get your personalized wine recommendations

### Prerequisites
1. First, open your terminal and run this command: git clone https://github.com/Pixel0613/DrPepper
2. Second run the following command to install all the required dependencies: pip install -r requirements.txt
3. Now you can run the Cantina Bella by running the following command: python app.py

### How to use La Cantina Bella
Simply enter the the five wine attributes listed above with your designated price, and our model will create an estiamte of the quality of wine you want. 
You will be provided with three recommendations that closely match your designated quality and price. 
