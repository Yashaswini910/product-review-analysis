# 📊 Product Review Sentiment Analyzer

A Streamlit web application that analyzes customer product reviews using Natural Language Processing (NLP) to determine sentiment — instantly and interactively.

## Features

- **Single Review Analysis** — Paste any review text and get an instant Positive / Neutral / Negative verdict with a polarity score.
- **Bulk CSV Analysis** — Upload a CSV file of reviews for batch processing with a full analytics dashboard.
- **Smart Column Detection** — Automatically detects the review column by scanning for a `Review` header, or falls back to the longest text column.
- **Interactive Visualizations:**
  - Bar chart of sentiment volume
  - Donut chart showing sentiment share (%)
  - Word cloud of most frequent terms
- **Overall Verdict** — Summarizes customer satisfaction as Great / Mixed / Poor based on the percentage of positive reviews.
- **Downloadable Report** — Export the analyzed results as a CSV file.

## Tech Stack

| Library | Purpose |
|---|---|
| `streamlit` | Web app UI |
| `textblob` | Sentiment analysis (NLP) |
| `pandas` | Data handling |
| `wordcloud` | Word frequency visualization |
| `matplotlib` | Charts and plots |

## 🚀 Live Demo

No installation needed — try it directly in your browser:

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://appuct-review-analysis.streamlit.app/)

## Usage

### Single Review
1. Type or paste a review into the text area under **"Analyze a Single Review"**.
2. Click **Analyze Sentiment** to see the result.

### Bulk Analysis
1. Prepare a CSV file with a column named `Review` (or any text column).
2. Upload it under **"Bulk Analysis via CSV Upload"**.
3. The dashboard will automatically generate charts, a word cloud, and a summary verdict.
4. Click **Download Analysis Report** to save the results.

### CSV Format Example

```
Review
"This product is absolutely amazing, highly recommended!"
"Worst purchase I've ever made. Completely useless."
"It's okay, nothing special but gets the job done."
```

## Project Structure


product-review-analysis/
├── app.py               # Main Streamlit application
├── requirements.txt     # Python dependencies
└── .devcontainer/       # Dev container configuration


## How Sentiment Scoring Works

The app uses **TextBlob's** polarity scoring:

- **Positive** → polarity score `> 0`
- **Neutral** → polarity score `= 0`
- **Negative** → polarity score `< 0`

The overall verdict thresholds are:
- 🌟 **Great** — more than 70% positive reviews
- ⚖️ **Mixed** — 40–70% positive reviews
- ⚠️ **Poor** — less than 40% positive reviews

## License

This project is open source. Feel free to fork and build on it!
