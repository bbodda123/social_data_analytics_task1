# Text Preprocessing Pipeline

## Overview

This project provides a configurable text preprocessing pipeline for cleaning and preparing scraped review datasets. The script dynamically loads multiple CSV files from a folder of per-product review CSVs, attaches product metadata (including `category` taken from the parent `products.csv`), and applies optional preprocessing steps via command-line flags.

Key behaviors added recently:

- The loader now adds a `category` column to each review row by mapping the source filename to `products.csv` (parent folder).
- Stopword removal is available using NLTK English stopwords while preserving common negations so sentiment is not harmed.
- A `--dedupe` option removes duplicate reviews by `reviewer_id`, `review_body`, and `date`.

---

## Project Structure

```
project/
│
├── task2/
│   └── cleaning.py        # preprocessing script
├── task1/
│   └── scraping.ipynb     # scraper that creates per-product CSVs and products.csv
├── data/
│   ├── products.csv       # product metadata (name, avg_rating, category, ...)
│   └── reviews/
│       ├── Product_A.csv
│       └── Product_B.csv
```

---

## Requirements

- Python 3.8+
- pandas
- textblob
- nltk

---

## Installation

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
# or individually
pip install pandas textblob nltk
```

3. Download required NLTK data (stopwords):

```bash
python -m nltk.downloader stopwords
```

4. (Optional) Download TextBlob corpora if you use TextBlob lemmatization:

```bash
python -m textblob.download_corpora
```

---

## Usage

Run the preprocessing pipeline on a folder containing per-product review CSVs (the script will look for `products.csv` in the parent folder to infer `category`):

```bash
python task2/cleaning.py <reviews_folder> [flags]
```

Common flags:

- `--lowercase` : Lowercase text fields
- `--remove-urls` : Remove URLs from text
- `--remove-special` : Remove special characters
- `--remove-stopwords` : Remove English stopwords (NLTK) but preserve negations
- `--lemmatize` : Lemmatize text using TextBlob
- `--dedupe` : Drop duplicate reviews by `reviewer_id`, `review_body`, and `date`
- `--output <file>` : Output CSV path (default: `clean_data.csv`)

Example:

```bash
python task2/cleaning.py ./data/reviews \
	--lowercase --remove-urls --remove-special --remove-stopwords --lemmatize --dedupe \
	--output ./data/cleaned_reviews.csv
```

---

## Output

The script writes the cleaned, concatenated DataFrame to the file provided with `--output` (default `clean_data.csv`). The DataFrame will include the appended `category` column (may be `null` if no mapping was found).

If you want per-product review CSVs, the scraper (task1) already produces `data/reviews/<product>.csv` files; `cleaning.py` expects the input folder to contain those CSV files.

---

## Notes and recommendations

- Stopword removal uses NLTK's English stopwords set, with common negations removed from the set so they remain in the text for sentiment analysis.
- The `--dedupe` flag runs a `drop_duplicates` on the concatenated DataFrame using `reviewer_id`, `review_body`, and `date` to filter repeated entries.
- If your filenames differ from the sanitization used by the scraper, the `category` mapping may not match; check `products.csv` and the review filenames.

---

## Author

Abdelrahman Hassan Metwally
