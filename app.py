import streamlit as st
import pandas as pd
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# --- HELPER FUNCTIONS ---
def get_sentiment_label(score):
    if score > 0:
        return 'Positive'
    elif score < 0:
        return 'Negative'
    else:
        return 'Neutral'

def main():
    # --- PAGE CONFIG ---
    st.set_page_config(page_title="Product Review Analyzer", layout="wide")

    st.title("📊 Product Review Sentiment Analyzer")
    st.markdown("Analyze customer feedback instantly using Natural Language Processing.")

    # --- SIDEBAR ---
    st.sidebar.header("Instructions")
    st.sidebar.info("Upload a CSV file with a column named 'Review' or 'Text' to see the dashboard.")

    # --- SINGLE REVIEW ANALYSIS ---
    st.subheader("🔍 Analyze a Single Review")
    user_input = st.text_area("Enter a product review here:", key="single_input")

    if st.button("Analyze Sentiment"):
        if user_input:
            blob = TextBlob(user_input)
            score = blob.sentiment.polarity
            label = get_sentiment_label(score)
            
            if label == 'Positive':
                st.success(f"Positive Sentiment (Score: {score:.2f}) 😊")
            elif label == 'Negative':
                st.error(f"Negative Sentiment (Score: {score:.2f}) 😡")
            else:
                st.warning(f"Neutral Sentiment (Score: {score:.2f}) 😐")
        else:
            st.write("Please enter some text first.")

    st.divider()

    # --- BULK FILE UPLOAD ---
    st.subheader("📂 Bulk Analysis via CSV Upload")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        
        try:
            df = pd.read_csv(uploaded_file, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
        
        if df.empty:
            st.error("The uploaded file is empty.")
            return
            st.write("### ⚙️ Settings")
            default_options = ['review', 'text', 'content', 'comment', 'Feedback', 'Message']
            # Try to find a match, otherwise default to the first column in the file
            found_col = next((c for c in default_options if c in df.columns), df.columns[0])
            
            col_name = st.selectbox(
                "Which column contains the reviews?", 
                options=df.columns, 
                index=list(df.columns).index(found_col)
            )

               

        if col_name:
            # Processing
            df['score'] = df[col_name].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
            df['analysis'] = df['score'].apply(get_sentiment_label)

            # --- VISUALIZATIONS ---
            st.write("### 📈 Sentiment Analytics Dashboard")
            color_map = {'Positive': '#2ecc71', 'Neutral': '#95a5a6', 'Negative': '#e74c3c'}
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("#### 📊 Total Sentiment Volume")
                st.bar_chart(df['analysis'].value_counts())
                
                st.write("---")
                
                st.write("#### ☁️ Most Frequent Words")
                all_words = ' '.join([str(text) for text in df[col_name]])
                wordcloud = WordCloud(width=500, height=300, background_color='white').generate(all_words)
                fig_wc, ax_wc = plt.subplots()
                ax_wc.imshow(wordcloud, interpolation='bilinear')
                ax_wc.axis("off")
                st.pyplot(fig_wc)

            with col2:
                st.write("##") # Vertical spacing
                st.write("#### 🍩 Sentiment Share (%)")
                counts = df['analysis'].value_counts()
                current_colors = [color_map[label] for label in counts.index]
                
                fig, ax = plt.subplots()
                ax.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=140, pctdistance=0.85, colors=current_colors)
                fig.gca().add_artist(plt.Circle((0,0), 0.70, fc='white')) # Donut hole
                ax.axis('equal')
                st.pyplot(fig)

            # --- SUMMARY SECTION ---
            st.divider()
            st.write("### 📢 What does this analysis tell us?")
            
            total = len(df)
            pos_c = len(df[df['analysis'] == 'Positive'])
            neu_c = len(df[df['analysis'] == 'Neutral'])
            neg_c = len(df[df['analysis'] == 'Negative'])
            pos_p = (pos_c / total) * 100 if total > 0 else 0

            s_col1, s_col2 = st.columns(2)
            with s_col1:
                st.info("**Quick Stats**")
                st.write(f"Out of **{total}** reviews: \n- Happy: {pos_c} \n- Neutral: {neu_c} \n- Unhappy: {neg_c}")

            with s_col2:
                if pos_p > 70:
                    st.success("### 🌟 Overall Verdict: Great!")
                    st.write("Customers are highly satisfied. Keep doing what you are doing!")
                elif pos_p > 40:
                    st.warning("### ⚖️ Overall Verdict: Mixed")
                    st.write("Results are okay, but there's room for improvement.")
                else:
                    st.error("### ⚠️ Overall Verdict: Poor")
                    st.write("High dissatisfaction detected. Investigation required.")

            # --- DATA PREVIEW ---
            st.write("---")
            st.dataframe(df[[col_name, 'analysis']].head(10), use_container_width=True)
            
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Analysis Report", data=csv, file_name="report.csv", mime="text/csv")
        else:
            st.error("Could not find a 'review' or 'text' column.")

# --- RUN THE APP ---
if __name__ == "__main__":
    main()
