#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from typing import Tuple, List
import yt_dlp
from helpers import create_safe_filename, validate_directory, show_progress

def download_video(url: str, output_path: str) -> bool:
    """Process YouTube video download."""
    try:
        print(f"\nInitializing download for: {url}")
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'writethumbnail': True,
            'progress_hooks': [show_progress],
            'quiet': True,
            'no_warnings': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Get video info
            info = ydl.extract_info(url, download=False)
            print(f"\nVideo details:")
            print(f"Title: {info['title']}")
            print(f"Duration: {info['duration']} seconds")
            print(f"View count: {info['view_count']}")
            
            # Download video and extract audio
            ydl.download([url])
            print("\nDownload completed successfully!")
            return True

    except Exception as e:
        print(f"Error occurred while downloading {url}: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        return False

def read_urls_from_file(file_path: str) -> List[str]:
    """Read URLs from a text file."""
    try:
        with open(file_path, 'r') as f:
            # Remove empty lines and strip whitespace
            urls = [line.strip() for line in f if line.strip()]
        return urls
    except Exception as e:
        print(f"Error reading URL file: {str(e)}")
        sys.exit(1)

def main():
    """Main function to handle user input and process download."""
    if len(sys.argv) not in [3, 4]:
        print("Usage:")
        print("Single URL: python youtube_downloader.py <youtube_url> <output_path>")
        print("Batch mode: python youtube_downloader.py --batch <urls_file> <output_path>")
        sys.exit(1)

    # Parse arguments
    is_batch_mode = sys.argv[1] == '--batch'
    if is_batch_mode:
        if len(sys.argv) != 4:
            print("Batch mode requires a URL file and output path")
            sys.exit(1)
        urls_file = sys.argv[2]
        output_path = sys.argv[3]
        urls = read_urls_from_file(urls_file)
    else:
        url = sys.argv[1]
        output_path = sys.argv[2]
        urls = [url]

    # Validate directory
    if not validate_directory(output_path):
        print(f"Error: Cannot access or create directory: {output_path}")
        sys.exit(1)

    # Process downloads
    total_urls = len(urls)
    successful = 0
    failed = 0

    print(f"Starting download of {total_urls} video{'s' if total_urls > 1 else ''}")
    print(f"Output directory: {output_path}")

    for i, url in enumerate(urls, 1):
        print(f"\nProcessing video {i}/{total_urls}")
        if download_video(url, output_path):
            successful += 1
        else:
            failed += 1

    # Print summary
    print("\nDownload Summary:")
    print(f"Total videos: {total_urls}")
    print(f"Successfully downloaded: {successful}")
    print(f"Failed: {failed}")

if __name__ == "__main__":
    main()
