import asyncio
from twikit import Client, TooManyRequests
from configparser import ConfigParser
import time
from datetime import datetime
import csv
from random import randint
import os



MINIMUM_TWEETS = 1

# query documentation: https://docs.x.com/x-api/posts/search/integrate/build-a-query
QUERY = '("egg price" OR "eggs price" OR "dozen eggs price" OR "cost of eggs" OR "eggs cost" OR "price of eggs") \
         AND (place_country:US OR "USA" OR "America" OR "US") \
         AND ("$" OR "USD" OR "costs" OR "currently" OR "price is" OR "sold at") \
         -filter:links -filter:replies -filter:retweets'
        #  since:2023-01-01 until:2025-02-14'
#-filter:links -filter:replies -filter:retweets -filter:verified"
QUERY_2 = '("avian flu" OR "bird flu" OR "H5N1" OR "avian influenza" OR "poultry disease" OR "chicken virus") \
         AND ("egg prices" OR "egg shortage" OR "cost of eggs" OR "chicken prices") \
         AND (place_country:US OR "USA" OR "America" OR "US") \
         -filter:links -filter:replies -filter:retweets \
         since:2020-01-01 until:2025-02-14'

output_file_name = "raw_tweets.csv"
output_tweets = os.path.join("data_tweets", output_file_name)

client = Client(language="en-US")


async def login_X():

    config = ConfigParser()
    config.read("config.ini")
    username = config["X"]["username"]
    email = config["X"]["email"]
    password = config["X"]["password"]

    await client.login(auth_info_1=username, auth_info_2=email, password=password)
    client.save_cookies("cookies.json")



async def get_tweets(tweets, query):

    if tweets is None:
        #* Get tweets
        print(f"{datetime.now()} - Getting tweets...")
        tweets = await client.search_tweet(query, product="Top")
    else:
        wait_time = randint(5, 10)
        print(f"{datetime.now()} - Getting new tweets after {wait_time} seconds.")
        time.sleep(wait_time)
        tweets = await tweets.next()

    return tweets



async def main(query):

    with open(output_tweets, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Id", "Username", "Text", "Created At", "Retweets", "Likes", "Language"])

    
    # client.load_cookies("cookies.json")

    tweet_count = 0
    tweets = None

    while tweet_count < MINIMUM_TWEETS:

        try:
            tweets = await get_tweets(tweets, query)
        except TooManyRequests as e:
            rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
            print(f"{datetime.now()} - Rate limit reached. Wainting until {rate_limit_reset}.")
            wait_time = rate_limit_reset - datetime.now()
            time.sleep(wait_time.total_seconds())
            continue

        if not tweets:
            print(f"{datetime.now()} - No more tweets found.")
            break

        for tweet in tweets:
            tweet_count += 1
            tweet_data = [tweet_count, tweet.user.name, tweet.text, tweet.created_at, tweet.retweet_count, tweet.favorite_count, tweet.lang]

            with open(output_tweets, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(tweet_data)

        print(f"{datetime.now()} - Got {tweet_count} tweets.")



asyncio.run(main(query=QUERY))