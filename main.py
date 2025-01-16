import os
import json
import csv
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

def process_input_account(dst_folder,account,search_type,max_videos=500):
    user_data_dir=""
    # Create a folder to save the scraped lists
    scraped_lists_folder = "scraped_lists"
    os.makedirs(scraped_lists_folder, exist_ok=True)

    # JSON file for storing URLs
    output_file = os.path.join(scraped_lists_folder, f"{account}_{search_type}_video_urls.json")

    # Scrape TikTok video URLs based on search type
    print(f"Scraping up to {max_videos} videos for {search_type} '{account}'...")
    if search_type == "hashtag":
        video_urls = scrape_tiktok_hashtag_videos(
            account, max_videos=max_videos, batch_size=50, rest_seconds=5, user_data_dir=user_data_dir, retry_delay=2, max_retries=10)

    elif search_type == "userid":
        video_urls = scrape_tiktok_user_videos(
            account, search_type=search_type, max_videos=max_videos, batch_size=50, rest_seconds=5, user_data_dir=user_data_dir, retry_delay=2, max_retries=2)
    else:
        print("Invalid search type! Exiting...")
        exit(1)

    # Append the URLs to the JSON file
    append_urls_to_json(video_urls, output_file)

    # Specify the external drive path
    external_drive = f"/videos"
    if not os.path.exists(external_drive):
        print(f"Error: External drive or folder {external_drive} not found!")
        external_drive = ""

    # Create a subfolder for the videos
    video_folder = os.path.join(external_drive, "videos", f"{dst_folder}/{account}_{search_type}_videos")
    os.makedirs(video_folder, exist_ok=True)

    print(f"Downloading videos to: {video_folder}")

    # Process videos
    rate_limit_delay = 10  # Delay in seconds to handle rate limits
    process_videos(output_file, video_folder, rate_limit_delay)

    

if __name__ == "__main__":
    search_type = get_search_type()
    search_folder = input(f"Enter source file to read: ").strip()
    # max videos to be scrapped
    max_videos = 400

    # Clear the errors.txt file
    with open("errors.txt", "w") as f:
        f.write("")

    # Read the CSV file
    # Row 0 should be keyword, the property some accounts shared. While be the subfolder name of videos
    # Row 1 should be account id, user id of tiktok. Do not contain @
    with open(search_folder, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) != 2 or len(row[0]) == 0 or len(row[1]) == 0:
                continue
            try:
                print(f"Processing account: {row[1]} with keyword: {row[0]}")
                process_input_account(row[0],row[1],search_type,max_videos)
            except Exception as e:
                print(f"Error processing account {row[1]}: {e}")
                with open("errors.txt", "a") as f:
                        f.write(f"An error occurred on {search_folder}, product {row[1]} \n")



    print("Done downloading.")

