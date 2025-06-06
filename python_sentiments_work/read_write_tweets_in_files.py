import csv



def read_tweets(file_path: str) -> list[dict[str, str]]:
    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        list_of_tweets = list(reader)
    return list_of_tweets



def write_tweets_with_sentiments(file_path: str, tweets: list[dict[str, str]]):
    with open(file_path, "w", newline="") as file:
        fieldnames = list(tweets[0].keys())
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tweets)