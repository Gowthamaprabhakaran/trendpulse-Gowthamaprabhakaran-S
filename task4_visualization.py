import pandas as pd
import matplotlib.pyplot as plt
import os


# --------------------------------------------------
# Load data
# --------------------------------------------------

df = pd.read_csv("data/trends_analysed.csv")

# Create outputs folder if it does not exist
os.makedirs("outputs", exist_ok=True)


# ==================================================
# CHART 1: Top 10 Stories by Score
# ==================================================

top_10 = df.sort_values("score", ascending=False).head(10).copy()

# Shorten long titles to 50 characters
top_10["short_title"] = top_10["title"].apply(
    lambda title: title[:50] + "..." if len(title) > 50 else title
)

plt.figure(figsize=(10, 6))

plt.barh(
    top_10["short_title"],
    top_10["score"]
)

# Highest score should appear at the top
plt.gca().invert_yaxis()

plt.title("Top 10 Stories by Score")
plt.xlabel("Score")
plt.ylabel("Story Title")

plt.tight_layout()

# Save before showing
plt.savefig("outputs/chart1_top_stories.png")

plt.show()
plt.close()


# ==================================================
# CHART 2: Stories per Category
# ==================================================

category_counts = df["category"].value_counts()

plt.figure(figsize=(8, 5))

# Give each bar a different colour
colors = plt.cm.tab10(range(len(category_counts)))

plt.bar(
    category_counts.index,
    category_counts.values,
    color=colors
)

plt.title("Stories per Category")
plt.xlabel("Category")
plt.ylabel("Number of Stories")

# Rotate category names for better readability
plt.xticks(rotation=30)

plt.tight_layout()

# Save before showing
plt.savefig("outputs/chart2_categories.png")

plt.show()
plt.close()


# ==================================================
# CHART 3: Score vs Number of Comments
# ==================================================

non_popular = df[df["is_popular"] == False]
popular = df[df["is_popular"] == True]

plt.figure(figsize=(9, 6))

plt.scatter(
    non_popular["score"],
    non_popular["num_comments"],
    label="Not Popular"
)

plt.scatter(
    popular["score"],
    popular["num_comments"],
    label="Popular"
)

plt.title("Score vs Comments")
plt.xlabel("Score")
plt.ylabel("Number of Comments")

plt.legend()

plt.tight_layout()

# Save before showing
plt.savefig("outputs/chart3_scatter.png")

plt.show()
plt.close()


# ==================================================
# BONUS: TRENDPULSE DASHBOARD
# ==================================================

fig, axes = plt.subplots(2, 2, figsize=(16, 10))


# --------------------------------------------------
# Dashboard Chart 1: Top 10 Stories
# --------------------------------------------------

axes[0, 0].barh(
    top_10["short_title"],
    top_10["score"]
)

axes[0, 0].invert_yaxis()

axes[0, 0].set_title("Top 10 Stories by Score")
axes[0, 0].set_xlabel("Score")
axes[0, 0].set_ylabel("Story Title")


# --------------------------------------------------
# Dashboard Chart 2: Stories per Category
# --------------------------------------------------

axes[0, 1].bar(
    category_counts.index,
    category_counts.values,
    color=colors
)

axes[0, 1].set_title("Stories per Category")
axes[0, 1].set_xlabel("Category")
axes[0, 1].set_ylabel("Number of Stories")

axes[0, 1].tick_params(axis="x", rotation=30)


# --------------------------------------------------
# Dashboard Chart 3: Score vs Comments
# --------------------------------------------------

axes[1, 0].scatter(
    non_popular["score"],
    non_popular["num_comments"],
    label="Not Popular"
)

axes[1, 0].scatter(
    popular["score"],
    popular["num_comments"],
    label="Popular"
)

axes[1, 0].set_title("Score vs Comments")
axes[1, 0].set_xlabel("Score")
axes[1, 0].set_ylabel("Number of Comments")

axes[1, 0].legend()


# --------------------------------------------------
# Empty fourth section
# --------------------------------------------------

axes[1, 1].axis("off")


# Overall dashboard title
fig.suptitle(
    "TrendPulse Dashboard",
    fontsize=18
)

plt.tight_layout()

# Save dashboard
plt.savefig("outputs/dashboard.png")

plt.show()
plt.close()


print("Task 4 completed successfully.")
print("Charts saved in the outputs folder.")