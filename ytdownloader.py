import os
import pytube
import re

def download_playlist(playlist_url):
    try:
        # Get the playlist
        playlist = pytube.Playlist(playlist_url)
        playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
        playlist_title = playlist.title

        # Create a directory to store the videos
        directory = os.path.join(os.path.dirname(__file__), playlist_title.replace("/", "_"))
        os.makedirs(directory, exist_ok=True)

        # Iterate through each video in the playlist
        for i, video_url in enumerate(playlist, 1):
            try:
                # Get the video
                video = pytube.YouTube(video_url)

                # Get the video title and the best quality video stream
                video_title = f"{i} - {video.title}"
                video_title = re.sub(r'[\\/:*?"<>|]', '', video_title) + ".mp4"
                video_stream = video.streams.filter(file_extension='mp4').get_highest_resolution()

                # Download the video
                print(f"Downloading {video_title}")
                video_stream.download(directory, filename=video_title)
                print(f"{video_title} has been downloaded successfully")
            except pytube.exceptions.PytubeError as e:
                print(f"Error: Unable to download video at index {i} - {video_url}")
                print(f"Error details: {str(e)}")
    except pytube.exceptions.PytubeError as e:
        print(f"Error: Unable to access the playlist at {playlist_url}")
        print(f"Error details: {str(e)}")

# Ask the user for the playlist URL
playlist_url = input("Enter the URL of the YouTube playlist: ")

# Download the playlist
download_playlist(playlist_url)
