import json
import os

# Function to read multiple JSON files and print headlines
def extract_headlines_from_multiple_files(json_files):
    headlines = []
    
    # Loop through each file in the list
    for json_file in json_files:
        with open(json_file, 'r') as file:
            data = json.load(file)
            
            # Extract headlines from each file
            for article in data:
                headlines.append(article['headline'])
    
    # # Print all headlines separated by newlines
    # print("\n".join(headlines))
    
    # Save headlines to a text file
    with open(output_file, 'w') as f:
        f.write("\n".join(headlines))

# List of JSON files to be read
json_files = ['article_titles_json/index_2016_1_1_page_1.json', 'article_titles_json/index_2016_1_1_page_2.json']  # Replace with actual file paths

output_file = "test_20160101_titles.txt"
# Call the function to extract and print headlines
extract_headlines_from_multiple_files(json_files)
