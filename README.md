# 🥚 US Egg Price Prediction — February 2025

This project forecasts the average retail price of a dozen eggs in the US for **February 2025**. It was developed to inform a prediction market on [Polymarket](https://polymarket.com/event/price-of-dozen-eggs-in-february?tid=1750708522977), leveraging a blend of econometric modeling, machine learning, and real-time sentiment analysis from Twitter (X).

---

## 📊 Project Summary

- **🎯 Objective:** Predict the average US retail price of a dozen eggs for February 2025.
- **📈 Market Context:** Polymarket prediction event.
- **🧪 Approach:** 
  - Historical time series modeling (OLS, VECM)
  - Sentiment analysis of X (Twitter) posts on egg prices and poultry disease
  - Integration of public opinion and economic indicators

---

## 🗂️ Repository Structure

```bash
├── data/
│   ├── Final_Dataset/
│   │   └── Predict_Avg_Eggs_Price_Dataset.csv
│   └── Data_Processing.ipynb         # Data loading and cleaning
├── python_model_work/
│   ├── regression_model.ipynb        # OLS Regression with features
│   └── VECM_model.ipynb              # Vector Error Correction Model
├── python_sentiments_work/
│   ├── llm_sentiment_analysis/
│   │   └── llm_sentiment.py          # LLM (LLaMA3 via Groq) sentiment labeling
│   ├── roberta_sentimental_analysis/
│   │   ├── roberta_sentiment.py      # RoBERTa sentiment analysis with translation
│   │   ├── sentiment.py              # Inference logic and model setup
│   │   ├── translate.py              # Translation for multilingual tweets
│   │   └── requirements.txt          # Environment dependencies
│   ├── X_tweets_extraction/
│   │   ├── config.ini                # Auth info for X API scraping
│   │   └── extraction_main.py        # X tweet extractor with relevant queries
│   └── read_write_tweets_in_files.py # I/O utils for tweets

---

## 🧠 Methodology

### 📅 Data Processing
- Collected and merged USDA price data, CPI components, and energy indices
- Created lagged features and differences for stationarity
- Merged structured data with social media sentiment statistics

### 🤖 Models

#### 1. **OLS Regression**
- scikit-learn-based linear model
- Features: lagged egg prices, inflation indicators, energy prices, and tweet sentiment stats

#### 2. **Vector Error Correction Model (VECM)**
- Models cointegrated time series relationships
- Suitable for economic systems with long-run equilibria
- Johansen test used to determine rank

### 🐦 Sentiment Analysis

#### 🧠 LLM-Based Sentiment (Groq LLaMA 3)
- One-word sentiment classification: `positive`, `neutral`, or `negative`
- Processes each tweet with a prompt and saves results

#### 🤖 RoBERTa-Based Sentiment
- Model: `cardiffnlp/twitter-roberta-base-sentiment`
- Translates non-English tweets using Google Translate API
- Outputs sentiment label and model confidence

### 🕸️ Tweet Extraction
- Uses [Twikit](https://github.com/rexploit/twikit) to scrape tweets
- Query 1: Price-specific egg-related tweets
- Query 2: Avian flu and poultry disease concerns
- Filters for US geography and signal-rich posts

---

## 📈 Results & Insights

- Energy prices and CPI metrics significantly influence egg prices
- Tweets about avian flu and rising prices show predictive sentiment shifts
- Both LLM and RoBERTa models show consistent sentiment trends over time

> 🧮 **Final price prediction for February 2025:** Based on the VECM model, the initial forecast was **$4.64** per dozen, with a 95% confidence interval between **$4.12** and **$5.17**.

However, after analyzing sentiment data from Twitter (X), which revealed overwhelmingly negative sentiment — including public concern over rising prices and avian flu outbreaks — we decided to **adjust our forecast upward** to align with the market narrative.

🎯 **Final bet placed:** **$5.25–$5.50** window on Polymarket  
📈 **Realized price (USDA):** **$5.897**  
✅ Fell within the **$5.75–$6.00** resolution window on Polymarket.

---