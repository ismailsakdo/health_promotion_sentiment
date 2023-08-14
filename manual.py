import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from textblob import TextBlob
import requests
from io import StringIO

# Function to perform sentiment analysis and add sentiment labels and scores
def analyze_sentiment(text):
    sentiment = TextBlob(text).sentiment.polarity
    if sentiment > 0:
        return "Positive", sentiment
    elif sentiment < 0:
        return "Negative", sentiment
    else:
        return "Neutral", sentiment

# Function to save sentiment analysis results and chart as files
def save_files(df, chart, output_dir):
    output_csv_file = f"{output_dir}/sentiment_analysis_with_values.csv"
    df.to_csv(output_csv_file, index=False)
    
    chart_png_file = f"{output_dir}/sentiment_distribution.png"
    chart.savefig(chart_png_file)
    
    return output_csv_file, chart_png_file

# Streamlit app
def main():
    st.title("Sentiment Analysis and Visualization")
    
    st.sidebar.header("Settings")
    base_sheet_link = "https://docs.google.com/spreadsheets/d/"
    sheet_id = st.sidebar.text_input("Enter Google Sheet ID")
    sheet_link = f"{base_sheet_link}{sheet_id}"
    
    if st.sidebar.button("Visualize Data"):
        try:
            response = requests.get(f"{sheet_link}/gviz/tq?tqx=out:csv")
            data = response.content.decode('utf-8')
            df = pd.read_csv(StringIO(data))
            st.write(df)
        except Exception as e:
            st.sidebar.error("Error fetching or visualizing data. Please check the link.")
    
    if st.sidebar.button("Analyze"):
        try:
            response = requests.get(f"{sheet_link}/gviz/tq?tqx=out:csv")
            data = response.content.decode('utf-8')
            df = pd.read_csv(StringIO(data))
            
            if len(df.columns) >= 3:
                df["Sentiment Label"], df["Sentiment Score"] = zip(*df.iloc[:, 2].apply(analyze_sentiment))
                
                st.header("Sentiment Analysis Results")
                st.write(df)
                
                st.header("Sentiment Distribution Chart")
                sentiment_counts = df["Sentiment Label"].value_counts()
                fig, ax = plt.subplots(figsize=(8, 6))
                bars = sentiment_counts.plot(kind="bar", color=["green", "red", "blue"], alpha=0.7, ax=ax)
                ax.set_xlabel("Sentiment Label")
                ax.set_ylabel("Frequency")
                ax.set_title("Sentiment Distribution")
                ax.set_xticklabels(sentiment_counts.index, rotation=0)
                for p in bars.patches:
                    ax.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='bottom', color='black', fontsize=10)
                st.pyplot(fig)
                
                output_dir = "output"
                
                if st.button("Download Sentiment Analysis Results"):
                    output_csv_file, _ = save_files(df, fig, output_dir)
                    st.download_button("Download", output_csv_file, label="Download CSV")
                
                if st.button("Download Sentiment Distribution Chart"):
                    _, chart_png_file = save_files(df, fig, output_dir)
                    st.download_button("Download", chart_png_file, label="Download PNG")
            else:
                st.error("There are not enough columns in the data to perform sentiment analysis.")
        except Exception as e:
            st.error("Error performing sentiment analysis. Please check the link and ensure valid data.")

if __name__ == "__main__":
    main()