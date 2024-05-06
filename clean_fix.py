import os
import pandas as pd
import re
from datetime import datetime

def extract_account_numbers(text):
    pattern = r'\b\d{10}\b'
    account_numbers = re.findall(pattern, text)
    return account_numbers

def parse_created_at(created_at):
    dt_object = datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")
    return dt_object.isoformat()

dfs = []
for csv_file in os.listdir("./tweets-data/"):
    df = pd.read_csv(os.path.join("./tweets-data/", csv_file))
    df = df[['username', 'created_at', 'full_text', 'tweet_url']]
    df['account_numbers'] = df['full_text'].apply(extract_account_numbers)
    df = df[df['account_numbers'].astype(bool)] 
    df = df.explode('account_numbers')
    df = df.drop_duplicates()
    df = df.drop(columns=['full_text'])
    df['created_at'] = df['created_at'].apply(parse_created_at)
    dfs.append(df)

final_df = pd.concat(dfs, ignore_index=True)
final_df.to_csv("cleaned_tweets.csv", index=False)
