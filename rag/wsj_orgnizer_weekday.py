import argparse
import glob
import json
import re
import pandas as pd
from datetime import datetime

"""
this file will generate a folder names as wsj_weekday to store reorg wsj files for rag.
"""

# how to run
# cd rag 
# python3 wsj_orgnizer_weekday.py gmm_labels.csv 2012-01-01 2019-12-31 /path/to/wsj_folder /path/to/output
# e.g.
# python3 wsj_orgnizer_weekday.py data/gmm_labels.csv 2012-01-01 2019-12-31 data/wsj_scrapper/article_titles_json data/wsj_weekday

# left join to the wsj
def combine_data_multiple_json_leftjoin(labels_df, start_date, end_date, wsj_folder_path, output_file_path):
    combined_data = {}
    date_regex = re.compile(r'index_(\d{4})_(\d{1,2})_(\d{1,2})_page.*\.json')

    # Convert the date in the dataframe to datetime to ensure proper comparison
    labels_df['Date'] = pd.to_datetime(labels_df['Date'])

    # Use the provided wsj_folder_path to search for JSON files
    for file_path in glob.glob(f'{wsj_folder_path}/index_*.json'):
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
            
            # If no exact match, find the next available label date
            if label_row.empty:
                future_labels = labels_df[labels_df['Date'] > article_date]
                if not future_labels.empty:
                    label_row = future_labels.iloc[0]  # Get the next available label row
                    next_available_date_str = label_row['Date'].strftime('%Y-%m-%d')  # Extract the date as a string
                    market_condition = int(label_row['Group'])  # Use the next available group value
                else:
                    market_condition = "None"
                    next_available_date_str = None
            else:
                next_available_date_str = label_row['Date'].iloc[0].strftime('%Y-%m-%d')  # Extract the date as a string
                market_condition = int(label_row['Group'].iloc[0])  # Use the matching group value

            # If no label row at all, skip this date
            if next_available_date_str is None:
                continue

            if next_available_date_str not in combined_data:
                combined_data[next_available_date_str] = {
                    'Date': next_available_date_str,
                    'Market Condition': market_condition,
                    'News': []
                }

            with open(file_path, 'r') as file:
                data = json.load(file)
                for article in data:
                    combined_data[next_available_date_str]['News'].append({
                        'news_title': article.get('headline', 'None'),
                        'keyword': article.get('keyword', 'None'),
                        'description': article.get('description', 'None'),
                        'url': article.get('link', 'None'),
                        'source': "WSJ"
                    })

    # Write each combined data set to a new JSON file with date in yyyy-mm-dd format
    for date, contents in combined_data.items():
        formatted_date = pd.to_datetime(date).strftime('%Y-%m-%d')
        output_file = f'{output_file_path}/reorg_wsj_{formatted_date}.json'
        
        with open(output_file, 'w') as outfile:
            json.dump(contents, outfile, indent=2)

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Combine WSJ data with GMM labels.")
    parser.add_argument("labels_file", help="Path to the labels CSV file.")
    parser.add_argument("start_date", help="Start date for filtering the WSJ data (YYYY-MM-DD).")
    parser.add_argument("end_date", help="End date for filtering the WSJ data (YYYY-MM-DD).")
    parser.add_argument("wsj_folder_path", help="Path to the WSJ folder containing article JSON files.")
    parser.add_argument("output_file_path", help="Output directory for the combined JSON files.")
    
    args = parser.parse_args()

    # Load labels dataframe
    labels_df = pd.read_csv(args.labels_file)

    # Parse start and end dates
    start_date = pd.to_datetime(args.start_date)
    end_date = pd.to_datetime(args.end_date)

    # Call the function with arguments
    combine_data_multiple_json_leftjoin(labels_df, start_date, end_date, args.wsj_folder_path, args.output_file_path)
