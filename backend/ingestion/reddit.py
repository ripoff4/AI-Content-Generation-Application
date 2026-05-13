import requests
from datetime import datetime, timedelta


def get_reddit_trending_information(
    topic: str,
    days: int = 3,
    limit: int = 15
):

    headers = {
        "User-Agent": "TrendIntelligenceBot/1.0"
    }

    url = (
        f"https://www.reddit.com/search.json"
        f"?q={topic}"
        f"&sort=new"
        f"&limit={limit}"
    )

    response = requests.get(
        url,
        headers=headers
    )

    data = response.json()

    posts = data["data"]["children"]

    filtered_posts = []

    cutoff_time = datetime.utcnow() - timedelta(days=days)

    for post in posts:

        post_data = post["data"]

        created_utc = post_data.get("created_utc")

        if not created_utc:
            continue

        post_date = datetime.utcfromtimestamp(created_utc)

        if post_date >= cutoff_time:

            title = post_data.get("title", "")

            selftext = post_data.get("selftext", "")

            subreddit = post_data.get("subreddit", "")

            score = post_data.get("score", 0)

            post_url = (
                f"https://www.reddit.com"
                f"{post_data.get('permalink', '')}"
            )

            if score < 10:
                continue

            filtered_posts.append({
                "title": title,
                "content": selftext,
                "subreddit": subreddit,
                "score": score,
                "url": post_url,
                "created_utc": created_utc
            })

    filtered_posts.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return filtered_posts
