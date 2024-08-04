import yt_dlp
import requests
import time
import re
import sys

def debug_print(*args, **kwargs):
    print(*args, **kwargs)

def extract_video_id(url):
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/|v\/|youtu.be\/)([0-9A-Za-z_-]{11})',
        r'(?:watch\?v=)([0-9A-Za-z_-]{11})'
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_best_video_and_audio_url(video_url, proxy=None, max_retries=3):
    video_id = extract_video_id(video_url)
    if not video_id:
        raise ValueError(f"Could not extract video ID from URL: {video_url}")

    debug_print(f"Extracted video ID: {video_id}")
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'quiet': True,
        'socket_timeout': 30,
    }
    if proxy:
        ydl_opts['proxy'] = proxy

    for attempt in range(max_retries):
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
                formats = info.get('formats', [])

                video_formats = [f for f in formats if f.get('vcodec') != 'none' and f.get('height') is not None]
                if not video_formats:
                    raise ValueError("No valid video formats found")

                best_video = max(video_formats, key=lambda x: (x['height'], x.get('tbr', 0)))
                video_has_audio = best_video.get('acodec') != 'none'

                audio_formats = [f for f in formats if f.get('acodec') != 'none']
                has_separate_audio = bool(audio_formats)

                if has_separate_audio:
                    best_audio = max(audio_formats, key=lambda x: (x.get('abr', 0) or 0, x.get('tbr', 0) or 0))
                    audio_url = best_audio['url']
                    audio_ext = best_audio['ext']
                else:
                    audio_url = None
                    audio_ext = None

                video_url = best_video['url']
                resolution = f"{best_video['height']}p"
                video_ext = best_video['ext']

                return video_url, audio_url, info.get('title', 'Unknown'), resolution, video_ext, audio_ext, video_has_audio, has_separate_audio

        except (yt_dlp.utils.DownloadError, requests.exceptions.RequestException, ValueError) as e:
            if attempt < max_retries - 1:
                print(f"Error occurred: {str(e)}. Retrying... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise

    raise Exception("Failed to get video information after multiple attempts")


