# frontend/app.py
import streamlit as st
import requests
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Social Media Analyzer", layout="wide")

BASE_URL = "https://social-media-analyzer-d2t0.onrender.com"

def main():
    st.title("Social Media Analytics Dashboard")
    
    # Sidebar controls
    st.sidebar.header("Controls")
    num_records = st.sidebar.slider("Number of Records", 50, 500, 100)
    
    if st.sidebar.button("Generate New Data"):
        response = requests.post(
            f"{BASE_URL}/generate-data",
            params={"num_records": num_records}
        )
        st.sidebar.success(response.json()["message"])
    
    # Main content
    if st.button("Analyze Data"):
        response = requests.get(f"{BASE_URL}/analyze")
        data = response.json()
        
        # Create multiple columns for different visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Temporal Patterns")
            # Convert temporal patterns to proper DataFrame format
            temporal_data = []
            for day, metrics in data["temporal_patterns"].items():
                metrics["day"] = day
                temporal_data.append(metrics)
            
            temporal_df = pd.DataFrame(temporal_data)
            
            # Create separate lines for each metric
            fig = px.line(temporal_df, 
                         x="day", 
                         y=["avg_likes", "avg_shares", "avg_comments"],
                         title="Average Engagement by Day",
                         labels={"value": "Count", "variable": "Metric"})
            st.plotly_chart(fig)
        
        with col2:
            st.subheader("Tag Performance")
            # Convert tag data to proper DataFrame format
            tag_data = []
            for tag, metrics in data["tag_co_occurrence"].items():
                metrics["tag"] = tag
                tag_data.append(metrics)
            
            tag_df = pd.DataFrame(tag_data)
            
            fig = px.bar(tag_df, 
                        x="tag", 
                        y=["avg_likes", "avg_shares", "avg_comments"],
                        title="Average Engagement by Tag",
                        barmode="group",
                        labels={"value": "Count", "variable": "Metric"})
            st.plotly_chart(fig)
        
        # Sentiment Analysis
        st.subheader("Sentiment Impact")
        sentiment_df = pd.DataFrame([data["sentiment_impact"]]).melt()
        fig = px.bar(sentiment_df, 
                     x="variable", 
                     y="value",
                     title="Average Likes by Sentiment",
                     labels={"value": "Average Likes", "variable": "Sentiment"})
        st.plotly_chart(fig)
        
        # Insights
        st.subheader("Generated Insights")
        st.write(data["insights"])

if __name__ == "__main__":
    main()