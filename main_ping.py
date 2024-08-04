import argparse
import yt_dlp
import requests
import time
import sys

from utils import get_best_video_and_audio_url

DEFAULT_VIDEO_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
DEFAULT_DURATION = 10
CHUNK_SIZE = 1024 * 1024  # 1 MB
DEBUG = False

def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)

def measure_download_speed(url, duration=DEFAULT_DURATION, proxy=None):
    start_time = time.time()
    downloaded = 0
    peak_speed = 0
    last_update_time = start_time
    retry_delay = 1

    proxies = {'http': proxy, 'https': proxy} if proxy else None

    try:
        while time.time() - start_time < duration:
            try:
                with requests.get(url, stream=True, timeout=10, proxies=proxies) as r:
                    r.raise_for_status()
                    for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
                        if chunk:
                            downloaded += len(chunk)
                            current_time = time.time()
                            elapsed_time = current_time - start_time
                            if elapsed_time >= duration:
                                break
                            speed = downloaded / elapsed_time / 1024 / 1024  # MB/s
                            peak_speed = max(peak_speed, speed)
                            if current_time - last_update_time >= 1:  # Update display every second
                                remaining_time = max(0, duration - elapsed_time)
                                sys.stdout.write(f"\rDownloaded: {downloaded/1024/1024:.2f} MB, Current Speed: {speed:.2f} MB/s, Peak Speed: {peak_speed:.2f} MB/s, Time left: {remaining_time:.0f}s \n")
                                sys.stdout.flush()
                                last_update_time = current_time
                retry_delay = 1  # Reset retry delay on successful download
            except requests.RequestException as e:
                error_type = type(e).__name__
                print(f"Error: {error_type}. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, duration / 2)  # Exponential backoff, max {duration} seconds
    except KeyboardInterrupt:
        print("\nTest interrupted by user.")

    total_time = time.time() - start_time
    avg_speed = downloaded / total_time / 1024 / 1024  # MB/s

    return avg_speed, downloaded / 1024 / 1024, peak_speed  # avg speed in MB/s, downloaded in MB, peak speed in MB/s


def main():
    parser = argparse.ArgumentParser(description="Measure download speed for YouTube video")
    parser.add_argument("--url", default=DEFAULT_VIDEO_URL, help="YouTube video URL to test")
    parser.add_argument("--duration", type=int, default=DEFAULT_DURATION, help="Duration of the speed test in seconds")
    parser.add_argument("--proxy", help="Proxy server to use (e.g., socks5://127.0.0.1:9150 for Tor)")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    args = parser.parse_args()

    if args.debug:
        debug_print("Debug mode enabled")

    video_url = args.url
    print(f"Video URL: {video_url}")
    print(f"Test duration: {args.duration} seconds")
    if args.proxy:
        print(f"Using proxy: {args.proxy}")

    try:
        video_url, _, title, resolution, video_ext, _, _, _ = get_best_video_and_audio_url(video_url, proxy=args.proxy)
        print(f"Video title: {title}")
        print(f"Max resolution: {resolution}")
        print(f"File extension: {video_ext}")

        print("Speed Test...")
        print("==================")

        avg_speed, downloaded, peak_speed = measure_download_speed(video_url, duration=args.duration, proxy=args.proxy)

        print("==================")
        print(f"Average download speed: {avg_speed:.2f} MB/s")
        print(f"Peak download speed: {peak_speed:.2f} MB/s")
        print(f"Total data downloaded: {downloaded:.2f} MB")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("If the error persists, please make sure you have the latest version of yt-dlp installed.")
        print("You can update it by running: pip install --upgrade yt-dlp")

if __name__ == "__main__":
    main()
