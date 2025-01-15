import os
import json
from scrape_lists import scrape_tiktok_hashtag_videos, scrape_tiktok_user_videos, append_urls_to_json
from download import process_videos


def get_search_type():
    """
    Prompts the user to choose the search type.

    Returns:
        str: The chosen search type ('hashtag', 'username', or 'userid').
    """
    print("\nChoose the type of search:")
    print("1. Hashtag")
    print("2. User ID")
    choice = input("Enter your choice (1/2): ").strip()

    if choice == "1":
        return "hashtag"
    elif choice == "2":
        return "userid"
    else:
        print("Invalid choice! Defaulting to 'hashtag'.")
        return "hashtag"


if __name__ == "__main__":
    search_type = get_search_type()
    search_query = input(f"Enter the {search_type} to scrape: ").strip()
    max_videos = int(input("Enter the maximum number of video URLs to scrape: ").strip())
    user_data_dir = input("Enter the path to your Chrome user data directory (optional): ").strip()

    if not user_data_dir:
        print("Warning: Without a Chrome user data directory, you may not stay logged in.")

    # Create a folder to save the scraped lists
    scraped_lists_folder = "scraped_lists"
    os.makedirs(scraped_lists_folder, exist_ok=True)

    # JSON file for storing URLs
    output_file = os.path.join(scraped_lists_folder, f"{search_query}_{search_type}_video_urls.json")

    # Scrape TikTok video URLs based on search type
    print(f"Scraping up to {max_videos} videos for {search_type} '{search_query}'...")
    if search_type == "hashtag":
        video_urls = scrape_tiktok_hashtag_videos(
            search_query, max_videos=max_videos, batch_size=50, rest_seconds=5, user_data_dir=user_data_dir, retry_delay=2, max_retries=10
        )
    elif search_type == "userid":
        video_urls = scrape_tiktok_user_videos(
            search_query, search_type=search_type, max_videos=max_videos, batch_size=50, rest_seconds=5, user_data_dir=user_data_dir, retry_delay=2, max_retries=10
        )
    else:
        print("Invalid search type! Exiting...")
        exit(1)

    # Append the URLs to the JSON file
    append_urls_to_json(video_urls, output_file)

    # Specify the external drive path
    external_drive = "/Volumes/T7 Black/Borderx"
    if not os.path.exists(external_drive):
        print(f"Error: External drive or folder {external_drive} not found!")
        external_drive = ""

    # Create a subfolder for the videos
    video_folder = os.path.join(external_drive, "videos", f"{search_query}_{search_type}_videos")
    os.makedirs(video_folder, exist_ok=True)

    print(f"Downloading videos to: {video_folder}")

    # Process videos
    rate_limit_delay = 10  # Delay in seconds to handle rate limits
    process_videos(output_file, video_folder, rate_limit_delay)

    print("Done downloading.")

