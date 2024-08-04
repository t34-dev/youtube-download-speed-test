import yt_dlp
import time
import random

def analyze_youtube_url(url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
    }

    max_retries = 3
    retry_delay = 10

    for attempt in range(max_retries):
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

                if isinstance(info, dict):
                    if info.get('_type') == 'playlist':
                        # It's a playlist or channel
                        return [entry['url'] for entry in info['entries'] if entry.get('url')]
                    elif info.get('_type') == 'url' or (info.get('webpage_url') and 'youtube.com' in info['webpage_url']):
                        # It's a single video
                        return [info.get('webpage_url') or info.get('url')]
                    else:
                        print(f"Unsupported URL type: {info.get('_type')}")
                        return []
                else:
                    print(f"Unexpected data type: {type(info)}")
                    return []

        except yt_dlp.utils.DownloadError as e:
            if 'HTTP Error 429' in str(e):
                if attempt < max_retries - 1:
                    wait_time = retry_delay + random.uniform(0, 5)
                    print(f"Too many requests. Waiting {wait_time:.2f} seconds before retrying...")
                    time.sleep(wait_time)
                else:
                    print("Maximum number of attempts reached. Failed to get information.")
                    return []
            else:
                print(f"An error occurred during download: {str(e)}")
                return []
        except Exception as e:
            print(f"Unknown error: {str(e)}")
            return []

def collect_all_video_urls(urls):
    all_video_urls = []
    for url in urls:
        print(f"\nAnalyzing URL: {url}")
        video_urls = analyze_youtube_url(url)
        print(f"Videos found: {len(video_urls)}")
        all_video_urls.extend(video_urls)
    return all_video_urls


