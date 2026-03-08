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
        
        # --- SECTION 3: DATA PREVIEW & AUTOMATED SUMMARY ---
        st.divider()
        col_sum1, col_sum2 = st.columns([1, 2])
        
        with col2:
            st.write("### 📋 Analysis Summary")
            total_reviews = len(df)
            pos_count = len(df[df['analysis'] == 'Positive'])
            neu_count = len(df[df['analysis'] == 'Neutral'])
            neg_count = len(df[df['analysis'] == 'Negative'])
            pos_percent = (pos_count / total_reviews) * 100
        
            # Logic for the final recommendation
            if pos_percent > 70:
                conclusion = "Excellent performance. The product has high market approval."
                status_color = "green"
            elif pos_percent > 40:
                conclusion = "Average performance. Mixed reviews suggest specific areas need improvement."
                status_color = "orange"
            else:
                conclusion = "Critical alert. High negative sentiment detected; review product quality immediately."
                status_color = "red"
        
            st.markdown(f"""
            - **Total Reviews:** {total_reviews}
            - **Positive:** {pos_count} 😊
            - **Neutral:** {neu_count} 😐
            - **Negative:** {neg_count} 😡
            
            **System Conclusion:** :{status_color}[{conclusion}]
            """)
    else:
        st.error("Error: Could not find a 'review' or 'text' column in your CSV file.")
