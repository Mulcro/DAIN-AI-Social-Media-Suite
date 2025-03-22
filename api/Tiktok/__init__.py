from tiktok import exchange_code_for_access_token, upload_video

# Exchange code (from URL param)
response = exchange_code_for_access_token("code_from_callback")
access_token = response.get("access_token")

# Upload video
result = upload_video(access_token, "videos/myvideo.mp4")
# tiktok/__init__.py

from .tiktok import exchange_code_for_access_token, upload_video  # relative import

if __name__ == "__main__":
    # Exchange code (from URL param)
    response = exchange_code_for_access_token("code_from_callback")
    access_token = response.get("access_token")

    # Upload video
    result = upload_video(access_token, "videos/myvideo.mp4")
    print(result)
