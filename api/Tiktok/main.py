import requests
import os

from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()

# Now fetch the actual token
ACCESS_TOKEN = os.getenv("TIK_TOK_ACCESS_TOKEN")
VIDEO_FILE_PATH = 'video/tiktok.mp4'

video_size = os.path.getsize(VIDEO_FILE_PATH)

# Function to initialize video upload
def initialize_video_upload(title, privacy_level="SELF_ONLY"):
    url = "https://open.tiktokapis.com/v2/post/publish/video/init/"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json; charset=UTF-8"
    }
    payload = {
        "post_info": {
            "title": title,
            "privacy_level": privacy_level,
            "disable_duet": False,
            "disable_comment": False,
            "disable_stitch": False,
            "video_cover_timestamp_ms": 1000
        },
        "source_info": {
            "source": "FILE_UPLOAD",
            "video_size": video_size,
            "chunk_size": video_size,
            "total_chunk_count": 1
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200 and response.json().get("error", {}).get("code") == "ok":
        return response.json()["data"]["upload_url"], response.json()["data"]["publish_id"]
    else:
        raise Exception(f"Initialization failed: {response.text}")

# Function to upload video file
def upload_video(upload_url, file_path):
    file_size = os.path.getsize(file_path)
    content_range = f"bytes 0-{file_size - 1}/{file_size}"

    headers = {
        "Content-Range": content_range,
        "Content-Type": "video/mp4"
    }

    with open(file_path, "rb") as video_file:
        video_data = video_file.read()

    response = requests.put(upload_url, headers=headers, data=video_data)

    if response.status_code in [200, 201]:
        print("✅ Video uploaded successfully.")
    else:
        raise Exception(f"❌ Video upload failed: {response.status_code} — {response.text}")

# Function to check post status
def check_post_status(publish_id):
    url = "https://open.tiktokapis.com/v2/post/publish/status/fetch/"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json; charset=UTF-8"
    }
    payload = {
        "publish_id": publish_id
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch post status: {response.text}")

# Main function
def main():
    try:
        print("🔄 Initializing video upload...")
        upload_url, publish_id = initialize_video_upload("My Awesome TikTok Video")
        print(f"🔗 Upload URL: {upload_url}")
        print(f"📦 Publish ID: {publish_id}")

        print("📤 Uploading video...")
        upload_video(upload_url, VIDEO_FILE_PATH)

        print("📊 Checking post status...")
        status = check_post_status(publish_id)
        print(f"📈 Post status: {status}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
