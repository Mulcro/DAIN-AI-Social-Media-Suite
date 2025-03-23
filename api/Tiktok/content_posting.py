import os
import urllib.parse
import webbrowser
from flask import Flask, request
import requests
import threading

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# 🔑 Your TikTok credentials
CLIENT_KEY = "TIKTOK_CLIENT_KEY"
CLIENT_SECRET = "TIKTOK_CLIENT_SECRET"
REDIRECT_URI = "https://7beb-134-xxx-xx.ngrok.io/callback"
VIDEO_PATH = "video/tiktok.mp4"

app = Flask(__name__)

# 📌 OAuth: Step 1 - Generate login URL
def get_login_url():
    base_auth_url = "https://www.tiktok.com/v2/auth/authorize/"
    params = {
        "client_key": CLIENT_KEY,
        "response_type": "code",
        "scope": "video.upload",
        "redirect_uri": REDIRECT_URI,
        "state": "secure_random_state"
    }
    return f"{base_auth_url}?{urllib.parse.urlencode(params)}"

# 📌 OAuth: Step 2 - Handle Redirect + Exchange Code
@app.route("/callback")
def oauth_callback():
    code = request.args.get("code")
    print(f"[✅] Authorization code: {code}")

    # Exchange code for access token
    token_res = requests.post("https://open.tiktokapis.com/v2/oauth/token/", data={
        "client_key": CLIENT_KEY,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI
    })

    data = token_res.json()
    access_token = data["access_token"]
    open_id = data["open_id"]
    print(f"[🔐] Access Token: {access_token}")
    print(f"[👤] Open ID: {open_id}")

    # Step 3 - Initiate upload
    upload_init = requests.post(
        "https://open.tiktokapis.com/v2/video/upload/",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"source": "file"}
    )
    upload_info = upload_init.json()["data"]
    upload_url = upload_info["upload_url"]
    video_id = upload_info["video_id"]
    print(f"[📤] Uploading to: {upload_url}")

    # Step 4 - Upload video
    with open(VIDEO_PATH, "rb") as f:
        video_binary = f.read()
    upload_res = requests.put(upload_url, data=video_binary, headers={"Content-Type": "video/mp4"})
    print(f"[⬆️] Upload response: {upload_res.status_code}")

    # Step 5 - Publish video
    publish_res = requests.post(
        "https://open.tiktokapis.com/v2/video/publish/",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"video_id": video_id, "title": "Hello TikTok from API!", "open_id": open_id}
    )
    print(f"[🚀] Publish response: {publish_res.json()}")
    return "✅ Upload & publish complete! Check console for details."

# 🔥 Run Flask server in a thread
def start_flask():
    app.run(port=3000)

if __name__ == "__main__":
    threading.Thread(target=start_flask).start()
    login_url = get_login_url()
    print(f"[🌐] Open this link to login: {login_url}")
    webbrowser.open(login_url)
