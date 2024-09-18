import pandas as pd
import json
import os
from glob import glob
import re
import argparse

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
                    'Group': market_condition,
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

    with open('data/wsj/combined_wsj.json', 'w') as outfile:
        json.dump(combined_data, outfile, indent=2, default=str)

    
    # this function will form multiple small json with date as title
    def combine_data_multiple_json(labels_df, start_date, end_date):
        combined_data = {}
        date_regex = re.compile(r'index_(\d{4})_(\d{1,2})_(\d{1,2})_page.*\.json')

        for file_path in glob('../wsj_scrapper/article_titles_json/index_*.json'):
            match = date_regex.search(file_path)
            if match:
                year, month, day = match.groups()
                date_str = f'{year}-{month}-{day}'
                article_date = pd.to_datetime(date_str)

                # Skip dates outside the specified range
                if article_date < start_date or article_date > end_date:
                    continue

                label_row = labels_df[labels_df['Date'] == article_date]
                if label_row.empty:
                    continue  # Skip this date if no corresponding entry in the labels

                # Ensure market condition is converted to Python native int (or str, as needed)
                market_condition = int(label_row['Group'].values[0]) if not label_row.empty else None

                if date_str not in combined_data:
                    combined_data[date_str] = {
                        'Date': date_str,
                        'Group': market_condition,
                        'News': []
                    }

                with open(file_path, 'r') as file:
                    data = json.load(file)
                    for article in data:
                        combined_data[date_str]['News'].append({
                            'news_title': article['headline'],
                            'keyword': article['keyword'],  # Assuming description is the headline for simplicity
                            'description':"None",
                            'url': article['link'],
                            'source':"WSJ"
                        })

        for date, contents in combined_data.items():
            with open(f'data/wsj/reorg_wsj_{date}.json', 'w') as outfile:
                # Use json.dump() with default=str to handle any other unserializable objects gracefully
                json.dump(contents, outfile, indent=2, default=str)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process WSJ articles within a date range.')
    parser.add_argument('--start_date', type=lambda s: pd.to_datetime(s), help='Start date YYYY-MM-DD')
    parser.add_argument('--end_date', type=lambda s: pd.to_datetime(s), help='End date YYYY-MM-DD')
    parser.add_argument('--json_type', type=str, choices=['big', 'small'], default='big', help='JSON type: "big" or "small"')

    args = parser.parse_args()

    labels_df = pd.read_csv('data/gmm_labels.csv')
    labels_df['Date'] = pd.to_datetime(labels_df['Date'], format='%Y-%m-%d')  # Ensure the date format is consistent
    
    if args.json_type == 'big':
        combine_data(labels_df, args.start_date, args.end_date)
    elif args.json_type == 'small':
        combine_data_multiple(labels_df, args.start_date, args.end_date)
    
    print("orgnization complete!")
    # example usage
    # python3 wsj_json_orgnizer.py --start_date 2012-01-01 --end_date 2019-12-31 --json_type big
