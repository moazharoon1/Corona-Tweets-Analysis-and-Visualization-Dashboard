import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import psycopg2
import re

# Read the data from the PostgreSQL database
db_name = 'CoronaData'
db_user = 'postgres'
db_password = 'db_password'
db_host = 'localhost'
db_port = '5432'
table_name = 'corona_tweets'

# Create the database connection
conn = psycopg2.connect(
    dbname=db_name,
    user=db_user,
    password=db_password,
    host=db_host,
    port=db_port
)

# Query the data from the database
query = f'SELECT * FROM {table_name};'
df = pd.read_sql(query, conn)

# Close the database connection
conn.close()

# Convert 'TweetAt' column to datetime format
df['tweetat'] = pd.to_datetime(df['tweetat'])

# Calculate number of tweets per day
tweets_per_day = df.groupby(df['tweetat'].dt.date).size().reset_index(name='count')

# Convert 'tweetat' to datetime to ensure correct sorting
tweets_per_day['tweetat'] = pd.to_datetime(tweets_per_day['tweetat'])

# Sort tweets_per_day by date
tweets_per_day = tweets_per_day.sort_values(by='tweetat')

# Calculate cumulative sum of tweets over time
tweets_per_day['cumulative_count'] = tweets_per_day['count'].cumsum()

# Function to extract hashtags from tweet text
def extract_hashtags(tweet):
    return re.findall(r'#(\w+)', tweet)

# Extract hashtags from tweet text
df['hashtags'] = df['originaltweet'].apply(extract_hashtags)

# Create a list of all hashtags
all_hashtags = [hashtag for hashtags in df['hashtags'] for hashtag in hashtags]

# Count occurrences of each hashtag
hashtag_counts = pd.Series(all_hashtags).value_counts().reset_index()
hashtag_counts.columns = ['hashtag', 'count']

# Select top 60 hashtags
top_60_hashtags = hashtag_counts.head(60)

# Sort top_60_hashtags by count
top_60_hashtags = top_60_hashtags.sort_values(by='count', ascending=False)

# Filter hashtags_per_day to include only the top 60 hashtags
hashtags_per_day = df.explode('hashtags').groupby([df['tweetat'].dt.date, 'hashtags']).size().reset_index(name='count')
hashtags_per_day = hashtags_per_day[hashtags_per_day['hashtags'].isin(top_60_hashtags['hashtag'])]

# Select top 10 hashtags for the bar chart
top_10_hashtags = hashtag_counts.head(10)

# Create the Dash app
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1("Corona Tweets Dashboard"),
    dcc.Graph(id='tweets-over-time', figure=px.line(tweets_per_day, x='tweetat', y='count', title='Number of Tweets Over Time')),
    dcc.Graph(id='cumulative-tweets', figure=px.line(tweets_per_day, x='tweetat', y='cumulative_count', title='Cumulative Number of Tweets Over Time')),
    dcc.Graph(id='histogram', figure=px.histogram(df, x='sentiment', title='Sentiment Distribution')),
    dcc.Graph(id='bar-chart', figure=px.bar(df.groupby('location').size().reset_index(name='Count').sort_values(by='Count', ascending=False).head(10),
              x='location', y='Count', title='Top 10 Locations by Tweet Count')),
    dcc.Graph(id='top-10-hashtags', figure=px.bar(top_10_hashtags, x='hashtag', y='count', title='Top 10 Hashtags')),
    dcc.Graph(id='hashtags-over-time', figure=px.line(hashtags_per_day, x='tweetat', y='count', color='hashtags', title='Top 60 Hashtags Over Time'))
])

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
