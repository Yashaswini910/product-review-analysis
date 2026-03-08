# Wordcloud
# Create a smaller wordcloud
plt.figure(figsize=(8, 4))     # Set the figure size
wordcloud = WordCloud(width=600, height=300).generate(text)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

# Analysis Summary
summary = {  
    'total_reviews': len(reviews),  
    'positive_reviews': sum(1 for r in reviews if r['sentiment'] == 'positive'),  
    'negative_reviews': sum(1 for r in reviews if r['sentiment'] == 'negative'),  
    'neutral_reviews': sum(1 for r in reviews if r['sentiment'] == 'neutral'),  
    'average_sentiment_score': sum(r['sentiment_score'] for r in reviews) / len(reviews),  
    'sentiment_distribution': {sentiment: sum(1 for r in reviews if r['sentiment'] == sentiment) for sentiment in ['positive', 'negative', 'neutral']}  
}

print(summary)  

if error_condition:  
    handle_error()  
