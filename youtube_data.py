import os
from googleapiclient.discovery import build

def scrape_youtube(min_results=100):
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    results = []
    next_page_token = None

    while len(results) < min_results:
        request = youtube.search().list(
            q="Burger King review",
            part="snippet",
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        video_ids = [
            item['id']['videoId'] for item in response.get("items", [])
            if item['id']['kind'] == "youtube#video"
        ]

        stats_response = youtube.videos().list(
            part="statistics",
            id=",".join(video_ids)
        ).execute()

        video_stats_map = {v['id']: v['statistics'] for v in stats_response.get('items', [])}

        for item in response.get("items", []):
            vid = item['id']['videoId']
            stats = video_stats_map.get(vid, {})
            results.append({
                "Product": None,
                "Price": None,
                "Type": None,
                "Location": None,
                "Review_Text": item["snippet"]["title"] + " - " + item["snippet"]["description"],
                "Hashtags": None,
                "URL": f"https://www.youtube.com/watch?v={vid}",
                "Date": item["snippet"]["publishedAt"],
                "Username": item["snippet"]["channelTitle"],
                "Source": "YouTube",
                "Platform_Type": "Video",
                "Engagement": f"Views: {stats.get('viewCount', '0')}, Likes: {stats.get('likeCount', '0')}"
            })

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return results[:min_results]
