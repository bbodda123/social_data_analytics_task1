import pandas as pd
import argparse
import os
import re
from textblob import Word


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

# -----------------------------
# Load all CSV files dynamically
# -----------------------------

def load_data(folder):

    files = [f for f in os.listdir(folder) if f.endswith(".csv")]

    dfs = []

    for file in files:
        path = os.path.join(folder, file)
        df = pd.read_csv(path)
        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)


# -----------------------------
# Main Pipeline
# -----------------------------

def main():

    parser = argparse.ArgumentParser(description="Dynamic Text Preprocessing Pipeline")

    parser.add_argument("input", type=str.lower, help="Input folder containing CSV files")
    parser.add_argument("--output", type=str.lower, default="clean_data.csv")

    parser.add_argument("--lowercase", action="store_true")
    parser.add_argument("--remove_urls", action="store_true")
    parser.add_argument("--remove_special", action="store_true")
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

            if args.lemmatize:
                df[col] = df[col].apply(lemmatize_text)

    df.to_csv(args.output, index=False)

    print("Dataset cleaned successfully")
    print("Rows:", df.shape[0])


if __name__ == "__main__":
    main()