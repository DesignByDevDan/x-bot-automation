import tweepy
import schedule
import time

# Retweet tweets by keyword
def retweet_by_keyword(twitter_client, keyword):
    for tweet in tweepy.Cursor(twitter_client.search_tweets, q=keyword, lang="en").items(5):
        try:
            twitter_client.retweet(tweet.id)
        except tweepy.TweepError as e:
            print(f"Error: {e}")

# Like tweets by keyword
def like_by_keyword(twitter_client, keyword):
    for tweet in tweepy.Cursor(twitter_client.search_tweets, q=keyword, lang="en").items(5):
        try:
            twitter_client.create_favorite(tweet.id)
        except tweepy.TweepError as e:
            print(f"Error: {e}")

# Post a tweet
def post_tweet(twitter_client, message):
    twitter_client.update_status(message)

# Fetch trending hashtags
def get_trending_hashtags(twitter_client, location_woeid):
    trends = twitter_client.get_place_trends(location_woeid)
    return [trend["name"] for trend in trends[0]["trends"]]
