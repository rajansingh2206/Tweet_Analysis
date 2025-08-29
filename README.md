# Indian Stock Market Tweet Intelligence System

## Overview

This project collects, processes, deduplicates, and analyzes real-time tweets about the Indian stock market, focusing on hashtags like **#nifty50**, **#sensex**, **#intraday**, and **#banknifty**. It handles large volumes efficiently, extracting trading signals from tweet content for algorithmic research.

---

## Features

- **Web scraping** of Twitter/X (no paid API required)
- **Handles anti-bot and rate limiting** (random delays, headless browser, error recovery)
- **Extracts:** username, timestamp, text, engagement (likes/retweets/replies), mentions, hashtags
- **Deduplication and Unicode handling** for Indian languages
- **Data storage** in Parquet format (efficient for big data)
- **Text-to-signal conversion:** TF-IDF, feature engineering
- **Memory-efficient visualization** (sampling for big data)
- **Scalable, modular, and production-ready codebase**
- **Logging and error handling**
- **Sample output and plots included**

---

## Project Structure

```
indian-market-tweet-intel/
├── README.md
├── requirements.txt
├── src/
│   ├── scraper.py
│   ├── analyze.py
│   ├── utils.py
│   └── config.py
├── data/
│   └── tweets.parquet
├── analysis/
│   ├── plots/
│   │   └── engagement_hist.png
│   └── signals.csv
├── logs/
│   └── scraper.log
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd indian-market-tweet-intel
```

### 2. Create Python Environment

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download ChromeDriver

- Download the [ChromeDriver](https://chromedriver.chromium.org/downloads) **matching your Chrome version**.
- Place the executable in your PATH or the project root.

---

## Usage

### 1. Scrape Tweets

```bash
python src/scraper.py
```
- Scrapes recent tweets for all target hashtags (~2000+ tweets total).
- Deduplicates, cleans, and saves to `data/tweets.parquet`.
- Logs activity in `logs/scraper.log`.

### 2. Analyze and Visualize

```bash
python src/analyze.py
```
- Loads `data/tweets.parquet`, processes text to signals (TF-IDF), and aggregates features.
- Outputs:
  - `analysis/signals.csv` (numeric features and confidence)
  - `analysis/plots/engagement_hist.png`

---

## Example Outputs

- **`data/tweets.parquet`**: Cleaned, deduplicated tweet dataset
- **`analysis/signals.csv`**: Quantitative trading signals
- **`analysis/plots/engagement_hist.png`**: Sample engagement plot

---

## Notes

- **No Twitter login is required** for public content. If you face a login wall, see README tips for Selenium login automation.
- Modular code: adjust hashtags or add feature engineering as needed.
- Handles Unicode and Indian languages in tweets.
- Production-level error handling and logging.

---

## Troubleshooting

- **If scraping fails** ("no tweets found" or errors): ensure ChromeDriver is installed, up to date, and matches Chrome version.
- **If Twitter requests login**: see Selenium login tips online or ask for a code snippet to handle login via Selenium.

---

## License

MIT License.
