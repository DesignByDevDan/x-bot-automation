import schedule
import time
import logging
from tasks import retweet_by_keyword, like_by_keyword
from database import db
from auth import create_twitter_client

logging.basicConfig(level=logging.INFO)

def perform_actions():
    logging.info("Starting scheduled actions...")
    bot_account = db["bot_accounts"].find_one({"account_name": "MyBotAccount"})
    twitter_client = create_twitter_client(bot_account["account_name"])
    settings = bot_account.get("settings", {})
    
    # Retweet tweets based on keywords
    for keyword in settings.get("keywords", []):
        logging.info(f"Retweeting for keyword: {keyword}")
        retweet_by_keyword(twitter_client, keyword)

    # Like tweets based on hashtags
    for hashtag in settings.get("monitor_hashtags", []):
        logging.info(f"Liking tweets for hashtag: {hashtag}")
        like_by_keyword(twitter_client, hashtag)

# Schedule the job
schedule.every(15).minutes.do(perform_actions)

# Keep running
while True:
    schedule.run_pending()
    time.sleep(1)
