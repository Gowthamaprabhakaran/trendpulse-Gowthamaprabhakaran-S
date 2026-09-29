
import requests
import time
import json
import os
from datetime import datetime

# -------------------------------
# Configuration
# -------------------------------

URL = "https://hacker-news.firebaseio.com/v0"
HEADERS = {"User-Agent": "TrendPulse/1.0"}

MAXI_STORIES = 500
LIMIT_PER_CATEGORY = 25

# Keywords used to categorize stories
categories = {
    "technology": [
        "AI", "software", "tech", "code", "computer",
        "data", "cloud", "API", "GPU", "LLM"
    ],
    "worldnews": [
        "war", "government", "country", "president",
        "election", "climate", "attack", "global"
    ],
    "sports": [
        "NFL", "NBA", "FIFA", "sport", "game", "team",
        "player", "league", "championship"
    ],
    "science": [
        "research", "study", "space", "physics",
        "biology", "discovery", "NASA", "genome"
    ],
    "entertainment": [
        "movie", "film", "music", "Netflix", "game",
        "book", "show", "award", "streaming"
    ]
}


# -------------------------------
# Step 1: Fetch top story IDs
# -------------------------------

def fetch_top_story_ids():
    url = f"{URL}/topstories.json"

    try:
        response = requests.get(
            url, headers=HEADERS, timeout=15
        )
        response.raise_for_status()

        # Return only the first 500 story IDs
        return response.json()[:MAXI_STORIES]

    except requests.RequestException as e:
        print(f"Failed to fetch story IDs: {e}")
        return []


# -------------------------------
# Step 2: Fetch story details
# -------------------------------

def fetch_story(story_id):
    url = f"{URL}/item/{story_id}.json"

    try:
        response = requests.get(
            url, headers=HEADERS, timeout=15
        )
        response.raise_for_status()

        return response.json()

    except requests.RequestException as e:
        print(f"Failed to fetch story {story_id}: {e}")
        return None


# -------------------------------
# Step 3: Categorize a story
# -------------------------------

def categorize_story(title):
    title_lower = title.lower()

    # Check each category's keywords
    for category, keywords in categories.items():
        for key in keywords:
            if key.lower() in title_lower:
                return category

    # Ignore stories that do not match any category
    return None


# -------------------------------
# Step 4: Collect stories
# -------------------------------

def collect_stories():
    story_ids = fetch_top_story_ids()

    # Create an empty list for each category
    collected = {
        category: [] for category in categories
    }

    for id in story_ids:

        # Stop when all categories reach 25 stories
        if all(
            len(stories) >= LIMIT_PER_CATEGORY
            for stories in collected.values()
        ):
            break

        story = fetch_story(id)

        if not story:
            continue

        # Skip items without a title
        title = story.get("title", "")

        if not title:
            continue

        category = categorize_story(title)

        # Skip stories without a matching category
        if category is None:
            continue

        # Skip categories that already have 25 stories
        if len(collected[category]) >= LIMIT_PER_CATEGORY:
            continue

        # Prepare the required 7 fields
        story_data = {
            "post_id": story.get("id"),
            "title": title,
            "category": category,
            "score": story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author": story.get("by", "unknown"),
            "collected_at": datetime.now().isoformat(
                timespec="seconds"
            )
        }

        collected[category].append(story_data)

        print(f"Collected: {title} -> {category}")

        # Wait 2 seconds after completing each category
        # (not after every individual story request)
        if len(collected[category]) == LIMIT_PER_CATEGORY:
            print(f"Category completed: {category}")
            time.sleep(2)

    # Combine all categories into one list
    all_stories = []

    for stories in collected.values():
        all_stories.extend(stories)

    return all_stories


# -------------------------------
# Step 5: Save stories to JSON
# -------------------------------

def save_to_json(stories):
    # Create data folder if it doesn't exist
    os.makedirs("data", exist_ok=True)

    # Create filename using today's date
    today = datetime.now().strftime("%Y%m%d")
    filename = f"data/trends_{today}.json"

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(
            stories,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"Collected {len(stories)} stories. "
        f"Saved to {filename}"
    )


# -------------------------------
# Main program
# -------------------------------


stories = collect_stories()
save_to_json(stories)