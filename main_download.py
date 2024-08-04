import argparse
import os
import sys
from video_format_utils import select_best_format
from moviepy_merger import merge_video_audio_moviepy
from url_analyzer import collect_all_video_urls
import yt_dlp
import requests
import time
import re

# Constants
DEFAULT_OUTPUT_DIR = "output"
DEFAULT_OUTPUT_RESULT = "done.txt"
DEBUG = False

def debug_print(*args, **kwargs):
    if DEBUG:
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

def get_best_video_and_audio_url(video_url, proxy=None, max_retries=3, max_quality=None):
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

                debug_print("\nAvailable video formats:")
                for i, format in enumerate(video_formats, 1):
                    debug_print(f"{i}. Resolution: {format.get('height')}p, "
                                f"Codec: {format.get('vcodec')}, "
                                f"FPS: {format.get('fps')}, "
                                f"Bitrate: {format.get('tbr')}k, "
                                f"Audio Codec: {format.get('acodec')}")
                debug_print()  # Add an empty line for better readability

                if max_quality:
                    video_formats = [f for f in video_formats if f['height'] <= max_quality]
                    if not video_formats:
                        raise ValueError(f"No video formats found with quality {max_quality}p or lower")

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
            debug_print(f"Error occurred: {str(e)}")
            if attempt < max_retries - 1:
                print(f"Error occurred: {str(e)}. Retrying... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise

    raise Exception("Failed to get video information after multiple attempts")

def clean_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def process_video(video_url, output_dir, max_quality=None):
    try:
        video_url, audio_url, title, resolution, video_ext, audio_ext, video_has_audio, has_separate_audio = get_best_video_and_audio_url(video_url, max_quality=max_quality)
        print(f"\nProcessing video: {title}")
        print(f"Resolution: {resolution}, Format: {video_ext}, Audio: {video_has_audio}")
        debug_print(f"Video URL: {video_url[:100]}...")  # Print first 100 chars of URL

        print("Downloading...")

        clean_title = clean_filename(title)
        output_filename = os.path.join(output_dir, f"{clean_title}.{video_ext}")
        merge_video_audio_moviepy(video_url, audio_url, output_filename)

        print("==================")

        if os.path.exists(output_filename):
            print(f"File saved to: {output_filename}")
            return "SUCCESS", output_filename
        else:
            print("Failed to save the file.")
            return "FAILED", None

    except Exception as e:
        print(f"Error processing video: {str(e)}")
        return "FAILED", None

def main():
    parser = argparse.ArgumentParser(description="Download YouTube videos from a list")
    parser.add_argument("--input", required=True, help="Input file with video URLs")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR, help="Output directory for downloaded videos")
    parser.add_argument("--output-result", default=DEFAULT_OUTPUT_RESULT, help="Output file for download results")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    parser.add_argument("--max-quality", type=int, choices=[144, 240, 360, 480, 720, 1080, 1440, 2160], help="Maximum video quality to download")
    args = parser.parse_args()

    global DEBUG
    DEBUG = args.debug

    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found.")
        sys.exit(1)

    os.makedirs(args.output_dir, exist_ok=True)

    # Read URLs from input file
    with open(args.input, 'r') as input_file:
        input_urls = [line.strip() for line in input_file if line.strip()]

    # Process URLs to extract all video URLs, including those from playlists
    all_video_urls = collect_all_video_urls(input_urls)
    total_videos = len(all_video_urls)
    print(f"\nTotal videos to download: {total_videos}")

    with open(args.output_result, 'w') as result_file:
        for index, video_url in enumerate(all_video_urls, start=1):
            print(f"Processing video {index}/{total_videos}: {video_url}")
            status, output_path = process_video(video_url, args.output_dir, max_quality=args.max_quality)
            result = f"{video_url},{status},{output_path if output_path else 'N/A'}\n"
            result_file.write(result)
            result_file.flush()  # Ensure the result is written immediately

    print(f"\nAll videos processed. Results saved to {args.output_result}")

if __name__ == "__main__":
    main()
