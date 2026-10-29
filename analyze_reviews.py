import pandas as pd
from pathlib import Path
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load the cleaned dataset
folder = Path(__file__).parent
df = pd.read_csv(folder / "amazon_reviews_cleaned.csv")

# Initialize sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Analyze review text
def analyze_sentiment(text):
    if pd.isna(text) or not str(text).strip():
        return "Neutral"

    score = analyzer.polarity_scores(str(text))["compound"]

    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# Apply sentiment analysis
df["sentiment"] = df["text"].apply(analyze_sentiment)

# Display sentiment counts
print("\nAMAZON REVIEWS SENTIMENT ANALYSIS")
print("-" * 40)
print("\nSentiment Distribution:")
print(df["sentiment"].value_counts())

# Calculate percentages
print("\nSentiment Percentages:")
print((df["sentiment"].value_counts(normalize=True) * 100).round(2))

# Save results
output_file = folder / "amazon_reviews_sentiment.csv"
df.to_csv(output_file, index=False, encoding="utf-8-sig")

print("\nSentiment analysis completed!")
print("Results saved to:", output_file)