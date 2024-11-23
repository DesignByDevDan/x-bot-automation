def fetch_tweet_metrics(twitter_client, tweet_id):
    tweet = twitter_client.get_status(tweet_id, tweet_mode="extended")
    return {
        "id": tweet.id,
        "text": tweet.full_text,
        "retweet_count": tweet.retweet_count,
        "like_count": tweet.favorite_count
    }
