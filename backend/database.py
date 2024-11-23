import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to MongoDB
MONGO_URI = os.getenv("MONGO_URI")
print(f"MONGO_URI: {MONGO_URI}")  # Debugging step
client = MongoClient(MONGO_URI)

# Select your database
db = client["twitter_bot"]

# Collections
tweets_collection = db["tweets"]
actions_collection = db["actions"]
bot_accounts_collection = db["bot_accounts"]  # New collection for bot accounts

# Add a bot account to the database
def add_bot_account(account_name, api_key, api_secret, access_token, access_secret):
    bot_accounts_collection.insert_one({
        "account_name": account_name,
        "api_key": api_key,
        "api_secret": api_secret,
        "access_token": access_token,
        "access_secret": access_secret
    })

# Retrieve all bot accounts
def get_bot_accounts():
    return list(bot_accounts_collection.find({}, {"_id": 0}))

# Retrieve a specific bot account by name
def get_bot_account(account_name):
    return bot_accounts_collection.find_one({"account_name": account_name}, {"_id": 0})
