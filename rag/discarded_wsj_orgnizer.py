

# this function will form one big json
def combine_data(labels_df, start_date, end_date):
    combined_data = {}
    date_regex = re.compile(r'index_(\d{4})_(\d{1,2})_(\d{1,2})_page.*\.json')
    # change path here
    for file_path in glob('../wsj_scrapper/article_titles_json/index_*.json'):
        match = date_regex.search(file_path)
        if match:
            year, month, day = match.groups()
            date_str = f'{year}-{int(month):02d}-{int(day):02d}'
            article_date = pd.to_datetime(date_str)

            # Skip dates outside the specified range
            if article_date < start_date or article_date > end_date:
                continue

            label_row = labels_df[labels_df['Date'] == article_date]
            if label_row.empty:
                continue  # Skip this date if no corresponding entry in the labels

            market_condition = int(label_row['Group'].values[0]) if not label_row.empty else None

            if date_str not in combined_data:
                combined_data[date_str] = {
                    'Market Condition': market_condition,
                    'News': []
                }

            with open(file_path, 'r') as file:
                data = json.load(file)
                for article in data:
                    combined_data[date_str]['News'].append({
                        'news_title': article['headline'],
                        'keyword': article['keyword'],
                        'description': "None",
                        'url': article['link'],
                        'source': "WSJ"
                    })

    with open('data/combined_wsj.json', 'w') as outfile:
        json.dump(combined_data, outfile, indent=2, default=str)

# with inner join
def combine_data_multiple_json(labels_df, start_date, end_date):
    combined_data = {}
    date_regex = re.compile(r'index_(\d{4})_(\d{1,2})_(\d{1,2})_page.*\.json')

    # Convert the date in the dataframe to datetime to ensure proper comparison
    labels_df['Date'] = pd.to_datetime(labels_df['Date'])

    for file_path in glob('../wsj_scrapper/article_titles_json/index_*.json'):
        match = date_regex.search(file_path)
        if match:
            year, month, day = match.groups()
            date_str = f'{year}-{month}-{day}'
            article_date = pd.to_datetime(date_str)

            # Skip dates outside the specified range
            if article_date < start_date or article_date > end_date:
                continue

            # Find label row with the exact same date
            label_row = labels_df[labels_df['Date'] == article_date]
            if label_row.empty:
                continue  # Skip this date if no corresponding entry in the labels

            # Assuming only one row per date in the label dataframe
            market_condition = int(label_row['Group'].iloc[0])

            if date_str not in combined_data:
                combined_data[date_str] = {
                    'Date': datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m-%d'),
                    'Market Condition': market_condition,
                    'News': []
                }

            with open(file_path, 'r') as file:
                data = json.load(file)
                for article in data:
                    combined_data[date_str]['News'].append({
                        'news_title': article.get('headline', 'None'),
                        'keyword': article.get('keyword', 'None'),
                        'description': article.get('description', 'None'),
                        'url': article.get('link', 'None'),
                        'source': "WSJ"
                    })

    # Write each combined data set to a new JSON file with date in yyyy-mm-dd format
    for date, contents in combined_data.items():
        formatted_date = pd.to_datetime(date).strftime('%Y-%m-%d')
        output_file_path = f'data/wsj_condition/reorg_wsj_{formatted_date}.json'
        
        with open(output_file_path, 'w') as outfile:
            json.dump(contents, outfile, indent=2)


# left join to the wsj
def combine_data_multiple_json_leftjoin(labels_df, start_date, end_date):
    combined_data = {}
    date_regex = re.compile(r'index_(\d{4})_(\d{1,2})_(\d{1,2})_page.*\.json')

    # Convert the date in the dataframe to datetime to ensure proper comparison
    labels_df['Date'] = pd.to_datetime(labels_df['Date'])

    for file_path in glob('../wsj_scrapper/article_titles_json/index_*.json'):
        match = date_regex.search(file_path)
        if match:
            year, month, day = match.groups()
            date_str = f'{year}-{month}-{day}'
            article_date = pd.to_datetime(date_str)

            # Skip dates outside the specified range
            if article_date < start_date or article_date > end_date:
                continue

            # Find label row with the exact same date
            label_row = labels_df[labels_df['Date'] == article_date]
            if label_row.empty:
                market_condition = "None"  # If no matching label row, set market condition to None
            else:
                market_condition = int(label_row['Group'].iloc[0])  # Use the matching group value

            if date_str not in combined_data:
                combined_data[date_str] = {
                    'Date': datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m-%d'),
                    'Market Condition': market_condition,
                    'News': []
                }

            with open(file_path, 'r') as file:
                data = json.load(file)
                for article in data:
                    combined_data[date_str]['News'].append({
                        'news_title': article.get('headline', 'None'),
                        'keyword': article.get('keyword', 'None'),
                        'description': article.get('description', 'None'),
                        'url': article.get('link', 'None'),
                        'source': "WSJ"
                    })

    # Write each combined data set to a new JSON file with date in yyyy-mm-dd format
    for date, contents in combined_data.items():
        formatted_date = pd.to_datetime(date).strftime('%Y-%m-%d')
        output_file_path = f'data/wsj_condition_left/reorg_wsj_{formatted_date}.json'
        
        with open(output_file_path, 'w') as outfile:
            json.dump(contents, outfile, indent=2)
