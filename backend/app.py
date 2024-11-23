from flask import Flask, request, jsonify
from auth import create_twitter_client
from tasks import retweet_by_keyword, like_by_keyword, post_tweet, get_trending_hashtags
from analytics import fetch_tweet_metrics
from database import db
from datetime import datetime
import tweepy


app = Flask(__name__)

# Route to initialize a bot dynamically and test its connection
@app.route('/initialize-bot', methods=['POST'])
def initialize_bot():
    """
    Initialize a Twitter bot dynamically by its name and test its connection.

    Request Body:
    {
        "bot_name": "<name_of_bot>"
    }

    Returns:
        JSON response indicating success or failure of initialization.
    """
    data = request.json

    # Validate the request body
    if not data or not isinstance(data, dict):
        return jsonify({"error": "Invalid request format. JSON data is required."}), 400

    bot_name = data.get("bot_name")

    if not bot_name:
        return jsonify({"error": "Bot name is required in the request body."}), 400

    try:
        # Initialize the Twitter client for the specified bot
        twitter_client = create_twitter_client(bot_name)

        # Test connection (e.g., verify credentials or perform a test action)
        twitter_client.verify_credentials()
        return jsonify({"message": f"Twitter bot '{bot_name}' initialized and verified successfully!"}), 200

    except tweepy.errors.Unauthorized as te:
        return jsonify({"error": f"Invalid or expired token for bot '{bot_name}'. Please verify the credentials.", "details": str(te)}), 401
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


# Endpoint: Test Database Connection
@app.route('/test-db', methods=['GET'])
def test_db():
    try:
        tweets_collection = db["tweets"]
        document = tweets_collection.find_one()
        if document:
            return jsonify({"status": "success", "data": document}), 200
        else:
            return jsonify({"status": "success", "data": "No documents found"}), 200
    except Exception as e:
        return jsonify({"status": "failed", "error": str(e)}), 500

# Endpoint: Post or Get Tweets
@app.route('/tweet', methods=['GET', 'POST'])
def tweet():
    if request.method == 'GET':
        try:
            tweets = list(db["tweets"].find({}, {"_id": 0}))
            if tweets:
                return jsonify({"status": "success", "tweets": tweets}), 200
            else:
                return jsonify({"status": "success", "tweets": "No tweets found"}), 200
        except Exception as e:
            return jsonify({"status": "failed", "error": str(e)}), 500

    if request.method == 'POST':
        data = request.json
        message = data.get('message')

        if not message:
            return jsonify({"error": "The 'message' field is required"}), 400

        try:
            post_tweet(create_twitter_client(), message)  # Post the tweet
            db["tweets"].insert_one({
                "message": message,
                "action": "posted",
                "timestamp": datetime.utcnow()
            })
            return jsonify({"message": "Tweet posted successfully!", "tweet": message}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

# Endpoint: Retweet by Keyword
@app.route('/retweet', methods=['POST'])
def retweet():
    data = request.json
    keyword = data.get('keyword')

    if not keyword:
        return jsonify({"error": "The 'keyword' field is required"}), 400

    try:
        retweet_by_keyword(create_twitter_client(), keyword)
        db["actions"].insert_one({"keyword": keyword, "action": "retweet", "timestamp": datetime.utcnow()})
        return jsonify({"message": f"Retweeted tweets containing '{keyword}'."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint: Like by Keyword
@app.route('/like', methods=['POST'])
def like():
    data = request.json
    keyword = data.get('keyword')

    if not keyword:
        return jsonify({"error": "The 'keyword' field is required"}), 400

    try:
        like_by_keyword(create_twitter_client(), keyword)
        db["actions"].insert_one({"keyword": keyword, "action": "like", "timestamp": datetime.utcnow()})
        return jsonify({"message": f"Liked tweets containing '{keyword}'."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint: Fetch Trending Hashtags
@app.route('/trends', methods=['GET'])
def trends():
    try:
        trends = get_trending_hashtags(create_twitter_client(), location_woeid=1)
        db["actions"].insert_one({"action": "fetch_trends", "timestamp": datetime.utcnow()})
        return jsonify(trends), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint: Fetch Tweet Metrics
@app.route('/metrics/<tweet_id>', methods=['GET'])
def metrics(tweet_id):
    try:
        metrics = fetch_tweet_metrics(create_twitter_client(), tweet_id)
        db["actions"].insert_one({"tweet_id": tweet_id, "action": "fetch_metrics", "timestamp": datetime.utcnow()})
        return jsonify(metrics), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
