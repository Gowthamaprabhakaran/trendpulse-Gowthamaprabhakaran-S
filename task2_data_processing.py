
import pandas as pd
import os
import glob

# ---------------------------------
# Step 1: Load the JSON file
# ---------------------------------

# Find the latest JSON file inside the data folder
json_files = glob.glob("data/trends_*.json")

if not json_files:
    raise FileNotFoundError("No JSON file found in the data folder.")

# Select the most recently modified JSON file
fletch_file = max(json_files, key=os.path.getmtime)

# Load JSON data into a Pandas DataFrame
df = pd.read_json(fletch_file)

# Print the number of rows loaded
print(f"Loaded {len(df)} stories from {fletch_file}")


# ---------------------------------
# Step 2: Remove duplicate stories
# ---------------------------------

# Remove duplicate rows based on post_id
df = df.drop_duplicates(subset="post_id", keep="first")

print(f"\nAfter removing duplicates: {len(df)}")


# ---------------------------------
# Step 3: Handle missing values
# ---------------------------------

# Remove rows where post_id, title, or score is missing
df = df.dropna(subset=["post_id", "title", "score"])

print(f"After removing nulls: {len(df)}")


# ---------------------------------
# Step 4: Clean data types
# ---------------------------------

# Convert score and num_comments to numeric values
df["score"] = pd.to_numeric(df["score"], errors="coerce")
df["num_comments"] = pd.to_numeric(
    df["num_comments"], errors="coerce"
)

# Remove rows where score is invalid
df = df.dropna(subset=["score"])

# Replace missing comment counts with 0
df["num_comments"] = df["num_comments"].fillna(0)

# Convert numeric columns to integers
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)


# ---------------------------------
# Step 5: Remove low-quality stories
# ---------------------------------

# Keep stories with a score of 5 or more
df = df[df["score"] >= 5]

print(f"After removing low scores: {len(df)}")


# ---------------------------------
# Step 6: Remove extra whitespace
# ---------------------------------

# Remove leading and trailing spaces from titles
df["title"] = df["title"].astype(str).str.strip()


# ---------------------------------
# Step 7: Save cleaned data as CSV
# ---------------------------------

# Create the data folder if it doesn't exist
os.makedirs("data", exist_ok=True)

output_file = "data/trends_clean.csv"

# Save without the DataFrame index
df.to_csv(output_file, index=False)

print(f"\nSaved {len(df)} rows to {output_file}")


# ---------------------------------
# Step 8: Print category summary
# ---------------------------------

print("\nStories per category:")

category_summary = df["category"].value_counts()

print(category_summary)