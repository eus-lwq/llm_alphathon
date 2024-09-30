import json
import os
from datetime import datetime, timedelta
import openai

# Initialize the OpenAI client
client = openai.OpenAI(api_key='your key')

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def read_market_regimes(file_path):
    regimes = {}
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, 1):
            line = line.strip()
            if not line:  # Skip empty lines
                continue
            try:
                date, regime = line.split(', ')
                regimes[date] = regime
            except ValueError as e:
                print(f"Error on line {line_number}: {line}")
                print(f"Error message: {str(e)}")
                print("Skipping this line and continuing...")
    return regimes

def write_market_regime(file_path, date, regime):
    with open(file_path, 'a') as file:
        file.write(f"{date}, {regime}\n")

def format_news_input(news_data):
    formatted_news = []
    date = news_data['Date']
    for item in news_data['News']:
        formatted_news.append(f"Title: {item['news_title']}, Keyword: {item['keyword']}")
    return "\n".join(formatted_news)

def get_market_regime_prediction(news_input):
    prompt = f"""
    ### Role ###
    You are a highly knowledgeable and helpful finance economist specializing in the US equity market. You have access to today's relevant news.

    ### Task ###
    Based on the provided news for today, please label the market regime. The 5 market regimes are represented as "Bull", "Bear", "Recession", "Recovery" or "Neutral".
    Market Regime 0: This regime is characterized by the initial phase of economic improvement following a recession, marked by increasing economic activity and improving investor sentiment.
    Market Regime 1: This regime is marked by robust economic growth, increasing corporate profits, and rising stock prices, often accompanied by higher consumer spending and business investments.
    Market Regime 2: This regime represents the height of economic activity, where growth rates are at their highest, but signs of overheating and potential downturns begin to emerge.
    Market Regime 3: This regime is characterized by slowing economic growth, declining corporate profits, and increasing market volatility, often leading to a downturn.
    Market Regime 4: This regime is marked by a significant decline in economic activity, rising unemployment, and falling stock prices, often leading to a prolonged economic downturn.

    ### Input ###
    {news_input}

    ### Output ###
    Please provide your prediction as A SINGLE INTEGER: 0 (Recovery), 1 (Expansion), 2 (Peak), 3 (Contraction), or 4 (Recession). NO EXPLANATION NEEDED.

    """

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt},
        ],
        model="gpt-4o-mini",
        temperature=0.1,
    )

    response = chat_completion.choices[0].message.content
    return response.strip()

# Main script/execution
start_date = datetime(2012, 1, 3)
end_date = datetime(2024, 7, 30)
current_date = start_date
folder_path = "/Users/elinazhuang/Desktop/wsj_2012to2024"
market_regimes_file = "/Users/elinazhuang/Desktop/5_market_regimes.txt"

market_regimes = read_market_regimes(market_regimes_file)

while current_date <= end_date:
    file_name = f"reorg_wsj_{current_date.strftime('%Y-%m-%d')}.json"
    file_path = os.path.join(folder_path, file_name)

    if os.path.exists(file_path):
        news_data = read_json_file(file_path)
        news_input = format_news_input(news_data)
        
        prediction = get_market_regime_prediction(news_input)
        write_market_regime(market_regimes_file, current_date.strftime('%Y-%m-%d'), prediction)
        market_regimes[current_date.strftime('%Y-%m-%d')] = prediction

        print(f"Date: {current_date.strftime('%Y-%m-%d')}")
        print(f"Predicted market regime: {prediction}")
        print("---")
    else:
        print(f"No news data found for {current_date.strftime('%Y-%m-%d')}. Skipping.")

    current_date += timedelta(days=1)

print("Market regime predictions completed.")