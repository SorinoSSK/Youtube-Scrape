# from pytube import YouTube
import os
import re
import time
import eyed3
from pytubefix import YouTube
from pytubefix.cli import on_progress
from pydub import AudioSegment
from urllib.error import HTTPError

# Function to download the video using pytube
def dwl_vid(video_url, output_folder, videoData, retries=3, delay=5):
    attempt = 0
    while attempt < retries:
        try:
            yt = YouTube(video_url, on_progress_callback = on_progress)
            print(f"Video Title: {yt.title}")
            # Get the highest resolution stream
            stream = yt.streams.get_highest_resolution()
            print(f"Downloading: {yt.title} to {output_folder}")
            # Download video to the specified folder
            stream.download(output_folder, filename=f"{sanitise_filename(videoData['title'])}.mp4")
            print(f"Download complete: {videoData['title']}.mp4")
            return os.path.join(output_folder, sanitise_filename(videoData['title']) + ".mp4")
        except HTTPError as e:
            print(f"HTTPError: {e.code} - Bad Request. Could be an issue with the video URL or YouTube's servers.")
            attempt += 1
            print(f"Error downloading video (Attempt {attempt}/{retries}): {e}")
            if attempt < retries:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("Max retries reached. Skipping video.")
                log_failed_video(video_url, videoData)
                return None
        except Exception as e:
            attempt += 1
            print(f"Error downloading video [{e}] (Attempt {attempt}/{retries}): {e}")
            if attempt < retries:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("Max retries reached. Skipping video.")
                log_failed_video(video_url, videoData)
                return None

# Function to convert downloaded video to MP3 using pydub
def convert_to_mp3(video_path, output_folder, VideoData):
    try:
        # Load the video file using pydub
        audio = AudioSegment.from_file(video_path)
        # Define the output MP3 file path
        mp3_path = os.path.join(output_folder, os.path.basename(video_path).replace(".mp4", ".mp3"))
        # Export the audio as MP3
        audio.export(mp3_path, format="mp3")
        print(f"Conversion complete: {mp3_path}")
        set_metadata(mp3_path, VideoData)
        print(f"Metadata set: {mp3_path}")
        # Remove the video file after conversion
        os.remove(video_path)
        print(f"Removed video file: {video_path}")
        return mp3_path
    except Exception as e:
        print(f"Error converting to MP3: {e}")
        log_failed_video(mp3_path ,VideoData)
        return None

def set_metadata(mp3_path, data):
    try:
        # Open the MP3 file with eyed3
        audio_file = eyed3.load(mp3_path)
        if audio_file.tag is None:
            audio_file.initTag()

        # Set the contributing artist
        audio_file.tag.album = data["album"]
        audio_file.tag.title = data["title"]
        audio_file.tag.artist = data["contributing_artist"]  # Contributing Artis
        if data["year"].isdigit():
            audio_file.tag.recording_date = eyed3.core.Date(int(data["year"]))

        # Save changes to the MP3 file
        audio_file.tag.save()
    except Exception as e:
        log_failed_video(mp3_path ,data)
        print(f"Error setting details for {mp3_path}: {e}")

# Function to log failed videos (creating the log file if it doesn't exist)
def log_failed_video(video_url, data, log_file="failed_downloads.txt"):
    # Create the log file if it does not exist
    if not os.path.exists(log_file):
        with open(log_file, "w", encoding="utf-8") as file:
            file.write("Failed video downloads:\n")  # Optionally add a header
    with open(log_file, "a", encoding="utf-8") as file:
        file.write(f"{video_url}\t{data['title']}\n")

def sanitise_filename(filename):
    # Remove invalid characters for Windows filenames: \ / : * ? " < > |
    return re.sub(r'[\\/:*?"<>|.]', '_', filename)

# Function to process the videos in the file
def process_videos(file_path):
    current_output_folder = None
    root_dir    = ""
    data        = {}

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()

            if not line:
                continue
            # If it's a folder name, update output folder
            if not line.startswith("http"):
                if root_dir == "":
                    root_dir = line
                elif not "contributing_artist" in data:
                    data["contributing_artist"] = line
                else:
                    current_output_folder = sanitise_filename(line)
                    os.makedirs(os.path.join(root_dir, current_output_folder), exist_ok=True)
                    print(f"Created folder: {current_output_folder}")

            elif current_output_folder:
                # set root dir to current if do not exist
                if root_dir == "":
                    root_dir = "./"

                # set contributing artist to unknown if do not exist
                elif not "contributing_artist" in data:
                    data["contributing_artist"] = "Unknown"
                
                # split video data info and store
                videoData = line.split(",")
                data["album"] = current_output_folder
                data["title"] = videoData[2].replace('"', '""')
                data["year"] = videoData[1]
                current_output_folder = sanitise_filename(current_output_folder)

                # If it's a URL, download the video to the current output folder
                print(f"Downloading video from: {videoData[0]} -> {os.path.join(root_dir, current_output_folder)}")
                video_path = dwl_vid(videoData[0], os.path.join(root_dir, current_output_folder), data)
                print(f"Video path: {video_path}")
                if video_path:
                    convert_to_mp3(video_path, os.path.join(root_dir, current_output_folder), data)
                else:
                    print("Video path do not exist.")

if __name__ == "__main__":
    # Specify the path to your videos.txt file
    process_videos("video_list.txt")