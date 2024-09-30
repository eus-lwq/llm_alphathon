# llm_alphathon

## 1. News Crawler 
- 1.1 WSJ News Scrapper:  wsj_scrapper: 
- 1.2 BBC Crawler: News-crawler (currently BBC scrapper only, New York Times using Captcha to prevent scrawling since 2023, Reuters only shows recent news)
check crawler details in Crawler folder readme!

## 2. RAG
- Used Milvus DB and Llama-Index to generate database embedding and store the vector data.
- Summarize and analyze 5 different market regimes.

## 3. Market regime prediction
#### - 3.1 Prediction result: prediction_result folder

#### - 3.2 wsj_news_database: Different wsj crawled news chunking:
    - 3.2.1 wsj news 2012 - 2024 
    - 3.2.2 wsj news 2012 - 2019
      
#### - 3.3 3_regime_predict: 3 label classification prediction
  - Market Regime 0: This regime is marked by slowing economic growth, declining consumer confidence, and reduced corporate earnings, leading to a bearish stock market.
  - Market Regime 1: This regime is characterized by mixed economic signals, geopolitical tensions, and policy uncertainties, leading to volatile market conditions.
  - Market Regime 2: This regime is characterized by robust economic growth, increased consumer confidence, and rising corporate earnings, leading to a bullish stock market. 

#### - 3.4 5_regime_predict: 3 label classification prediction
  - Market Regime 0: This regime is characterized by the initial phase of economic improvement following a recession, marked by increasing economic activity and improving investor sentiment.
  - Market Regime 1: This regime is marked by robust economic growth, increasing corporate profits, and rising stock prices, often accompanied by higher consumer spending and business investments.
  - Market Regime 2: This regime represents the height of economic activity, where growth rates are at their highest, but signs of overheating and potential downturns begin to emerge.
  - Market Regime 3: This regime is characterized by slowing economic growth, declining corporate profits, and increasing market volatility, often leading to a downturn.
  - Market Regime 4: This regime is marked by a significant decline in economic activity, rising unemployment, and falling stock prices, often leading to a prolonged economic downturn.

