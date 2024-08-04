.DEFAULT_GOAL := help
.PHONY: help analyze ping download

help:
	@echo "YouTube URL Analyzer, Ping, and Downloader Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  help     : Show this help message"
	@echo "  ping     : Run the ping script to measure download speed"
	@echo "  analyze  : Run the analyzer script"
	@echo "  download : Download videos from a list of URLs"
	@echo ""
	@echo "========================================"
	@echo "Ping - Measure YouTube video download speed"
	@echo "========================================"
	@echo "Usage:"
	@echo "  make ping [URL=<video_url>] [DURATION=<seconds>] [PROXY=<proxy_url>] [DEBUG=1]"
	@echo ""
	@echo "Parameters:"
	@echo "  URL      : (Optional) YouTube video URL to test"
	@echo "  DURATION : (Optional) Duration of the speed test in seconds (default: 20)"
	@echo "  PROXY    : (Optional) Proxy server to use"
	@echo "  DEBUG    : (Optional) Set to 1 to enable debug output"
	@echo ""
	@echo "Example:"
	@echo "  make ping URL=https://www.youtube.com/watch?v=dQw4w9WgXcQ DURATION=30 PROXY=socks5://127.0.0.1:9150 DEBUG=1"
	@echo ""
	@echo "========================================"
	@echo "Analyze - Extract video URLs from a list"
	@echo "========================================"
	@echo "Usage:"
	@echo "  make analyze INPUT=<input_file> [OUTPUT=<output_file>]"
	@echo ""
	@echo "Parameters:"
	@echo "  INPUT    : (Required) Input file containing URLs to analyze"
	@echo "  OUTPUT   : (Optional) Output file for video URLs (default: video.txt)"
	@echo ""
	@echo "Example:"
	@echo "  make analyze INPUT=urls.txt OUTPUT=results.txt"
	@echo ""
	@echo "========================================"
	@echo "Download - Download videos from a list of URLs"
	@echo "========================================"
	@echo "Usage:"
	@echo "  make download INPUT=<input_file> [OUTPUT_DIR=<output_directory>] [OUTPUT_RESULT=<result_file>] [MAX_QUALITY=<quality>] [DEBUG=1]"
	@echo ""
	@echo "Parameters:"
	@echo "  INPUT         : (Required) Input file with video URLs to download"
	@echo "  OUTPUT_DIR    : (Optional) Output directory for downloaded videos (default: output)"
	@echo "  OUTPUT_RESULT : (Optional) Output file for download results (default: done.txt)"
	@echo "  MAX_QUALITY   : (Optional) Maximum video quality to download (e.g., 720, 1080)"
	@echo "  DEBUG         : (Optional) Set to 1 to enable debug output"
	@echo ""
	@echo "Example:"
	@echo "  make download INPUT=video_list.txt OUTPUT_DIR=downloads OUTPUT_RESULT=results.txt MAX_QUALITY=720 DEBUG=1"

install:
	pip3 install yt-dlp requests moviepy

analyze:
	@if [ -z "$(INPUT)" ]; then \
		echo "Error: INPUT parameter is required."; \
		echo "Usage: make analyze INPUT=<input_file> [OUTPUT=<output_file>]"; \
		exit 1; \
	fi
	@if [ -z "$(OUTPUT)" ]; then \
		python main_analyze.py --input=$(INPUT); \
	else \
		python main_analyze.py --input=$(INPUT) --output-result=$(OUTPUT); \
	fi

ping:
	@python main_ping.py $(if $(URL),--url=$(URL)) $(if $(DURATION),--duration=$(DURATION)) $(if $(PROXY),--proxy=$(PROXY)) $(if $(DEBUG),--debug)

download:
	@if [ -z "$(INPUT)" ]; then \
		echo "Error: INPUT parameter is required."; \
		echo "Usage: make download INPUT=<input_file> [OUTPUT_DIR=<output_directory>] [OUTPUT_RESULT=<result_file>] [MAX_QUALITY=<quality>] [DEBUG=1]"; \
		exit 1; \
	fi
	@python main_download.py --input=$(INPUT) $(if $(OUTPUT_DIR),--output-dir=$(OUTPUT_DIR)) $(if $(OUTPUT_RESULT),--output-result=$(OUTPUT_RESULT)) $(if $(MAX_QUALITY),--max-quality=$(MAX_QUALITY)) $(if $(DEBUG),--debug)
