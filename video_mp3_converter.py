import os
from pydub import AudioSegment

# Function to convert video files to MP3
def convert_video_to_mp3(video_path, output_folder):
    try:
        # Load the video file as audio using pydub
        audio = AudioSegment.from_file(video_path)
        # Define the output MP3 file path
        mp3_path = os.path.join(output_folder, os.path.basename(video_path).replace(".mp4", ".mp3"))
        # Export the audio as MP3
        audio.export(mp3_path, format="mp3")
        print(f"Conversion complete: {mp3_path}")
        
        # Remove the video file after conversion
        os.remove(video_path)
        print(f"Removed video file: {video_path}")
        
        return mp3_path
    except Exception as e:
        print(f"Error converting {video_path} to MP3: {e}")
        return None

# Function to search for video files in a directory and its subdirectories
def convert_videos_in_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            # Only process .mp4 files (or add other video file types as needed)
            if file.lower().endswith(".mp4"):
                video_path = os.path.join(root, file)
                print(f"Found video file: {video_path}")
                # Convert and remove the video file
                convert_video_to_mp3(video_path, root)

if __name__ == "__main__":
    folder_to_search = input("Enter the path of the folder to search for video files: ")
    convert_videos_in_folder(folder_to_search)