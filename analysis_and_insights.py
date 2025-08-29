import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import TextBlob

# 1. Load tweets
df = pd.read_parquet('data/tweets.parquet')

# 2. Text-to-signal: TF-IDF feature extraction
tfidf = TfidfVectorizer(max_features=50)
tfidf_matrix = tfidf.fit_transform(df['content'].fillna(""))
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf.get_feature_names_out())

# Optionally, add custom features (e.g., sentiment)
df['sentiment'] = df['content'].fillna("").apply(lambda x: TextBlob(x).sentiment.polarity)

# 3. Memory-efficient visualization: sample 100 tweets
sample_idx = np.random.choice(len(df), size=min(100, len(df)), replace=False)
sample_tfidf = tfidf_df.iloc[sample_idx]
sample_sentiment = df['sentiment'].iloc[sample_idx]

plt.figure(figsize=(10,5))
plt.hist(sample_sentiment, bins=20, alpha=0.7)
plt.title("Sentiment Distribution (Sampled)")
plt.xlabel("Sentiment Polarity")
plt.ylabel("Tweet Count")
plt.tight_layout()
plt.savefig('analysis/plots/sentiment_distribution.png')
plt.close()

# 4. Signal Aggregation: Composite signal
# Example: composite = 0.7*sentiment + 0.3*TF-IDF score for 'buy'
if 'buy' in tfidf_df.columns:
    df['composite_signal'] = 0.7*df['sentiment'] + 0.3*tfidf_df['buy']
else:
    df['composite_signal'] = df['sentiment']

# Compute confidence intervals
mean_signal = df['composite_signal'].mean()
std_signal = df['composite_signal'].std()
ci_low, ci_high = np.percentile(df['composite_signal'], [2.5, 97.5])

# Plot composite signal
plt.figure(figsize=(10,5))
df['composite_signal'].sample(n=min(100, len(df)), random_state=42).hist(bins=20)
plt.title("Composite Signal Distribution (Sampled)")
plt.xlabel("Composite Signal Value")
plt.ylabel("Tweet Count")
plt.tight_layout()
plt.savefig('analysis/plots/composite_signal_distribution.png')
plt.close()

# Save confidence intervals and stats
with open('analysis/composite_signal_stats.txt', 'w') as f:
    f.write(f"Mean: {mean_signal:.3f}\nStd: {std_signal:.3f}\n95% CI: [{ci_low:.3f}, {ci_high:.3f}]\n")