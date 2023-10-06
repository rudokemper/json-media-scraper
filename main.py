import os
import json
import requests
import warnings
import argparse
from urllib.parse import urljoin

# To make the console less verbose when downloading media
warnings.simplefilter('ignore')

parser = argparse.ArgumentParser(description="A script to scrape media from a URL")
parser.add_argument('-u', '--url', type=str, required=True, help="The base URL to scrape from")
parser.add_argument('-f', '--file', type=str, required=True, help="The JSON file to load data from")
args = parser.parse_args()
BASE_URL = args.url
JSON_FILE = args.file

# Ensure the necessary directories exist or create them
directories = {
    "image": "./media/images/",
    "audio": "./media/audio/",
    "video": "./media/video/"
}

for dir_path in directories.values():
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

# Read the JSON file and load its content
try:
    with open(JSON_FILE, 'r') as file:
        data = json.load(file)
except FileNotFoundError:
    print(f"Error: The file {JSON_FILE} does not exist.")
    exit(1)
except json.JSONDecodeError:
    print(f"Error: The file {JSON_FILE} is not a valid JSON file.")
    exit(1)

# Function to determine save path based on media type
def get_save_path(media_type, filename):
    return os.path.join(directories[media_type], filename)

downloaded_count = 0
skipped_count = 0

# Function to download media
def download_media(url, media_type):
    global downloaded_count, skipped_count
    
    filename = url.split('/')[-1]
    save_path = get_save_path(media_type, filename)
    
    # Check if the file already exists
    if os.path.exists(save_path):
        print(f"{filename} already exists. Skipping...")
        skipped_count += 1
        return
    
    print(f"Downloading {filename}...")
    try:
        response = requests.get(urljoin(BASE_URL, url), stream=True, verify=False)
        response.raise_for_status()
        
        # Check the Content-Type header
        content_type = response.headers.get('Content-Type', '')
        if 'image' in content_type:
            media_type = 'image'
        elif 'audio' in content_type:
            media_type = 'audio'
        elif 'video' in content_type:
            media_type = 'video'
        else:
            print(f"Unknown media type for {url}. Skipping...")
            return
        
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"{filename} downloaded successfully.")
        downloaded_count += 1
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")

# Function to recursively traverse the JSON data and download media
def traverse_and_download(data):
    if isinstance(data, dict):
        for key, value in data.items():
            traverse_and_download(value)
    elif isinstance(data, list):
        for item in data:
            traverse_and_download(item)
    elif isinstance(data, str):
        file_extension = os.path.splitext(data)[1]
        if file_extension == '.jpg':
            download_media(data, "image")
        elif file_extension == '.mp3':
            download_media(data, "audio")
        elif file_extension == '.mp4':
            download_media(data, "video")

# Extract URLs and download media content
traverse_and_download(data)

print("\nMedia download summary:")
print(f"Total files downloaded: {downloaded_count}")
print(f"Files skipped due to existence: {skipped_count}")
