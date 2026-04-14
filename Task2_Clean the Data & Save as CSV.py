import pandas as pd
import os
# Load Json File
file_path = "data/hacker_news_20260414_215754.json" 
df = pd.read_json(file_path)
print("Rows loaded:", len(df))

# Remove duplicates based on post_id
df = df.drop_duplicates(subset="post_id")

# Drop missing values
df = df.dropna(subset=["post_id", "title", "score"])

# Convert data types
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# Remove low quality (score < 5)
df = df[df["score"] >= 5]

# Remove whitespace from title
df["title"] = df["title"].str.strip()

print("Rows after cleaning:", len(df))


# SAVE AS CSV
os.makedirs("data", exist_ok=True)

output_file = "data/trends_clean.csv"
df.to_csv(output_file, index=False)

print(f"Saved cleaned data to {output_file}")
print("Total rows saved:", len(df))
print("\nStories per category:")
print(df["category"].value_counts())

