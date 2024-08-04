import argparse
from url_analyzer import collect_all_video_urls

def main():
    parser = argparse.ArgumentParser(description="Analyze YouTube URLs and collect video links.")
    parser.add_argument("--input", required=True, help="Input file containing URLs to analyze")
    parser.add_argument("--output-result", default="video.txt", help="Output file for video URLs (default: video.txt)")
    args = parser.parse_args()

    # Read URLs from input file
    with open(args.input, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip()]

    all_video_urls = collect_all_video_urls(urls)
    print(f"\nTotal number of videos found: {len(all_video_urls)}")

    # Write video URLs to output file
    with open(args.output_result, 'w', encoding='utf-8') as f:
        for video_url in all_video_urls:
            f.write(f"{video_url}\n")

    print(f"List of video URLs saved to '{args.output_result}'")

if __name__ == "__main__":
    main()
