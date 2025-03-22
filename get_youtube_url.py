import yt_dlp
import os
from urllib.parse import urlparse, parse_qs

def remove_hash_part(string):
    return string.split('#')[0]

def extract_youtube_urls(playlist_url, v_year):
    ydl_opts = {
        'extract_flat': True,
        'force_generic_extractor': True
    }
    
    try:
        playlist_url = playlist_url
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(playlist_url, download=False)
            if 'entries' in result:
                print(f"Found {len(result['entries'])} videos in the playlist:")
                log_video_details(result.get('title', None))
                for entry in result['entries']:
                    print(remove_hash_part(entry['url']), "\t", v_year, "\t",entry['title'])
                    log_video_details(remove_hash_part(entry['url']) + "," + v_year + "," + entry['title'])
                log_video_details("\n")
            else:
                print("The provided URL is not a playlist.")
    except Exception as e:
        print(f"Error extracting URLs: {e}")

# Function to log failed videos (creating the log file if it doesn't exist)
def log_video_details(video_info, log_file="video_list.txt"):
    # Create the log file if it does not exist
    if not os.path.exists(log_file):
        with open(log_file, "w", encoding="utf-8") as file:
            file.write("")
    with open(log_file, "a", encoding="utf-8") as file:
        file.write(f"{video_info}\n")

if __name__ == "__main__":
    playlist_url = input("Enter the YouTube Music playlist URL: ")
    album_year = input("Release Year?: ")
    extract_youtube_urls(playlist_url, album_year)
