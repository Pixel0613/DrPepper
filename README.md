# \[Wine Reccomender\]

### Team Members
- Alex Lee (Project Lead)
- Yuna Shin
- Donghyun Kim

### Project Description

Happy early Thanksgiving and Christmas 🥧🎄! With the holiday season approaching to us, our goal is to make a smart and personalized wine recommendation system that helps you to find the perfect bottle for your Thanksgiving gatherings, Christmas dinner, or festival celebrations! By using ML LSTM model and actual data from the vivino.com, our web recommends wine based on your taste preferences and budget, ensuring your holiday gatherings are unforgettable.

Whether you're hosting a Thanksgiving feast or searching for the perfect gift for a wine lover this Christmas, our Wine Recommendation System makes it easy to find the best wines tailored to your needs. Simply input your preferences for six key factors:

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
This is where you give instructions on how to run your project

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* npm (Node JS)
  ```sh
  npm install npm@latest -g
  ```

### Installation

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
   ```sh
   git clone https://github.com/your_username_/Project-Name.git
   ```
3. Install NPM packages
   ```sh
   npm install
   ```
4. Enter your API in `config.js`
   ```js
   const API_KEY = 'ENTER YOUR API';
   ```
## Demo
If your app is hosted on a published website, include the link here
