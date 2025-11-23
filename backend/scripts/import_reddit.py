import json, requests, uuid

API_URL = "http://127.0.0.1:5000/api/queries"
FILE = "reddit_pic_programming.json"

raw = json.load(open(FILE))

# The posts are inside: raw["data"]["children"]
posts = raw.get("data", {}).get("children", [])

for post in posts:
    entry = post.get("data", {})
    
    payload = {
        "title": entry.get("title", ""),
        "content": entry.get("selftext", ""),
        "source": f"reddit/{entry.get('subreddit', '')}",
        "url": entry.get("url", ""),
        "timestamp": entry.get("created_utc"),
        "comments_count": entry.get("num_comments", 0)
    }

    r = requests.post(API_URL, json=payload)
    print("Uploaded:", payload["title"], "Status:", r.status_code)
