import tweepy
from database import db  # Import the database connection

def get_bot_account(account_name):
    """
    Fetch bot account credentials from the database.

    Args:
        account_name (str): The name of the bot account to fetch credentials for.

    Returns:
        dict: A dictionary containing the bot's credentials if found, else None.
    """
    try:
        # Query the database for the bot account
        account = db["bot_accounts"].find_one({"account_name": account_name})
        if account:
            return {
                "api_key": account.get("api_key"),
                "api_secret": account.get("api_secret"),
                "access_token": account.get("access_token"),
                "access_secret": account.get("access_secret"),
            }
        return None
    except Exception as e:
        raise Exception(f"Error fetching bot account '{account_name}': {str(e)}")


def create_twitter_client(account_name):
    """
    Create a Twitter client for a specific bot account.

    Args:
        account_name (str): The name of the bot account to fetch credentials for.

    Returns:
        tweepy.API: Authenticated Twitter API client.

    Raises:
        ValueError: If the account credentials are not found.
        Exception: If Tweepy authentication fails.
    """
    # Fetch account credentials from the database
    account = get_bot_account(account_name)

    if not account:
        raise ValueError(f"Bot account '{account_name}' not found in the database.")

    # Extract credentials
    api_key = account["api_key"]
    api_secret = account["api_secret"]
    access_token = account["access_token"]
    access_secret = account["access_secret"]

    try:
        # Set up Tweepy authentication
        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_secret)

        # Return the authenticated Twitter API client
        return tweepy.API(auth, wait_on_rate_limit=True)
    except Exception as e:
        raise Exception(f"Failed to authenticate Twitter client for '{account_name}': {str(e)}")
