# JSON Media Scraper

This script is designed to scrape media files from a JSON file and a given URL and save them to specific directories based on their type (image, audio, video). The script uses a JSON file as input, which should contain the URLs of the media files to be downloaded.

### Usage

To use this script, you need to provide two command-line arguments:

- `-u` or `--url`: The base URL to scrape from.
- `-f` or `--file`: The path to the JSON file to load data from.

Here is an example of how to run the script:

```
python ./main.py -u http://your_url -f ./your_json_file
```

### Directory Structure

The script will automatically create the following directories if they do not exist:

- `./media/images/` for image files
- `./media/audio/` for audio files
- `./media/video/` for video files

### JSON File Structure

The JSON file should contain the URLs of the media files to be downloaded. The script will traverse through the JSON data and download any media files it encounters based on the file header `Content-Type`.
