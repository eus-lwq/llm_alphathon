0. create folder names as
    article_titles_json
to store crawled files

1. install packages
    requests
    bs4
    json
    datetime  
    sqlite3  
    time    
    numpy  
    os  
    selenium
    dotenv   

2. run
    python3 createDB.py 
to create a database, 

3. run
    python3 crawl.py (可以在文件最下修改需要的日期)
to obtain the links of the existing webpages, 

4. run 
    python 3 web_scrap.py 
to obtain the content in the webpages.