#!/usr/bin/env python3
import os
import json
import argparse
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import googleapiclient.http
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

# Define the OAuth scope required for uploading videos
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service(client_secrets_file, credential_file="credentials.json"):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # Only for testing; remove in production.

    creds = None
    # Check if the credential file exists
    if os.path.exists(credential_file):
        with open(credential_file, "r") as token:
            creds_data = json.load(token)
        creds = Credentials.from_authorized_user_info(creds_data, SCOPES)
        print("Loaded credentials from", credential_file)
    
    # If there are no valid credentials available, prompt the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            print("Refreshed credentials.")
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, SCOPES
            )
            creds = flow.run_local_server(port=8081)
            print("Obtained new credentials.")
        # Save the credentials for future use
        with open(credential_file, "w") as token:
            token.write(creds.to_json())
            print("Saved credentials to", credential_file)
    
    # Build the YouTube service object.
    return googleapiclient.discovery.build("youtube", "v3", credentials=creds)

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