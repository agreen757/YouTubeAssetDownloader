import os
import re
import sys
import time
from pathlib import Path
from typing import Callable

def create_safe_filename(title: str) -> str:
    """Create a safe filename from video title."""
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', title)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    # Limit length
    return filename[:100]

def validate_directory(path: str) -> bool:
    """Validate and create directory if it doesn't exist."""
    try:
        directory = Path(path)
        directory.mkdir(parents=True, exist_ok=True)
        return directory.is_dir() and os.access(path, os.W_OK)
    except Exception:
        return False

def format_bytes(bytes_count: float) -> str:
    """Format bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_count < 1024.0:
            return f"{bytes_count:.1f} {unit}"
        bytes_count /= 1024.0
    return f"{bytes_count:.1f} TB"

def format_time(seconds: int) -> str:
    """Format seconds to HH:MM:SS."""
    if seconds < 0:
        return '--:--:--'
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

def show_progress(d: dict) -> None:
    """Display download progress."""
    if d['status'] == 'downloading':
        # Calculate progress
        total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
        downloaded_bytes = d.get('downloaded_bytes', 0)
        
        if total_bytes > 0:
            # Calculate percentage and create progress bar
            percent = downloaded_bytes / total_bytes * 100
            width = 50
            filled = int(width * percent / 100)
            bar = '█' * filled + '-' * (width - filled)
            
            # Calculate speed and ETA
            speed = d.get('speed', 0)
            eta = d.get('eta', 0)
            
            # Create status line
            status = (
                f'\r{d["info_dict"]["title"][:40]:<40} '
                f'[{bar}] {percent:5.1f}% '
                f'| {format_bytes(downloaded_bytes)}/{format_bytes(total_bytes)} '
                f'| {format_bytes(speed)}/s '
                f'| ETA: {format_time(eta)}'
            )
            
            # Print status
            sys.stdout.write(status)
            sys.stdout.flush()
    
    elif d['status'] == 'finished':
        sys.stdout.write('\n')
        sys.stdout.flush()
