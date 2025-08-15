import os
import time
import pandas as pd
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re

load_dotenv()

USERNAME = os.getenv("TWITTER_USERNAME")
PASSWORD = os.getenv("TWITTER_PASSWORD")
PHONE_OR_EMAIL = os.getenv("TWITTER_PHONE", None)
PROFILE_URL = os.getenv("TWITTER_PROFILE_URL")
TWEET_LIMIT = int(os.getenv("TWEET_LIMIT", 101))

def login(driver):
    driver.get("https://twitter.com/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "text")))

    user_input = driver.find_element(By.NAME, "text")
    user_input.send_keys(USERNAME)
    user_input.send_keys(Keys.ENTER)
    time.sleep(3)

    try:
        header_text = driver.find_element(By.TAG_NAME, "h1").text.lower()
        if "phone" in header_text or "email" in header_text:
            verify_input = driver.find_element(By.NAME, "text")
            verify_input.send_keys(PHONE_OR_EMAIL)
            verify_input.send_keys(Keys.ENTER)
            time.sleep(3)
    except:
        pass

    pass_input = driver.find_element(By.NAME, "password")
    pass_input.send_keys(PASSWORD)
    pass_input.send_keys(Keys.ENTER)
    time.sleep(5)

def scrape_twitter():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    login(driver)

    driver.get(PROFILE_URL)
    time.sleep(5)

    tweets_data = []
    seen_tweets = set()

    while len(tweets_data) < TWEET_LIMIT:
        WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, "//article[@data-testid='tweet']")))
        soup = BeautifulSoup(driver.page_source, "html.parser")
        tweets = soup.find_all("article", {"data-testid": "tweet"})

        for tweet in tweets:
            tweet_id = hash(tweet.get_text())
            if tweet_id in seen_tweets:
                continue
            seen_tweets.add(tweet_id)

            text_elem = tweet.find("div", {"data-testid": "tweetText"})
            tweet_text = text_elem.get_text(" ", strip=True) if text_elem else ""

            hashtags = []
            for a in tweet.find_all("a", href=True):
                if "/hashtag/" in a["href"]:
                    hashtags.append(a.get_text(strip=True).lstrip("#"))

            def get_count(label):
                btn = tweet.find(attrs={"data-testid": label})
                if btn:
                    spans = btn.find_all("span")
                    for span in spans[::-1]:
                        txt = span.get_text(strip=True)
                        if re.search(r"\d", txt):
                            return txt
                return "0"

            replies = get_count("reply")
            reposts = get_count("retweet")
            likes = get_count("like")

            views = "0"
            # Match span containing K/M numbers or digits next to 'Views'
            possible_views = tweet.find_all("span", string=re.compile(r"^\d+(\.\d+)?[KkMm]?$"))
            for v in possible_views:
                if v.find_parent("a") and "views" in v.find_parent("a").get("aria-label", "").lower():
                    views = v.get_text(strip=True)
                    break

            tweets_data.append({
                "Tweet": tweet_text,
                "Replies": replies,
                "Reposts": reposts,
                "Likes": likes,
                "Views": views,
                "Hashtags": ", ".join(set(hashtags)) if hashtags else ""
            })

            if len(tweets_data) >= TWEET_LIMIT:
                break

        driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
        time.sleep(3)

    driver.quit()
    return tweets_data

if __name__ == "__main__":
    data = scrape_twitter()
    os.makedirs("data", exist_ok=True)
    pd.DataFrame(data).to_csv("data/twitter_data.csv", index=False, encoding="utf-8")
    print(f"✅ Scraped {len(data)} tweets from {PROFILE_URL}")
