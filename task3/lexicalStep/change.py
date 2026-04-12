import pandas as pd

# Load your dataset
df = pd.read_csv("output.csv")

# Columns to process
cols = ["bing_prediction", "swn_prediction"]

# Rows before cleaning
before_rows = len(df)

# Keep only rows where BOTH columns are 'positive' or 'negative'
df_clean = df[
    df["bing_prediction"].isin(["positive", "negative"]) &
    df["swn_prediction"].isin(["positive", "negative"])
].copy()

# Rows after cleaning
after_rows = len(df_clean)
deleted_rows = before_rows - after_rows

# Convert values: negative -> 0, positive -> 1
mapping = {
    "negative": 0,
    "positive": 1
}

for col in cols:
    df_clean[col] = df_clean[col].map(mapping)

# Count values
print("===== Data Summary =====")
print(f"Total rows before cleaning: {before_rows}")
print(f"Total rows after cleaning: {after_rows}")
print(f"Deleted rows: {deleted_rows}")
print("------------------------")

for col in cols:
    counts = df_clean[col].value_counts()
    ones = counts.get(1, 0)
    zeros = counts.get(0, 0)

    print(f"\nColumn: {col}")
    print(f"1 (positive): {ones}")
    print(f"0 (negative): {zeros}")

# Optional: save cleaned data
df_clean.to_csv("cleaned_data_numeric.csv", index=False)