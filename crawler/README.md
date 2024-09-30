# Crawler
## Crawler Usage
- WSJ Crawler - `wsj_scrapper`
- BBC Crawler - `News-crawler`

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
to obtain the links of the existing webpages.

this script will save crawled contents as db in root folder and jsons in folder

json example:
```
[{"headline": "2012: Taking a Look on the Bright Side", "article_time": "6:35 PM ET", "year": 2012, "month": 1, "day": 2, "keyword": "Agenda", "link": "http://online.wsj.com/article/SB10001424052970203550304577136773807576662.html", "scraped_at": "2024-09-13 01:55:27", "scanned_status": 0}, {"headline": "Ethiopia Makes Gains Against Militants in Somalia", "article_time": "5:21 PM ET", "year": 2012, "month": 1, "day": 2, "keyword": "Africa", "link": "http://online.wsj.com/article/SB10001424052970203462304577136612699687638.html", "scraped_at": "2024-09-13 01:55:27", "scanned_status": 0},
```

#### (optional) Step 5. to obtain the content in the webpages.
this is an optional step , currently we just need title, description, date, and url.
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

This script will save crawled content as `year_folder/month_folder/day_folder/article` and `year_folder/month_folder/day_folder/titles`

one day `article` example:
```
{
    "expected_number": 27,
    "number": 26,
    "articles": [
        {
            "title": "Australia Speaker Bronwyn Bishop quits over expenses - BBC News",
            "published_date": "2015-08-02",
            "authors": [
                "https://www.facebook.com/bbcnews"
            ],
            "description": "The speaker of the lower house of the Australian parliament, Bronwyn Bishop, resigns over an expenses scandal.",
            "section": "Australia",
            "link": "http://www.bbc.co.uk/news/world-australia-33751156"
        },
        {
            "title": "Selma civil rights march begins - BBC News",
            "published_date": "2015-08-02",
            "authors": [],
            "description": "Civil rights campaigners in the US start an 860-mile (1,385 km) march from Selma, Alabama to Washington DC to highlight what they say is a fresh attack on equal rights for African Americans",
            "section": null,
            "link": "http://www.bbc.co.uk/news/world-us-canada-33750613"
        },....
```

one day `titles` example:
```
Australia Speaker Bronwyn Bishop quits over expenses - BBC News
Selma civil rights march begins - BBC News
British Airways to cut hand baggage allowance - BBC News
Jerusalem Gay Pride: Israel teenage stabbing victim dies - BBC News
MH370 search: More debris removed from Reunion beach - BBC News
Arsenal 1-0 Chelsea - BBC Sport
```
