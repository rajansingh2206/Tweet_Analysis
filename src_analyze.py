import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
import os
os.makedirs("analysis/plots", exist_ok=True)
DATA_PATH = "data/tweets.parquet"
SIGNALS_PATH = "analysis/signals.csv"
PLOTS_DIR = "analysis/plots/"

def text_to_signal(texts):
    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(
        max_features=128,
        strip_accents='unicode',
        token_pattern=r"(?u)\b\w\w+\b"
    )
    X = vectorizer.fit_transform(texts)
    return X, vectorizer

def plot_engagement(df):
    plt.figure(figsize=(8,6))
    sample = df.sample(min(500, len(df)))
    plt.hist(sample['likes'].astype(int), bins=20, alpha=0.7, label="Likes")
    plt.hist(sample['retweets'].astype(int), bins=20, alpha=0.7, label="Retweets")
    plt.legend()
    plt.xlabel("Count")
    plt.title("Engagement Distribution (Sampled)")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "engagement_hist.png"))
    plt.close()

def main():
    if not os.path.exists(PLOTS_DIR):
        os.makedirs(PLOTS_DIR)
    df = pd.read_parquet(DATA_PATH)
    # Basic Cleaning
    df['content'] = df['content'].astype(str).str.replace('\n', ' ').str.strip()
    df = df[df['content'] != '']

    # Numeric signals from text
    X, vectorizer = text_to_signal(df['content'])
    signals = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())
    signals["likes"] = df["likes"].astype(int)
    signals["retweets"] = df["retweets"].astype(int)
    signals["replies"] = df["replies"].astype(int)
    signals["confidence"] = signals.iloc[:,:-3].sum(axis=1) / (signals["likes"] + signals["retweets"] + 1)

    # Save signals
    signals.to_csv(SIGNALS_PATH, index=False)
    print(f"Signals saved to {SIGNALS_PATH}")

    # Visualize
    plot_engagement(df)
    print(f"Plots saved to {PLOTS_DIR}")

if __name__ == "__main__":
    main()