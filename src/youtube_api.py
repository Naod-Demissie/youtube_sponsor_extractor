"""
YouTube API related functions for fetching video information
"""
import re
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from constants import YOUTUBE_API_KEY

def extract_video_id(url):
    """Extract video ID from YouTube URL."""
    patterns = [r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", r"youtu\.be\/([0-9A-Za-z_-]{11})"]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def fetch_youtube_description(youtube_url):
    """Fetch the description of a YouTube video using the YouTube Data API."""
    if not YOUTUBE_API_KEY:
        raise ValueError("YouTube API key not found in .env file")

    video_id = extract_video_id(youtube_url)
    if not video_id:
        raise ValueError("Invalid YouTube URL")

    try:
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        request = youtube.videos().list(part="snippet", id=video_id)
        response = request.execute()

        if "items" in response and len(response["items"]) > 0:
            return response["items"][0]["snippet"]["description"]
        return None
    except HttpError as e:
        raise Exception(f"YouTube API error: {str(e)}")

def get_video_details(youtube_url):
    """Fetch full video details including title and description."""
    if not YOUTUBE_API_KEY:
        raise ValueError("YouTube API key not found in .env file")
        
    video_id = extract_video_id(youtube_url)
    if not video_id:
        raise ValueError("Invalid YouTube URL")
        
    try:
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        request = youtube.videos().list(part="snippet", id=video_id)
        response = request.execute()
        
        if "items" in response and len(response["items"]) > 0:
            snippet = response["items"][0]["snippet"]
            return {
                "title": snippet["title"],
                "description": snippet["description"]
            }
        return None
    except HttpError as e:
        raise Exception(f"YouTube API error: {str(e)}")
