import json
import os
import requests
import time


def fetch_tunnel_url(video_url, api_url="http://localhost:9000/"):
    """
    Fetch the tunnel URL for a video using the self-hosted Cobalt API.

    Args:
        video_url (str): The TikTok video URL.
        api_url (str): The URL of the self-hosted Cobalt API.

    Returns:
        dict: A dictionary containing the tunnel URL and filename.
    """
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {"url": video_url}
    response = requests.post(api_url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        if response.status_code == 429 or '"code":"error.api.rate_exceeded"' in response.text:
            print("Rate limit exceeded. Retrying after delay...")
            return {"rate_exceeded": True}
        print(f"Failed to fetch tunnel URL for {video_url}. Response: {response.text}")
        return None


def download_video_from_tunnel(tunnel_url, filename, output_dir):
    """
    Download the video from the tunnel URL.

    Args:
        tunnel_url (str): The tunnel URL to fetch the video.
        filename (str): The name to save the video as.
        output_dir (str): The directory to save the downloaded video.

    Returns:
        None
    """
    response = requests.get(tunnel_url, stream=True)

    if response.status_code == 200:
        output_path = os.path.join(output_dir, filename)
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        print(f"Downloaded: {filename} -> {output_path}")
    else:
        print(f"Failed to download from tunnel URL: {tunnel_url}. Response: {response.text}")


def process_videos(json_file, output_dir, rate_limit_delay=5):
    """
    Process video URLs from a JSON file and download them using the Cobalt API.

    Args:
        json_file (str): Path to the JSON file containing video URLs.
        output_dir (str): Directory to save the downloaded videos.
        rate_limit_delay (int): Number of seconds to wait after hitting a rate limit.

    Returns:
        None
    """
    os.makedirs(output_dir, exist_ok=True)

    with open(json_file, "r") as f:
        video_urls = json.load(f)

    for video_url in video_urls:
        print(f"Processing: {video_url}")

        # Retry logic for rate limits
        while True:
            result = fetch_tunnel_url(video_url)
            if result is None:
                break  # Failed to fetch and no rate limit
            if result.get("rate_exceeded"):
                print(f"Rate limit hit. Waiting for {rate_limit_delay} seconds...")
                time.sleep(rate_limit_delay)
                continue  # Retry after delay
            break  # Success, proceed to download

        if result and "url" in result and "filename" in result:
            download_video_from_tunnel(result["url"], result["filename"], output_dir)