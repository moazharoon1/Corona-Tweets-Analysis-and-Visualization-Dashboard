# Corona-Tweets-Analysis-and-Visualization-Dashboard
Dash app visualizing Corona Tweets: daily counts, cumulative tweets, sentiment distribution, top locations, and top hashtags over time.


# Corona Tweets Dashboard

This project is a Dash application that visualizes data from a PostgreSQL database containing tweets about the Coronavirus. The dashboard provides insights through various visualizations, including the number of tweets over time, cumulative tweet counts, sentiment distribution, top tweeting locations, and trending hashtags.

## Features

- **Number of Tweets Over Time**: Line chart showing daily tweet counts.
- **Cumulative Number of Tweets Over Time**: Line chart displaying the cumulative tweet counts.
- **Sentiment Distribution**: Histogram showing the distribution of tweet sentiments.
- **Top 10 Locations by Tweet Count**: Bar chart highlighting the top 10 locations with the highest tweet counts.
- **Top 10 Hashtags**: Bar chart showing the top 10 most frequently used hashtags.
- **Top 60 Hashtags Over Time**: Line chart illustrating the usage trends of the top 60 hashtags over time.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/corona-tweets-dashboard.git
    ```

## Usage

1. Ensure your PostgreSQL database is running and accessible with the specified credentials.
2. Run the Dash app:
    ```bash
    python app.py
    ```
3. Open your web browser and go to `http://127.0.0.1:8050/` to view the dashboard.

