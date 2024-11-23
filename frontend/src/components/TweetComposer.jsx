import React, { useState } from 'react';
import axios from 'axios';

function TweetComposer() {
    const [message, setMessage] = useState("");

    const postTweet = async () => {
        try {
            const response = await axios.post('http://127.0.0.1:5000/tweet', { message });
            alert(response.data.message);
        } catch (error) {
            console.error("Error posting tweet:", error);
            alert("Failed to post the tweet.");
        }
    };

    return (
        <div>
            <h1>Tweet Composer</h1>
            <textarea
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Write your tweet here..."
            />
            <button onClick={postTweet}>Post Tweet</button>
        </div>
    );
}

export default TweetComposer;
