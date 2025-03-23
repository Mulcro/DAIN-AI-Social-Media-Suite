import requests
import os 
from dotenv import load_dotenv 

# Tiktok access token ( must be obtianed via Oauth2 )

load_dotenv()

CLIENT_KEY = os.getenv("TIKTOK_CLIENT_KEY")
CLIENT_SECRET = os.getenv("TIKTOK_API_CLIENT_SECRET")
REDIRECT_URI = "https://7beb-134-xxx-xx.ngrok.io/callback" # FIXME: PLACEHOLDER


# code needed to get access token for tiktok 
# this might be more of the correct url 
# 'https://www.tiktok.com/v2/auth/authorize/'
def exchange_code_for_access_token(code):   
    url = "https://open.tiktokapis.com/v2/oauth/token/"
    payload = {
    "client_key": CLIENT_KEY,
    "client_secret": CLIENT_SECRET,
    "code": code, # FIXME: 
    "grant_type": "authorization_code",
    "redirect_uri": REDIRECT_URI, 
    
    }

    response = requests.post(url, data=payload)
    return response.json()

def upload_video(access_token, file_path, title="My TikTok Video"):
    # Step 1: Initialize upload 
    init_url = "https://open.tiktokapis.com/v2/post/publish/inbox/video/init/"
    headers = { 
        "Authorization": f"Bearer {access_token}",
        "Content-type": "application/json"
    }
    video_size = 5661910 #TODO: FIXME
    payload = {
    "source_info": {
        "source": "FILE_UPLOAD",
        "video_size": video_size, 
        "chunk_size": video_size, 
        "total_chunk_count": 1 
        }
    }
    response = requests.post(init_url, headers=headers, json=payload)
    res_json = response.json()
    data = res_json.get("data")
    print(data)
    # data: {'publish_id': 'v_inbox_file~v2.7484826579114706990', 'upload_url': 'https://open-upload.tiktokapis.us/upload?upload_id=7484826579114739758&upload_token=bbf4cf75-4ab9-9e6d-d934-0ceea9b8d603'}
    upload_url = data.get("upload_url")
    print(upload_url)
    publish_id = data.get("publish_id")


    # # Step 2: upload video file 
    content_range = "0-5661910/5661910" # FIXME: make this the actual video size
    headers = { 
        "Content-Range": f'bytes {content_range}',
        "Content-type": "video/mp4"
    }
    payload = 'video/tiktok.mp4' 
    response = requests.put(upload_url, headers=headers, json=payload) 

    return {
        "publish_id": publish_id,
    }






