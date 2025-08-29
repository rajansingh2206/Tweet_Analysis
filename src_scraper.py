import os
import time
import logging
from datetime import datetime, timedelta
import pandas as pd
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

HASHTAGS = ["#nifty50", "#sensex", "#intraday", "#banknifty"]
MIN_TWEETS = 2000
DATA_PATH = "data/tweets.parquet"
LOG_PATH = "logs/scraper.log"

def setup_logging():
    if not os.path.exists("logs"):
        os.makedirs("logs")
    logging.basicConfig(
        filename=LOG_PATH,
        filemode="a",
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO
    )
    logging.getLogger().addHandler(logging.StreamHandler())

def get_driver():
    chrome_options = Options()
    # Remove headless so user can log in manually
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def wait_for_login(driver):
    print("\n*** Please log in to Twitter/X in the opened browser window. ***")
    print("After successful login, press Enter in this terminal to continue...")
    driver.get("https://twitter.com/login")
    input()
    print("Continuing with scraping...")

def scroll_and_collect(hashtag, driver, max_tweets):
    url = f"https://twitter.com/search?q={hashtag}%20lang%3Aen&src=typed_query&f=live"
    driver.get(url)
    time.sleep(5)
    tweets = []
    last_height = driver.execute_script("return document.body.scrollHeight")
    pbar = tqdm(total=max_tweets, desc=f"Scraping {hashtag}")
    scraped_ids = set()
    fail_count = 0

    while len(tweets) < max_tweets and fail_count < 10:
        cards = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')
        if not cards:
            print("WARNING: No tweet cards found. Check if Twitter is asking for login or blocking you.")
            print("Page source (first 1000 chars):\n", driver.page_source[:1000])
            logging.warning("No tweet cards found for %s", hashtag)
            fail_count += 1
            time.sleep(3)
            continue
        for card in cards:
            try:
                tweet_id = card.get_attribute("data-tweet-id") or card.get_attribute("id")
                if tweet_id and tweet_id in scraped_ids:
                    continue
                # Username
                username_elem = card.find_element(By.XPATH, './/div[@data-testid="User-Name"]//span')
                username = username_elem.text if username_elem else ""
                # Timestamp
                time_elem = card.find_element(By.XPATH, './/time')
                timestamp = time_elem.get_attribute("datetime") if time_elem else ""
                # Content
                content_elem = card.find_element(By.XPATH, './/div[@data-testid="tweetText"]')
                content = content_elem.text if content_elem else ""
                # Engagement
                stats = card.find_elements(By.XPATH, './/div[@data-testid="like"] | .//div[@data-testid="retweet"] | .//div[@data-testid="reply"]')
                likes = stats[0].text if len(stats) > 0 else "0"
                retweets = stats[1].text if len(stats) > 1 else "0"
                replies = stats[2].text if len(stats) > 2 else "0"
                # Mentions/hashtags
                mentions = [e.text for e in card.find_elements(By.XPATH, './/a[contains(@href, "/")]/span') if e.text.startswith('@')]
                hashtags = [e.text for e in card.find_elements(By.XPATH, './/a/span') if e.text.startswith('#')]
                tweets.append({
                    "username": username,
                    "timestamp": timestamp,
                    "content": content,
                    "likes": likes,
                    "retweets": retweets,
                    "replies": replies,
                    "mentions": mentions,
                    "hashtags": hashtags,
                    "source_hashtag": hashtag
                })
                if tweet_id:
                    scraped_ids.add(tweet_id)
                pbar.update(1)
                if len(tweets) >= max_tweets:
                    break
            except Exception as e:
                logging.error(f"Error parsing tweet card: {e}")
                continue
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            fail_count += 1  # No more new tweets loaded
            time.sleep(2)
        else:
            fail_count = 0
        last_height = new_height
    pbar.close()
    return tweets

def main():
    setup_logging()
    if not os.path.exists("data"):
        os.makedirs("data")
    driver = get_driver()
    wait_for_login(driver)
    all_tweets = []
    for h in HASHTAGS:
        tweets = scroll_and_collect(h, driver, MIN_TWEETS // len(HASHTAGS))
        all_tweets.extend(tweets)
    driver.quit()

    if not all_tweets or len(all_tweets) == 0:
        print("No tweets collected. Please check your login and selectors.")
        logging.error("No tweets collected for any hashtag.")
        return

    df = pd.DataFrame(all_tweets)
    if "timestamp" not in df.columns or df.empty:
        print("No tweets collected or 'timestamp' column missing.")
        logging.error("No tweets or missing timestamp column.")
        return
    # Deduplicate
    df = df.drop_duplicates(subset=["username", "timestamp", "content"])
    # Clean timestamps
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    # Save as Parquet
    df.to_parquet(DATA_PATH, index=False)
    print(f"Saved {len(df)} tweets to {DATA_PATH}")
    logging.info("Saved %d tweets to %s", len(df), DATA_PATH)

if __name__ == "__main__":
    main()