import os
import json
import argparse

# Define your mapping of market conditions
market_mapping = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}

# Argument parser for input and output directories
def parse_args():
    parser = argparse.ArgumentParser(description="Map market condition values and save to another directory.")
    parser.add_argument('input_dir', type=str, help="Path to the input directory containing JSON files.")
    parser.add_argument('output_dir', type=str, help="Path to the output directory to save modified JSON files.")
    return parser.parse_args()

# Main function to process the JSON files
def process_json_files(input_directory, output_directory):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Iterate through all JSON files in the input directory
    for filename in os.listdir(input_directory):
        if filename.endswith('.json'):
            input_file_path = os.path.join(input_directory, filename)
            
            # Open and load the JSON data
            with open(input_file_path, 'r') as file:
                data = json.load(file)
            
            # Replace "Market Condition" value with the corresponding letter
            if 'Market Condition' in data:
                condition = data['Market Condition']
                if condition in market_mapping:
                    data['Market Condition'] = market_mapping[condition]
            
            # Save the modified data to the output directory
            output_file_path = os.path.join(output_directory, filename)
            with open(output_file_path, 'w') as file:
                json.dump(data, file, indent=4)

            print(f"Processed {filename} and saved to {output_file_path}")

if __name__ == "__main__":
    # Parse command-line arguments
    args = parse_args()
    
    # Process the JSON files with provided input and output directories
    process_json_files(args.input_dir, args.output_dir)

    # example usgae:
    # python3 market_condition_converter.py <old_dir_path> <new_dir_path>
    # python3 market_condition_converter.py data/wsj_weekday data/wsj_weekday_new
