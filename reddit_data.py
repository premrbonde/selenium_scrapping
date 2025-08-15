import os
import praw
from datetime import datetime

def scrape_reddit(min_results=100):
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT")
    )

    results = []
    for submission in reddit.subreddit("burgerking").hot(limit=min_results):
        results.append({
            "Product": None,
            "Price": None,
            "Type": None,
            "Location": None,
            "Review_Text": submission.title + " - " + submission.selftext,
            "Hashtags": None,
            "URL": submission.url,
            "Date": datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d'),
            "Username": submission.author.name if submission.author else None,
            "Source": "Reddit",
            "Platform_Type": "Forum",
            "Engagement": f"Upvotes: {submission.score}"
        })

    return results
