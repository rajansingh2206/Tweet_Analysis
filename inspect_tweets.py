import pandas as pd
from datetime import datetime, timedelta

DATA_PATH = "data/tweets.parquet"

def main():
    print(f"Loading tweets from {DATA_PATH}")
    df = pd.read_parquet(DATA_PATH)
    print(f"Total tweets collected: {len(df)}\n")

    # Show a random sample of 10 tweets with all key fields
    print("Sample tweets:")
    print(df[["username", "timestamp", "content", "likes", "retweets", "replies", "mentions", "hashtags", "source_hashtag"]].sample(min(10, len(df))).to_string(index=False))
    print("\n" + "="*60 + "\n")

    # Check how many tweets are from the last 24 hours
    now = pd.Timestamp.now(tz='UTC')
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", utc=True)
    last24h = now - pd.Timedelta(hours=24)
    recent = df[df["timestamp"] >= last24h]

    print(f"Tweets from the last 24 hours: {len(recent)}")
    if not recent.empty:
        print("Sample of recent tweets:")
        print(recent[["username", "timestamp", "content", "likes", "retweets", "replies", "mentions", "hashtags", "source_hashtag"]].sample(min(5, len(recent))).to_string(index=False))
    else:
        print("No tweets found from the last 24 hours.")

    print("\nField coverage check on all columns:")
    for col in ["username", "timestamp", "content", "likes", "retweets", "replies", "mentions", "hashtags"]:
        non_null = df[col].notnull().sum()
        print(f"  {col}: {non_null} non-null values out of {len(df)}")

if __name__ == "__main__":
    main()