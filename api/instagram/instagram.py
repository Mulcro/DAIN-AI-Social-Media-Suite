#!/usr/bin/env python3
import os
import time
import argparse
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read credentials from environment
IG_USER_ID = os.getenv("IG_USER_ID")  # Your Instagram Business/Creator Account ID
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")  # Your Page Access Token with necessary permissions
API_VERSION = os.getenv("API_VERSION", "v16.0")  # Default API version

# print(f"ACCESS_TOKEN: {ACCESS_TOKEN}")
def create_reels_container(video_url, caption, thumb_offset, share_to_feed=True):
    """
    Create a media container for a Reel by posting to the /media endpoint.
    """
    url = f"https://graph.facebook.com/{API_VERSION}/{IG_USER_ID}/media"
    params = {
        "media_type": "REELS",
        "video_url": video_url,
        "caption": caption,
        "share_to_feed": str(share_to_feed).lower(),  # 'true' or 'false'
        "thumb_offset": thumb_offset,
        "access_token": ACCESS_TOKEN
    }
    print("Creating reels container...")
    response = requests.post(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Error creating reels container: {response.status_code} {response.text}")
    data = response.json()
    container_id = data.get("id")
    if not container_id:
        raise Exception("No container ID returned in the response.")
    print(f"Reels container created with ID: {container_id}")
    return container_id

def publish_reels_container(container_id):
    """
    Publish the media container using the /media_publish endpoint.
    """
    url = f"https://graph.facebook.com/{API_VERSION}/{IG_USER_ID}/media_publish"
    params = {
        "creation_id": container_id,
        "access_token": ACCESS_TOKEN
    }
    print("Publishing reels container...")
    response = requests.post(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Error publishing reels: {response.status_code} {response.text}")
    data = response.json()
    media_id = data.get("id")
    if not media_id:
        raise Exception("No media ID returned after publishing.")
    print(f"Reels published successfully! Media ID: {media_id}")
    return media_id

def main():
    parser = argparse.ArgumentParser(
        description="Post a video to Instagram Reels using the Instagram Graph API."
    )
    parser.add_argument("--video_url", required=True, help="Public URL of the video to post as a Reel")
    parser.add_argument("--caption", default="", help="Caption for the Reel")
    parser.add_argument("--thumb_offset", default="2000", help="Thumbnail offset in milliseconds (default: 2000)")
    args = parser.parse_args()

    try:
        # Step 1: Create a media container for the Reel
        container_id = create_reels_container(args.video_url, args.caption, args.thumb_offset)
        
        # Optional: Wait a few seconds to ensure the container is processed (adjust if needed)
        print("Waiting for the media container to be processed...")
        time.sleep(10)
        
        # Step 2: Publish the container to post the Reel
        media_id = publish_reels_container(container_id)
        print(f"Successfully published Reel with Media ID: {media_id}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()