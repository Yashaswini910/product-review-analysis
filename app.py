import streamlit as st
import pandas as pd
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="Product Review Analyzer", layout="wide")

st.title("📊 Product Review Sentiment Analyzer")
st.markdown("Analyze customer feedback instantly using Natural Language Processing.")

# --- SIDEBAR ---
st.sidebar.header("Instructions")
st.sidebar.info("Upload a CSV file with a column named 'review' or 'text' to see the dashboard.")

# --- OPTION 1: SINGLE REVIEW ANALYSIS ---
st.subheader("🔍 Analyze a Single Review")
user_input = st.text_area("Enter a product review here:")

if st.button("Analyze Sentiment"):
    if user_input:
        blob = TextBlob(user_input)
        sentiment_score = blob.sentiment.polarity
        
        if sentiment_score > 0:
            st.success(f"Positive Sentiment (Score: {sentiment_score:.2f}) 😊")
        elif sentiment_score < 0:
            st.error(f"Negative Sentiment (Score: {sentiment_score:.2f}) 😡")
        else:
            st.warning(f"Neutral Sentiment (Score: {sentiment_score:.2f}) 😐")
    else:
        st.write("Please enter some text first.")

st.divider()

# --- OPTION 2: BULK FILE UPLOAD ---
st.subheader("📂 Bulk Analysis via CSV Upload")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # Try to find the correct column automatically
    col_name = None
    for possible_col in ['review', 'text', 'content', 'comment']:
        if possible_col in df.columns:
            col_name = possible_col
            break;
            
    if col_name:
        # Perform Sentiment Analysis
        def get_sentiment(text):
            return TextBlob(str(text)).sentiment.polarity

        df['score'] = df[col_name].apply(get_sentiment)
        df['analysis'] = df['score'].apply(lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else 'Neutral'))
        # --- Visualizations Section ---
        st.write("### 📈 Sentiment Analytics Dashboard")
        
        # Create a fixed color mapping for consistency
        color_map = {'Positive': '#2ecc71', 'Neutral': '#95a5a6', 'Negative': '#e74c3c'}
        
        # Create two columns
        col1, col2 = st.columns(2)
        
        with col1:
            # Top of Column 1: Bar Chart
            st.write("#### 📊 Total Sentiment Volume")
            counts = df['analysis'].value_counts()
            # We use a standard bar chart, but the counts are already calculated
            st.bar_chart(counts)
            
            st.write("---") 
            
            # Bottom of Column 1: Word Cloud
            st.write("#### ☁️ Most Frequent Words")
            all_words = ' '.join([str(text) for text in df[col_name]])
            wordcloud = WordCloud(width=500, height=300, background_color='white').generate(all_words)
            
            fig_wc, ax_wc = plt.subplots()
            ax_wc.imshow(wordcloud, interpolation='bilinear')
            ax_wc.axis("off")
            st.pyplot(fig_wc)
        
        with col2:
            # Vertical spacing to center the Donut Chart
            st.write("##")
            st.write("##")
            
            st.write("#### 🍩 Sentiment Share (%)")
            sentiment_counts = df['analysis'].value_counts()
            
            # Ensure colors match the labels in the pie chart
            current_colors = [color_map[label] for label in sentiment_counts.index]
            
            fig, ax = plt.subplots()
            ax.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', 
                   startangle=140, pctdistance=0.85, colors=current_colors)
            
            # Add the center circle to make it a donut
            centre_circle = plt.Circle((0,0), 0.70, fc='white')
            fig.gca().add_artist(centre_circle)
            
            ax.axis('equal')  
            st.pyplot(fig)
        
      with col_sum1:
    st.write("### 📊 Executive Summary")
    
    # Calculate averages
    avg_polarity = df['score'].mean()
    # Subjectivity tells you if reviews are factual (0) or opinionated (1)
    df['subjectivity'] = df[col_name].apply(lambda x: TextBlob(str(x)).sentiment.subjectivity)
    avg_sub = df['subjectivity'].mean()

    # Create Metrics for a "Professional Dashboard" look
    m1, m2 = st.columns(2)
    m1.metric("Avg. Polarity", f"{avg_polarity:.2f}")
    m2.metric("Avg. Subjectivity", f"{avg_sub:.2f}")

    st.write("---")

    # Dynamic Interpretation
    if avg_polarity > 0.2:
        sentiment_label = "Positive"
        advice = "Maintain current quality and leverage positive testimonials in marketing."
    elif avg_polarity < -0.1:
        sentiment_label = "Negative"
        advice = "Urgent: Investigate common complaints in the 'Negative' filter to prevent churn."
    else:
        sentiment_label = "Neutral"
        advice = "The audience is indifferent. Consider adding 'wow' factors to the product."

    st.markdown(f"**Overall Sentiment:** `{sentiment_label}`")
    st.info(f"**Recommendation:** {advice}")
        
            with col_sum2:
                st.write("### 📄 Processed Data Preview")
                st.dataframe(df.head(10), use_container_width=True)
                
                # Download Button
                csv_data = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Analyzed Results",
                    data=csv_data,
                    file_name="sentiment_analysis_results.csv",
                    mime="text/csv"
                )
        else:
            st.warning("The uploaded file contains no data rows.")
