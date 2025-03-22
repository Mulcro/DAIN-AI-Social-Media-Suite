#!/usr/bin/env python
import os
import argparse
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import googleapiclient.http

# Define the OAuth scope required for uploading videos
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service(client_secrets_file):
    """
    Creates an authenticated YouTube service using OAuth 2.0.
    """
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # Only for testing; remove in production.
    
    client_secrets_file = "client_secrets.json"
    # Run the OAuth flow to get credentials.
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, SCOPES
    )
    credentials = flow.run_local_server(port=8080)    

    # Build the YouTube service object.
    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

def upload_video(youtube, file_path, title, description, category_id, privacy_status):
    """
    Uploads a video to YouTube.

    Args:
        youtube: Authenticated YouTube service.
        file_path: Path to the video file.
        title: Video title.
        description: Video description.
        category_id: YouTube video category (e.g., "22" for People & Blogs).
        privacy_status: Video privacy ("public", "private", or "unlisted").
    """
    # Build the request body.
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "categoryId": category_id
        },
        "status": {
            "privacyStatus": privacy_status
        }
    }

    # Prepare the video file for upload.
    media = googleapiclient.http.MediaFileUpload(
        file_path, chunksize=-1, resumable=True
    )
    
    # Initiate the insert request.
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    # Upload the video in chunks.
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")
    print("Upload complete.")
    print("Video details:")
    print(response)

def main():
    parser = argparse.ArgumentParser(
        description="Upload a video to YouTube (or YouTube Shorts)."
    )
    parser.add_argument("--file", help="Path to the video file", required=True)
    parser.add_argument("--title", help="Video title", default="Test Video")
    parser.add_argument("--description", help="Video description", default="Uploaded via Python script")
    parser.add_argument("--category", help="Video category id (e.g., 22 for People & Blogs)", default="22")
    parser.add_argument("--privacy", help="Video privacy status", choices=["public", "private", "unlisted"], default="private")
    parser.add_argument("--client-secrets", help="Path to OAuth client secrets JSON file", required=True)
    args = parser.parse_args()

    # Authenticate and build the YouTube API service.
    youtube = get_authenticated_service(args.client_secrets)
    
    # Upload the video.
    upload_video(youtube, args.file, args.title, args.description, args.category, args.privacy)

if __name__ == "__main__":
    main()