# YouTube Video Analyzer and Downloader

A comprehensive toolkit for analyzing and downloading YouTube videos, playlists.

## Key Features:
- URL analysis for single videos, playlists, and channels
- High-quality video downloading
- Download speed testing
- Proxy support
- Detailed debug information
- Results logging

Built with yt-dlp and moviepy for robust YouTube interaction and video processing.

## Main Components:
- `main_analyze.py`: URL analysis and video info collection
- `main_download.py`: Video downloading
- `main_ping.py`: Download speed testing

Utilizes a Makefile for easy task execution and project management.

## Table of Contents

1. [Installation](#installation)
2. [Ping - Measure YouTube Video Download Speed](#ping---measure-youtube-video-download-speed)
3. [Analyze - Extract Video URLs from a List](#analyze---extract-video-urls-from-a-list)
4. [Download - Download Videos from a List of URLs](#download---download-videos-from-a-list-of-urls)

## Installation

To install the required dependencies, run:

```
make install
```

This will install `yt-dlp`, `requests`, and `moviepy` using pip3.

Make sure you have Python 3 and pip installed on your system before running this command.

## Ping - Measure YouTube Video Download Speed

The `ping` tool allows you to measure the download speed for a YouTube video.

### Usage

```
make ping [URL=<video_url>] [DURATION=<seconds>] [PROXY=<proxy_url>] [DEBUG=1]
```

### Parameters

- `URL`: (Optional) YouTube video URL to test
- `DURATION`: (Optional) Duration of the speed test in seconds (default: 20)
- `PROXY`: (Optional) Proxy server to use
- `DEBUG`: (Optional) Set to 1 to enable debug output

### Example

```
make ping URL=https://www.youtube.com/watch?v=dQw4w9WgXcQ DURATION=30 PROXY=socks5://127.0.0.1:9150 DEBUG=1
```

This command will:
1. Test the download speed for the specified YouTube video
2. Run the test for 30 seconds
3. Use the specified SOCKS5 proxy
4. Enable debug output

The script will display real-time information about the download speed, including current speed, peak speed, and total data downloaded. At the end of the test, it will show the average download speed, peak download speed, and total data downloaded.

## Analyze - Extract Video URLs from a List

The `analyze` tool extracts video URLs from a list of YouTube URLs, which may include playlist URLs.

### Usage

```
make analyze INPUT=<input_file> [OUTPUT=<output_file>]
```

### Parameters

- `INPUT`: (Required) Input file containing URLs to analyze
- `OUTPUT`: (Optional) Output file for video URLs (default: video.txt)

### Example

```
make analyze INPUT=urls.txt OUTPUT=results.txt
```

This command will:
1. Read URLs from the `urls.txt` file
2. Extract all video URLs, including those from playlists
3. Save the extracted video URLs to `results.txt`

The script will display the total number of videos found and confirm where the list of video URLs has been saved.

## Download - Download Videos from a List of URLs

The `download` tool allows you to download videos from a list of YouTube URLs.

### Usage

```
make download INPUT=<input_file> [OUTPUT_DIR=<output_directory>] [OUTPUT_RESULT=<result_file>] [MAX_QUALITY=<quality>] [DEBUG=1]
```

### Parameters

- `INPUT`: (Required) Input file with video URLs to download
- `OUTPUT_DIR`: (Optional) Output directory for downloaded videos (default: output)
- `OUTPUT_RESULT`: (Optional) Output file for download results (default: done.txt)
- `MAX_QUALITY`: (Optional) Maximum video quality to download (e.g., 720, 1080)
- `DEBUG`: (Optional) Set to 1 to enable debug output

### Example

```
make download INPUT=video_list.txt OUTPUT_DIR=downloads OUTPUT_RESULT=results.txt MAX_QUALITY=720 DEBUG=1
```

This command will:
1. Read video URLs from `video_list.txt`
2. Download videos to the `downloads` directory
3. Save download results to `results.txt`
4. Limit the maximum video quality to 720p
5. Enable debug output

The script will display progress information for each video, including the title, resolution, and file format. After processing all videos, it will show where the results have been saved.

## Notes

- All scripts use `yt-dlp` for video information extraction and downloading. Make sure you have the latest version installed.
- The download script uses `moviepy` for merging video and audio streams if they are separate.
- If you encounter any errors, try updating `yt-dlp` by running: `pip install --upgrade yt-dlp`

## Contributing

Feel free to submit issues or pull requests if you have any improvements or bug fixes for these tools.

## License

This project is licensed under the ISC License.

---

Developed with ❤️ by [T34](https://github.com/t34-dev)
