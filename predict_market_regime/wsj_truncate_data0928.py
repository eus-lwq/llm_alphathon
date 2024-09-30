import os
import json

# Define the source and target directories
source_folder = '/Users/elinazhuang/Desktop/wsj'
target_folder = '/Users/elinazhuang/Desktop/wsj_2012to2024_0929'

# Create the target folder if it doesn't exist
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

# Iterate over all files in the source folder
for filename in os.listdir(source_folder):
    if filename.startswith("reorg_wsj_") and filename.endswith(".json"):
        # Construct the full path to the source file
        source_path = os.path.join(source_folder, filename)
        
        # Open and load the JSON data
        with open(source_path, 'r') as file:
            data = json.load(file)
        
        # Remove the 'Group' field
        if 'Group' in data:
            del data['Group']
        
        # Process the 'News' list and remove 'description', 'url', and 'source' fields
        if 'News' in data:
            for news_item in data['News']:
                if 'description' in news_item:
                    del news_item['description']
                if 'url' in news_item:
                    del news_item['url']
                if 'source' in news_item:
                    del news_item['source']
        
        # Define the new file path in the target folder
        target_path = os.path.join(target_folder, filename)
        
        # Save the modified data to the target folder
        with open(target_path, 'w') as new_file:
            json.dump(data, new_file, indent=4)

print("Processing completed! All files have been updated and saved in the 'wsj_2012to2024_0929' folder.")
