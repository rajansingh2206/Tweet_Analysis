# Tweet Analysis

## Overview
This project analyzes tweets related to financial markets (e.g., #nifty50, #sensex) to extract actionable quantitative signals for algorithmic trading. It involves scraping Twitter/X, converting text data into features, aggregating signals, and visualizing results, with a focus on memory efficiency and scalability.

## Features
- **Twitter Scraping:** Collects tweets for specified hashtags.
- **Text-to-Signal Conversion:** Extracts TF-IDF features and sentiment.
- **Memory-Efficient Analysis:** Uses sampling and chunking for large datasets.
- **Signal Aggregation:** Combines features into composite trading signals.
- **Visualization:** Generates informative plots for exploration and reporting.
- **Performance Optimized:** Supports concurrent processing and scalable data handling.

## Repository Structure

```plaintext
rajansingh2206/Tweet_Analysis
├── README.md
├── requirements.txt
├── .gitignore
├── src_scraper.py
├── src_analyze.py
├── analysis_and_insights.py
├── technical_overview.md
├── data/
│   └── tweets.parquet
├── analysis/
│   ├── signals.csv
│   ├── composite_signal_stats.txt
│   └── plots/
│       ├── engagement_distribution.png
│       ├── sentiment_distribution.png
│       └── ...
├── logs/
│   └── scraper.log
```

## Setup Instructions

### Requirements
- Python 3.10 or higher
- Chrome browser (for scraping)
- See `requirements.txt` for Python packages

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/rajansingh2206/Tweet_Analysis.git
    cd Tweet_Analysis
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. (Optional) Set up a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

### Usage

1. **Scrape Tweets**  
   Edit hashtags or scraping settings in `src/scraping.py` as needed, then run:
    ```bash
    python src/scraping.py
    ```
   This saves tweets to `data/tweets.parquet`.

2. **Analyze & Extract Signals**
    ```bash
    python src/analyze.py
    ```
   Signals and plots are saved to `analysis/`.

### Output

- **Raw tweets:** `data/tweets.parquet`
- **Signals/features:** `analysis/signals.csv`
- **Plots:** `analysis/plots/`
- **Composite signal stats:** `analysis/composite_signal_stats.txt`

## Sample Results

- See `analysis/plots/` for sample engagement and sentiment distributions.
- See `analysis/signals.csv` for extracted features.

> **Note:** The number of tweets collected depends on Twitter’s live hashtag activity and scraping constraints. If fewer tweets are available for a hashtag in a given 24-hour window, the script will collect as many as possible. This is a real-world limitation of public data sources.

## Contributing

Contributions are welcome! Please open issues or submit pull requests.

## License

MIT License
