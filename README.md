# YouTube Audio and Thumbnail Downloader

A Python script to download audio and thumbnails from YouTube videos.

## Features

- Downloads audio in MP3 format
- Downloads video thumbnails
- Shows download progress
- Handles errors gracefully
- Creates safe filenames
- Validates download directory
- Supports batch downloading from URL list

## Requirements

- Python 3.7+
- yt-dlp
- FFmpeg

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Single Video Download
```bash
python youtube_downloader.py <youtube_url> <output_path>
```

Example:
```bash
python youtube_downloader.py https://www.youtube.com/watch?v=example ./downloads
```

### Batch Download
To download multiple videos at once, create a text file containing YouTube URLs (one per line) and use the `--batch` option:

```bash
python youtube_downloader.py --batch <urls_file> <output_path>
```

Example:
```bash
python youtube_downloader.py --batch urls.txt ./downloads
```

Sample URLs file format (urls.txt):
```
https://www.youtube.com/watch?v=example1
https://www.youtube.com/watch?v=example2
https://www.youtube.com/watch?v=example3
```

## Output

The script will:
1. Create the output directory if it doesn't exist
2. Download each video's audio in MP3 format
3. Download each video's thumbnail
4. Save all files in the specified output directory
5. Display progress for each download
6. Show a summary of successful and failed downloads

## Error Handling

- The script handles invalid URLs and network errors gracefully
- Failed downloads are reported in the summary
- The process continues even if some downloads fail
