from sentiment import predict_sentiment, ROBERTA_SUPPORTED_LANGUAGES
from translate import translate_text
import asyncio
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from read_write_tweets_in_files import read_tweets, write_tweets_with_sentiments



input_file_name = "raw_tweets.csv"
path_input_tweets = os.path.join("..", "X_tweets_extraction", "data_tweets", input_file_name)

output_file_name = "tweets_with_sentiments_roberta.csv"
output_tweets = os.path.join("sentiment_output", output_file_name)



async def generate_sentiments(tweets):
    for tweet in tweets:
        tweet_text, language = tweet["Text"], tweet["Language"]

        # if not (language and language in ROBERTA_SUPPORTED_LANGUAGES):
        translated_text, language = await translate_text(tweet_text)    

        # if language in ROBERTA_SUPPORTED_LANGUAGES:
        #     sentiment = predict_sentiment(tweet_text)
        # else:
        sentiment, probability = predict_sentiment(translated_text)

        tweet["Translated Text"] = translated_text
        tweet["Sentiment"] = sentiment
        tweet["Sentiment Probability"] = probability

    write_tweets_with_sentiments(output_tweets, tweets)



tweets = read_tweets(path_input_tweets)
asyncio.run(generate_sentiments(tweets))