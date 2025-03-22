import requests
import os 
from dotenv import load_dotenv 

# Tiktok access token ( must be obtianed via Oauth2 )

load_dotenv()

CLIENT_KEY = os.getenv("TIKTOK_CLIENT_KEY")
CLIENT_SECRET = os.getenv("TIKTOK_CLIENT_SECRET")

# code needed to get access token for tiktok 
# this might be more of the correct url 
# 'https://www.tiktok.com/v2/auth/authorize/'
def exchange_code_for_access_token(code):   

    url = "https://open.tiktokapis.com/v2/oauth/token/"
    payload = {
    "client_key": CLIENT_KEY,
    "client_secret": CLIENT_SECRET,
    "code": code,
    "grant_type": "authorization_code",
    "redirect_uri": REDIRECT_URI,
    
    }

    response = requests.post(url, data=payload)
    return response.json()

def upload_video(access_token, file_path, title="My TikTok Video"):
    # Step 1: Initialize upload 
    init_url = " https://open.tiktokapis.com/v2/post/publish/video/init/"
    headers = { 
        "Authorization": f"Bearer {access_token}",
        "Content-type": "application/json"
    }
    payload = {
    "post_info": {
        "title": title
        }
    }

    response = request.post(init_url, headers=headers, json=payload)
    data = response.json()
    upload_url = data.get("upload_url")
    video_id = data.get("video_id")

    # Step 2: upload video file 
    with open(file_path, "rb") as f:
        upload_resp = requests.post(upload_url, files={"video": f})
    
    return {
        "video_id": video_id,
        "upload_status": upload_resp.status_code
    }






