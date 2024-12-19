import subprocess
import logging

logger = logging.getLogger(__name__)

def check_ffmpeg():
    """Ensure ffmpeg is installed and accessible."""
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info("ffmpeg is available.")
        return True
    except FileNotFoundError:
        logger.error("ffmpeg is not installed or not in PATH. Please install it to proceed.")
        return False

def get_video_duration(video_path):
    """Returns the duration of a video file."""
    cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{video_path}"'
    try:
        return float(subprocess.check_output(cmd, shell=True).decode().strip())
    except Exception as e:
        logger.error(f"Error getting duration of {video_path}: {e}")
        return 0
