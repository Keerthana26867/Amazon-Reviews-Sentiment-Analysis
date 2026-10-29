
import pandas as pd
import json
import re
from pathlib import Path

# File paths
input_file = Path(__file__).parent / "Gift_Cards.jsonl"
output_file = Path(__file__).parent / "amazon_reviews_cleaned.csv"

reviews = []

# Read JSONL file
with open(input_file, "r", encoding="utf-8") as file:
    for line in file:
        try:
            reviews.append(json.loads(line))
        except json.JSONDecodeError:
            continue

# Convert to DataFrame
df = pd.DataFrame(reviews)

# Keep useful columns that exist in the dataset
columns = ["rating", "title", "text", "timestamp", "asin"]
df = df[[col for col in columns if col in df.columns]].copy()

# Remove duplicate reviews
df.drop_duplicates(inplace=True)

# Remove rows without review text
if "text" in df.columns:
    df.dropna(subset=["text"], inplace=True)
    df["text"] = df["text"].astype(str).str.strip()
    df = df[df["text"] != ""]

# Clean review text
def clean_text(text):
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

if "text" in df.columns:
    df["text"] = df["text"].apply(clean_text)

# Save cleaned dataset
df.to_csv(output_file, index=False, encoding="utf-8-sig")

print("Cleaning completed successfully!")
print("Total reviews after cleaning:", len(df))
print("Saved file:", output_file)
