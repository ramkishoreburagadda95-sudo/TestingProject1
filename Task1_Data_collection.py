# task1 data  Collection

import requests
import time
import json
import os
from datetime import datetime

headers = {"User-Agent": "TrendPulse/1.0"}

#Category keywords
categories = {
    "Technology": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports":["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"]
}

def get_category(title):
    title= title.lower()
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword.lower() in title:
                return category 
    return "None"

def fetch_data():
    url= "https://hacker-news.firebaseio.com/v0/topstories.json"
    ids = requests.get(url,headers=headers).json()[:500]
    collected = [] 
    category_count = {category: 0 for category in categories}  

    for id in ids:
        try:
            response= requests.get(f"https://hacker-news.firebaseio.com/v0/item/{id}.json",headers=headers)
            data=response.json()
            if not  data or 'title' not in data:
                continue
            category=get_category(data['title'])
            if category and category_count[category] < 25:
                story={
                    "post_id": data.get('id'),
                    "title": data.get('title'),
                    "category": category,
                    "score": data.get('score', 0),
                    "num_comments": data.get('descendants', 0),
                    "author": data.get('by'),
                    "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                collected.append(story)
                category_count[category] += 1
            if all(count >= 25 for count in category_count.values()):
                break
        except Exception as e:
            print(f"Error fetching story {id}: {e}")
    return collected
def save_json_data(data):
    os.makedirs("data", exist_ok=True)
    filename = f"data/hacker_news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"collected {len(data)} stories.saved to {filename}")
if __name__ == "__main__":
    data= fetch_data() 
    save_json_data(data)
print("no of stories collected:", len(data))
