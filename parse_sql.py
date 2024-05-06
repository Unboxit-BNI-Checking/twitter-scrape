import csv
from datetime import datetime
import pytz

utc_plus_7 = pytz.timezone('Asia/Bangkok')
sql_file = "twitter_reports_seeder.sql"
current_time_utc_7 = datetime.now(pytz.utc).astimezone(utc_plus_7)
current_timestamp = current_time_utc_7.strftime('%Y-%m-%d %H:%M:%S')
idx = 1

with open('cleaned_tweets.csv', 'r', newline='') as csvfile, open(sql_file, 'w') as sqlfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)
    sqlfile.write("INSERT INTO twitter_reports (id, twitter_username, post_date, tweet_link, account_number, created_at, updated_at) VALUES ")
    for row in csvreader:
        username, created_at, tweet_url, account_numbers = row
        values = f"({idx}, '{username}', '{created_at}', '{tweet_url}', '{account_numbers}', '{current_timestamp}', '{current_timestamp}')"
        sqlfile.write(values)
        sqlfile.write(",\n")
        idx += 1
    sqlfile.write(";")
