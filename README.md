# Market Regime Labeling Based on Investor Sentiments Using Large Language Models (LLMs)
We utilized large language models from January 1, 2012, to December 31, 2019, leveraging a Retrieval-Augmented Generation (RAG) framework combined with GPT-4o for market regime summarization. For market regime prediction, we employed GPT-4o mini, extending from January 1, 2012, to July 31, 2024, with out-of-sample testing performed from 2020 to 2024.

## 1. Data collection: Wall Street Journal News Crawler
Data Collection: After attempting to crawl data from multiple sources, only The Wall Street Journal provided a comprehensive dataset from 2012 to 2024, suitable for U.S. equity market analysis. The code of wsj crawler is based on https://github.com/gonzalezcortes/scraping_news_articles and modified.

### How to use
#### Step 1.0 Install Dependencies
- option 1. intsall from pip
```
cd crawler
pip install -r requirements.txt
```

- option 2. install from yaml
```
conda env create -f environment.yaml
```

#### Step 1.1 open folder in wsj_scrapper
```
cd wsj_scrapper
```

#### Step 1.2 create folder names as "article_titles_json" to store crawled files
```
mkdir article_titles_json
```

#### Step 1.3 Create a database
```
python3 createDB.py
```

#### Step 1.4 Start scrawling with changed start time and end time
```
python3 crawl.py --start <start date in yyyy-mm-dd> --end <end date in yyyy-mm-dd>
```

example: 
```
python3 crawl.py --start "2018-01-02" --end "2019-12-31"
```
to obtain the links of the existing webpages.

this script will save crawled contents as db in root folder and jsons in folder

json example:
```
[{"headline": "2012: Taking a Look on the Bright Side", "article_time": "6:35 PM ET", "year": 2012, "month": 1, "day": 2, "keyword": "Agenda", "link": "http://online.wsj.com/article/SB10001424052970203550304577136773807576662.html", "scraped_at": "2024-09-13 01:55:27", "scanned_status": 0}, {"headline": "Ethiopia Makes Gains Against Militants in Somalia", "article_time": "5:21 PM ET", "year": 2012, "month": 1, "day": 2, "keyword": "Africa", "link": "http://online.wsj.com/article/SB10001424052970203462304577136612699687638.html", "scraped_at": "2024-09-13 01:55:27", "scanned_status": 0},
```

#### (optional) Step 1.5 to obtain the content in the webpages.
This script crawl the news detail content from wsj into the folder.
this is an optional step , currently we just need title, description, date, and url.
```
python 3 web_scrap.py
```



## 2. Market Regime Summarization: RAG Indexing & Prompt Engineering & Query
Market Regime Summarization: We used the RAG framework and Llama-Index to incorporate daily news and structure the dataset indexing, enabling the model to recursively merge text chunks and utilize this data during generation. The summarized training data was embedded into the Milvus vector database for efficient storage and retrieval. 
Following prompt engineering, the model produced two market regime classification schemas, each supported by detailed descriptions and evidence: 
- one with three categories (Bear, Neutral, Bull) and
- one with five categories (Recovery, Expansion, Peak, Contraction, Recession).
### How to run
#### Step 2.1 Data reorgnization
```
cd summarization
python3 wsj_orgnizer_weekday.py <gmm_labels_df_csv> <start_date> <end_date> <wsj_folder_path> <output_file_path>
# example usage:
python3 wsj_orgnizer_weekday.py data/gmm_labels.csv 2012-01-01 2019-12-31 data/wsj_weekday data/wsj_weekday_reorg
```
#### Step 2.2 Market condition converter
```
python3 market_condition_converter.py <old_dir_path> <new_dir_path>
# example usage:
python3 market_condition_converter.py data/wsj_weekday_reorg data/wsj_weekday_convert
```
#### Step 2.3 Use RAG to summarize the market regime
run `rag_multiple_files.ipynb` with RAG db indexing, and prompt engineering to get the market regime analysis and result


## 3. Market regime prediction: 
Market Regime Prediction: After defining the market regime classifications, we incorporated these labels into daily prediction prompts. We performed prompt engineering and parameter sampling (e.g., top-p, temperature, and frequency penalty) to ensure the quality of market regime prediction outputs. 

#### Step 3.1 wsj_news_database: Different wsj crawled news chunking
We chunked wsj news into two chunks, 
chunk 1, contains wsj news from 2012 to 2019 to generate the prediction result,
chunk 2, contains wsj news from 2012 to 2024 to examine our prediction accuracy.
      
#### Step 3.2 prediction in 3 label classification, 3_regime_predict
`3_regime_predict.py` will generate a text file names as `3_market_regime.txt`into prediction_result folder, contains 3 labels classification to market regimes (1 as Bull, 0 as Neutral, -1 as Bear).

Prompt: 
```
  - Market Regime 0: This regime is marked by slowing economic growth, declining consumer confidence, and reduced corporate earnings, leading to a bearish stock market.
  - Market Regime 1: This regime is characterized by mixed economic signals, geopolitical tensions, and policy uncertainties, leading to volatile market conditions.
  - Market Regime 2: This regime is characterized by robust economic growth, increased consumer confidence, and rising corporate earnings, leading to a bullish stock market. 
```

#### Step 3.3  prediction in 5 label classification, 5_regime_predict
`5_regime_predict.py` will generate a text file names as `5_market_regime.txt` into prediction_result folder, contains 5 labels classification to market regimes (0 as Recovery, 1 as Expansion, 3 as Peak, 3 as Contraction, 4 as Recession).

Prompt:

```
  - Market Regime 0: This regime is characterized by the initial phase of economic improvement following a recession, marked by increasing economic activity and improving investor sentiment.
  - Market Regime 1: This regime is marked by robust economic growth, increasing corporate profits, and rising stock prices, often accompanied by higher consumer spending and business investments.
  - Market Regime 2: This regime represents the height of economic activity, where growth rates are at their highest, but signs of overheating and potential downturns begin to emerge.
  - Market Regime 3: This regime is characterized by slowing economic growth, declining corporate profits, and increasing market volatility, often leading to a downturn.
  - Market Regime 4: This regime is marked by a significant decline in economic activity, rising unemployment, and falling stock prices, often leading to a prolonged economic downturn.
```

