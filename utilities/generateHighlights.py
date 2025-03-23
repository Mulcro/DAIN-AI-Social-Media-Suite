import time
import requests
import os
import sys
import json

def push_and_wait_for_highlights(api_key, file_url, highlight_search_phrases, render_clips=True, poll_interval=5, max_attempts=60):
    """
    Push a highlights generation job to the API and wait until it is completed.

    Args:
        api_key (str): Your API key.
        file_url (str): Public URL of the video file.
        highlight_search_phrases (str): The search phrases for highlights.
        render_clips (bool): Whether to render clips (default: True).
        poll_interval (int): Seconds to wait between polling attempts.
        max_attempts (int): Maximum number of polling attempts before giving up.

    Returns:
        dict: Final job data once the status is no longer "processing".
    """
    # Push the job via POST
    post_url = "https://mango.sievedata.com/v2/push"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": api_key
    }
    payload = {
        "function": "sieve/highlights",
        "inputs": {
            "file": {"url": file_url},
            "render_clips": render_clips,
            "highlight_search_phrases": highlight_search_phrases
        }
    }
    
    post_resp = requests.post(post_url, headers=headers, json=payload)
    if post_resp.status_code != 200:
        raise Exception(f"Error pushing job: {post_resp.status_code} {post_resp.text}")
    post_result = post_resp.json()
    job_id = post_result.get("id")
    if not job_id:
        raise Exception("Job ID not found in the POST response.")
    
    print(f"Job pushed successfully! Job ID: {job_id}")
    
    # Poll the job status until it's no longer "processing"
    get_url = f"https://mango.sievedata.com/v2/jobs/{job_id}"
    attempts = 0
    while attempts < max_attempts:
        get_resp = requests.get(get_url, headers={"X-API-Key": api_key})
        if get_resp.status_code != 200:
            raise Exception(f"Error retrieving job data: {get_resp.status_code} {get_resp.text}")
        job_data = get_resp.json()
        
        status = job_data.get("status")
        print(f"Attempt {attempts+1}: Job status is '{status}'.")
        if status.lower() != "processing":
            # Job is complete (or at least no longer processing)
            return job_data
        
        time.sleep(poll_interval)
        attempts += 1
    
    raise Exception("Job did not complete within the allotted polling time.")

def extract_highlight_urls(response_json):
    """
    Extracts all URL values from the given JSON response.
    
    Args:
        response_json (dict): The JSON response from the GET job request.
    
    Returns:
        list: A list of URLs found in the outputs.
    """
    urls = []
    for output in response_json.get("outputs", []):
        for item in output.get("data", []):
            if isinstance(item, dict) and "url" in item:
                urls.append(item["url"])
    return urls
def download_video(url, output_path):
    """
    Downloads a video from the provided URL and saves it to output_path.

    Args:
        url (str): The URL of the video to download.
        output_path (str): The path (including filename) where the video will be saved.
    """
    response = requests.get(url, stream=True)
    if response.status_code != 200:
        raise Exception(f"Failed to download video. Status code: {response.status_code}")

    total_size = int(response.headers.get('content-length', 0))
    downloaded = 0
    chunk_size = 8192  # 8KB per chunk

    print(f"Downloading video from {url} ...")
    with open(output_path, "wb") as file:
        for chunk in response.iter_content(chunk_size):
            if chunk:
                file.write(chunk)
                downloaded += len(chunk)
                percent = downloaded * 100 / total_size if total_size else 0
                print(f"Downloaded {downloaded} of {total_size} bytes ({percent:.2f}%)", end="\r")
    
    print(f"\nDownload completed. Video saved as {output_path}")

if __name__ == "__main__":
    API_KEY = "82GhvkGPGZaoFN4u3m5magcMJ4u0e_3pph2-B6KZMro"
    FILE_URL = sys.argv[1]
    HIGHLIGHT_SEARCH_PHRASES = "Pick the shortest most educational parts"
    
    try:
        print(FILE_URL)
        # Push the job and wait for it to finish
        final_job_data = push_and_wait_for_highlights(API_KEY, FILE_URL, HIGHLIGHT_SEARCH_PHRASES)
        print("Final Job Data:")
        print(final_job_data)
        
        # Extract highlight URLs from the finished job data
        highlight_urls = extract_highlight_urls(final_job_data)
        if highlight_urls:
            print("Processed Highlight URLs:")
            for i, url in enumerate(highlight_urls, start=1):
                print(f"Downloading highlight {i} from URL: {url}")
                output_dir = os.path.join(os.path.dirname(__file__), "..", "constants", "highlights")
                os.makedirs(output_dir, exist_ok=True)

                output_filename = f"highlight_{i}.mp4"
                output_path = os.path.join(output_dir, output_filename)

                download_video(url, output_path)
                print(f"Downloaded highlight {i} to {output_filename}\n")

            # Print the highlight URLs as the final output JSON.
        else:
            print("No highlight URLs were found in the response.")
        
        result = {"highlight_urls": highlight_urls}
        # Ensure only JSON is printed on the last line.
        print(json.dumps(result))

    except Exception as e:
        print(f"An error occurred: {e}")