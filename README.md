# Social Data Analytics – Task 1

A Walmart product-review scraper built with Selenium and `undetected_chromedriver`.
It visits Walmart review pages, collects up to 150 reviews per product, and saves everything locally as CSV files for downstream analysis.

---

## Requirements

- Python 3.11+
- Google Chrome (used by the Selenium driver)

---

## Installation

### Using uv (recommended)

```bash
uv sync
```

### Using pip

```bash
pip install -r requirements.txt
```

---

## Getting Started

Open the notebook and run the cells from top to bottom:

```bash
jupyter notebook task1.ipynb
```

Before running, you can edit the `PRODUCT_URLS` list in the notebook to point at any Walmart review pages you want to scrape, and adjust `MAX_REVIEWS_PER_PRODUCT` if needed.

---

## Data Storage

All scraped data is written to the `scraped_data/` directory.

```
scraped_data/
├── products.csv                   # One row per product (name, avg rating, review count, star distribution)
└── <Product_Name>/
    └── reviews.csv                # One row per review (rating, reviewer id, date, title, body)
```

### `products.csv` columns

| Column | Description |
|--------|-------------|
| `name` | Product name |
| `avg_rating` | Average star rating |
| `num_of_reviews` | Total number of reviews scraped |
| `one_star` – `five_star` | Count of reviews at each star level |

### `reviews.csv` columns (per product folder)

| Column | Description |
|--------|-------------|
| `rating` | Star rating given by the reviewer |
| `reviewer_id` | Reviewer username or identifier |
| `date` | Date the review was posted |
| `review_title` | Short title of the review |
| `review_body` | Full review text |

---

## Project Structure

```
.
├── task1.ipynb        # Main scraping notebook
├── scraped_data/      # Output directory (see above)
├── pyproject.toml     # Project metadata and dependencies (uv)
├── requirements.txt   # Pinned dependencies (pip)
├── uv.lock            # Locked dependency graph (uv)
└── .python-version    # Pinned Python version (3.11)
```

---

## License

This project is for educational purposes.
