import os
import pandas as pd
from dotenv import load_dotenv

from burgerking_website import scrape_burgerking_products
from youtube_data import scrape_youtube
from reddit_data import scrape_reddit
from twitter_data import scrape_twitter
from instagram_data import scrape_instagram_posts

if __name__ == "__main__":
    load_dotenv()
    os.makedirs("data", exist_ok=True)

    # # 1️⃣ Burger King Website
    # bk_data = scrape_burgerking_products()
    # pd.DataFrame(bk_data).to_csv("data/burgerking_website.csv", index=False, encoding="utf-8")
    # print(f"✅ Burger King Website data saved with {len(bk_data)} rows")

    # # 2️⃣ YouTube
    # yt_data = scrape_youtube()
    # pd.DataFrame(yt_data).to_csv("data/youtube_data.csv", index=False, encoding="utf-8")
    # print(f"✅ YouTube data saved with {len(yt_data)} rows")

    # # 3️⃣ Reddit
    # reddit_data = scrape_reddit()
    # pd.DataFrame(reddit_data).to_csv("data/reddit_data.csv", index=False, encoding="utf-8")
    # print(f"✅ Reddit data saved with {len(reddit_data)} rows")

    # 4️⃣ Twitter
    twitter_data = scrape_twitter()
    pd.DataFrame(twitter_data).to_csv("data/twitter_data.csv", index=False, encoding="utf-8")
    print(f"✅ Twitter data saved with {len(twitter_data)} rows")

    # 5️⃣ Instagram
    # insta_data = scrape_instagram_posts()
    # pd.DataFrame(insta_data).to_csv("data/instagram_data.csv", index=False, encoding="utf-8")
    # print(f"✅ Instagram data saved with {len(insta_data)} rows")