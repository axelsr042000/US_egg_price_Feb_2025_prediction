from groq import Groq
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from read_write_tweets_in_files import read_tweets, write_tweets_with_sentiments
import tqdm


GROQ_API_KEY = "XXX"
client = Groq(api_key=GROQ_API_KEY)
model="llama3-8b-8192"

input_file_name = "raw_tweets.csv"
path_input_tweets = os.path.join("..", "X_tweets_extraction", "data_tweets", input_file_name)

output_file_name = "tweets_with_sentiments.csv"
output_tweets = os.path.join("sentiment_output", output_file_name)



def llm_request(prompt, model=model):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        messages=messages, 
        model=model)
    return response.choices[0].message.content



tweets = read_tweets(path_input_tweets)

for tweet in tqdm.tqdm(tweets):
    prompt = f"""
    What is the sentiment of the following tweet,
    tweet text: {tweet["Text"]}
    return the result with one word as positive, neutral, or negative.
    """
    try:
        sentiment_result = llm_request(prompt=prompt, model=model)
    except Exception as e:
        print(f"Error processing tweet {tweet['Text']}: {e}")
        sentiment_result = "unknown"

    tweet["Sentiment"] = sentiment_result

write_tweets_with_sentiments(output_tweets, tweets)