# Crawler
## Crawler Usage
- WSJ
- BBC

## How to use
### 0. Install Dependencies
- option 1. intsall from pip
```
pip install -r requirements.txt
```

- option 2. install from yaml
```
conda env create -f environment.yaml
```

### 1. WSJ Crawler (WSJ)
#### Step 1. open folder in wsj_scrapper
```
cd wsj_scrapper
```

#### Step 2. create folder names as "article_titles_json" to store crawled files
```
mkdir article_titles_json
```

#### Step 3. Create a database
```
python3 createDB.py
```

#### Step 4. Start scrawling with changed start time and end time
```
python3 crawl.py --start <start date in yyyy-mm-dd> --end <end date in yyyy-mm-dd>
```

example: 
```
python3 crawl.py --start "2018-01-02" --end "2019-12-31"
```
to obtain the links of the existing webpages, 

#### (optional, currently we just need title, description, date, and url) Step 5. to obtain the content in the webpages.
```
python 3 web_scrap.py
```

### 2. News Crawler (BBC)
#### Step 1. Change settings in configuration
news_crawler - settings - bbc.cfg

These are the variables that you can change:
 `start_date`, `end_date` and `path`.
```
# The start date to crawl
# Format: yyyy-mm-dd
start_date=2016-01-01

# The end date to crawl, not included
# format: yyyy-mm-dd
end_date=2016-12-31

# The step time
# Unit can be day, month, year
step_unit=day
step=1

# Storage path
path=./dataset/bbc/

# Time interval between two fetches
# Unit: seconds
# default: 0.2
sleep=0.2
```

#### Step 2. Start crawling with new bbc configuration
```
python bbc_crawler.py settings/bbc.cfg
```

