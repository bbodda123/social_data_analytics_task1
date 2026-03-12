import pandas as pd
import argparse
import os
import re
from textblob import Word
from pathlib import Path
import nltk


# -----------------------------
# Cleaning Functions
# -----------------------------


def to_lowercase(text):
    return str(text).lower()


def remove_urls(text):
    return re.sub(r"http\S+|www\S+", "", str(text))


def remove_special_chars(text):
    return re.sub(r"[^a-zA-Z0-9\s]", "", str(text))


def lemmatize_text(text):
    words = str(text).split()
    return " ".join([Word(w).lemmatize("v") for w in words])


# Keep these negations because they affect sentiment
NEGATIONS = {
    "no",
    "not",
    "nor",
    "never",
    "none",
    "n't",
    "nothing",
    "nowhere",
    "neither",
    "cannot",
}

# Load NLTK English stopwords, falling back to download if necessary
try:
    from nltk.corpus import stopwords

    NLTK_STOPWORDS = set(stopwords.words("english"))
except Exception:
    nltk.download("stopwords")
    from nltk.corpus import stopwords

    NLTK_STOPWORDS = set(stopwords.words("english"))

# Final stopwords set (remove negations so sentiment is preserved)
STOPWORDS = NLTK_STOPWORDS - {s.lower() for s in NEGATIONS}


def remove_stopwords(text):
    if pd.isna(text):
        return text
    tokens = str(text).split()
    filtered = []
    for tok in tokens:
        key = re.sub(r"[^a-zA-Z0-9'-]", "", tok).lower()
        if not key:
            continue
        if key in NEGATIONS or key not in STOPWORDS:
            filtered.append(tok)
    return " ".join(filtered)


# -----------------------------
# Load all CSV files dynamically
# -----------------------------


def load_data(folder):
    files = [f for f in os.listdir(folder) if f.endswith(".csv")]
    dfs = []

    # Attempt to load products.csv from parent folder to map filename -> category
    prod_map = {}
    products_path = Path(folder).parent / "products.csv"

    prod_df = pd.read_csv(products_path)
    for i in range(len(prod_df)):
        row = prod_df.iloc[i]
        prod_map[row["name"].lower()] = row["category"].lower()

    for file in files:
        path = os.path.join(folder, file)
        df = pd.read_csv(path)

        # infer category from filename using products.csv mapping
        fname = file.split(".")[0].lower()
        category = prod_map.get(fname)
        # attach category column
        df["category"] = category

        dfs.append(df)

    if not dfs:
        return pd.DataFrame()
    return pd.concat(dfs, ignore_index=True)


# -----------------------------
# Main Pipeline
# -----------------------------


def main():

    parser = argparse.ArgumentParser(description="Dynamic Text Preprocessing Pipeline")

    parser.add_argument(
        "input", type=str.lower, help="Input folder containing CSV files"
    )
    parser.add_argument("--output", type=str.lower, default="clean_data.csv")

    parser.add_argument("--lowercase", action="store_true")
    parser.add_argument("--remove-urls", action="store_true")
    parser.add_argument("--remove-special", action="store_true")
    parser.add_argument("--remove-stopwords", action="store_true")
    parser.add_argument(
        "--dedupe",
        action="store_true",
    )
    parser.add_argument("--lemmatize", action="store_true")

    args = parser.parse_args()

    df = load_data(args.input)

    # Columns we want to process
    target_columns = ["reviewer_id", "review_title", "review_body"]

    for col in target_columns:

        if col in df.columns:

            if args.lowercase:
                df[col] = df[col].apply(to_lowercase)

            if args.remove_urls:
                df[col] = df[col].apply(remove_urls)

            if args.remove_special:
                df[col] = df[col].apply(remove_special_chars)

            if args.remove_stopwords:
                df[col] = df[col].apply(remove_stopwords)

            if args.lemmatize:
                df[col] = df[col].apply(lemmatize_text)

    df.to_csv(args.output, index=False)

    if args.dedupe:
        before = df.shape[0]
        df.drop_duplicates(subset=["reviewer_id", "review_body", "date"], inplace=True)
        after = df.shape[0]
        print(f"Removed {before - after} duplicate rows")
        df.to_csv(args.output, index=False)

    print("Dataset cleaned successfully")
    print("Rows:", df.shape[0])


if __name__ == "__main__":
    main()
