
import pandas as pd
import numpy as np
import os

# ---------------------------------
# Step 1: Load the cleaned CSV file
# ---------------------------------

fletch_file = "data/trends_clean.csv"

# Load CSV data into a DataFrame
df = pd.read_csv(fletch_file)

# Print the shape of the DataFrame
print("Loaded data:", df.shape)


# ---------------------------------
# Step 2: Explore the data
# ---------------------------------

# Display the first 5 rows
print("\nFirst 5 rows:")
print(df.head())

# Calculate average score and comments
avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()

print(f"\nAverage score   : {avg_score:,.2f}")
print(f"Average comments: {avg_comments:,.2f}")


# ---------------------------------
# Step 3: NumPy statistical analysis
# ---------------------------------

# Convert score column into a NumPy array
scores = df["score"].to_numpy()

# Calculate mean, median, and standard deviation
mean = np.mean(scores)
median = np.median(scores)
std = np.std(scores)

# Find highest and lowest scores
max_score = np.max(scores)
min_score = np.min(scores)

print("\n--- NumPy Stats ---")
print(f"Mean score   : {mean:,.2f}")
print(f"Median score : {median:,.2f}")
print(f"Std deviation: {std:,.2f}")
print(f"Max score    : {max_score:,}")
print(f"Min score    : {min_score:,}")


# ---------------------------------
# Step 4: Find category with most stories
# ---------------------------------

# Count the number of stories in each category
category_counts = df["category"].value_counts()

# Get the category with the highest count
most_common_category = category_counts.idxmax()
most_common_count = category_counts.max()

print(
    f"\nMost stories in: {most_common_category} "
    f"({most_common_count} stories)"
)


# ---------------------------------
# Step 5: Find the most commented story
# ---------------------------------

# Find the index of the row with the highest comment count
most_commented_index = df["num_comments"].idxmax()

# Get the story details
most_commented_story = df.loc[most_commented_index]

print(
    f'\nMost commented story: '
    f'"{most_commented_story["title"]}" '
    f'— {most_commented_story["num_comments"]:,} comments'
)


# ---------------------------------
# Step 6: Add new columns
# ---------------------------------

# Engagement = comments divided by score + 1
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# Popular if score is greater than the average score
df["is_popular"] = df["score"] > avg_score


# ---------------------------------
# Step 7: Save the analysed CSV
# ---------------------------------

# Ensure the data folder exists
os.makedirs("data", exist_ok=True)

output_file = "data/trends_analysed.csv"

# Save the updated DataFrame
df.to_csv(output_file, index=False)

print(f"\nSaved to {output_file}")