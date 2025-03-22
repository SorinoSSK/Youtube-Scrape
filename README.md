# Youtube-Scrape
## Getting Started
1) Installation
```
py -m pip install -r requirements.txt
```
## Executables
1) List down all youtube URL for a youtube music playlist
```
py get_youtube_url.py
```
2) Download music from a list of youtube url
```
py youtube_mp3_downloader.py
```
3) Search for any .mp4 file and convert them to .mp3 file
```
py video_mp3_converter.py
```
## To know
1) failed_downloads.txt\
The file records a list of failed download, convertion, or meta update files.
2) video_list.txt\
The file records a list of youtube url arranged in the following format
```
/root/directory
artist_name

album_name_1
url1_1,release_year,music1_title_1
url1_2,release_year,music1_title_2
url1_n,release_year,music1_title_n

album_name_2
url2_1,release_year,music2_title_1
url2_2,release_year,music2_title_2
url2_n,release_year,music2_title_n
```
