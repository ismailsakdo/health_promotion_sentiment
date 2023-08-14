#how to insert data from Google Sheets and make sentiment score

import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
import requests
from io import StringIO

# Google Sheet link
sheet_link = "https://docs.google.com/spreadsheets/d/1o6x1JAnSpyZFboIjNtLcxWKyhUJTvO9yxwEMY60kbmc/gviz/tq?tqx=out:csv"

# Fetch the data from Google Sheet
response = requests.get(sheet_link)
data = response.content.decode('utf-8')

# Create a DataFrame from the data
df = pd.read_csv(StringIO(data))
df 
# Perform sentiment analysis and add sentiment labels and scores to the DataFrame
def analyze_sentiment(text):
    sentiment = TextBlob(text).sentiment.polarity
    if sentiment > 0:
        return "Positive", sentiment
    elif sentiment < 0:
        return "Negative", sentiment
    else:
        return "Neutral", sentiment

# Apply sentiment analysis to the "Translate" column
df["Sentiment Label"], df["Sentiment Score"] = zip(*df["Translated"].apply(analyze_sentiment))

# Count the occurrences of each sentiment label
sentiment_counts = df["Sentiment Label"].value_counts()

# Plot a bar chart to visualize sentiment distribution
plt.figure(figsize=(8, 6))
bars = sentiment_counts.plot(kind="bar", color=["green", "red", "blue"], alpha=0.7)
plt.xlabel("Sentiment Label")
plt.ylabel("Frequency")
plt.title("Sentiment Distribution")
plt.xticks(rotation=0)

# Add labels to the bars
for p in bars.patches:
    bars.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='bottom', color='black', fontsize=10)

plt.tight_layout()

# Save the bar chart as a PNG image
chart_png_file = "sentiment_distribution.png"
plt.savefig(chart_png_file)

plt.show()

# Save the DataFrame with sentiment values to a CSV file
output_csv_file = "sentiment_analysis_with_values.csv"
df.to_csv(output_csv_file, index=False)

print(f"Sentiment analysis results saved to {output_csv_file}")
print(f"Sentiment distribution chart saved to {chart_png_file}")
