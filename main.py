import os
import random
import subprocess
from datetime import datetime
from moviepy.editor import VideoFileClip, CompositeVideoClip, AudioFileClip, CompositeAudioClip
from moviepy.video.fx.all import mirror_x
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Constants for global settings
height_global = 1920
width_global = 1080
start_time = 1300

# Ensure temp and output folders exist
os.makedirs("temp", exist_ok=True)
os.makedirs("output", exist_ok=True)

def check_ffmpeg():
    """Ensure ffmpeg is installed and accessible."""
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info("ffmpeg is available.")
    except FileNotFoundError:
        logger.error("ffmpeg is not installed or not in PATH. Please install it to proceed.")
        exit(1)

def get_video_duration(video_path):
    """Returns the duration of a video file."""
    cmd = f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {video_path}"
    try:
        return float(subprocess.check_output(cmd, shell=True).decode().strip())
    except Exception as e:
        logger.error(f"Error getting duration of {video_path}: {e}")
        return 0

def divide_video_into_clips(input_video, clip_duration=50):
    """Divides the input video into segments of a specific duration."""
    video_duration = get_video_duration(input_video)
    clips = [(start, min(start + clip_duration, video_duration)) for start in range(start_time, int(video_duration), clip_duration - 5)]
    return clips

def render_video_segment(input_video, temp_folder, start, end):
    """Renders a specific portion of the input video."""
    clip_output = f"{temp_folder}/temp_clip.mp4"
    cmd = f"ffmpeg -i {input_video} -ss {start} -to {end} -c:v libx264 -crf 27 -preset veryfast -c:a copy {clip_output} -y"
    subprocess.run(cmd, shell=True)
    return clip_output

def pick_random_filler_video(random_videos, temp_folder, clip_duration):
    """Selects and extracts a random segment from a filler video."""
    random_video = random.choice(random_videos)
    video_duration = get_video_duration(random_video)

    if video_duration < clip_duration:
        raise ValueError(f"Filler video {random_video} is shorter than the clip duration ({clip_duration}s).")

    start = random.uniform(0, video_duration - clip_duration)
    end = start + clip_duration

    random_video_output = f"{temp_folder}/temp_random_video.mp4"
    cmd = f"ffmpeg -i {random_video} -ss {start} -to {end} -c:v copy -an {random_video_output} -y"
    subprocess.run(cmd, shell=True)
    return random_video_output

def add_background_music(video_path, music_path, temp_folder, volume=0.1):
    """Adds background music to a video."""
    background_music_video = f"{temp_folder}/temp_clip_with_music.mp4"
    video = VideoFileClip(video_path)
    music = AudioFileClip(music_path).volumex(volume)
    music = music.subclip(0, min(video.duration, music.duration))

    mixed_audio = CompositeAudioClip([video.audio, music])
    video = video.set_audio(mixed_audio)
    video.write_videofile(background_music_video, codec="libx264", audio_codec="aac")
    return background_music_video

def create_short_videos(input_video, random_videos, output_folder, temp_folder, duration=30):
    """Creates short videos by combining segments from the input video and filler videos."""
    clips = divide_video_into_clips(input_video, duration)

    for i, (start, end) in enumerate(clips):
        try:
            logger.info(f"Processing clip {i + 1} ({start}-{end}s)")

            # Extract the main video clip
            clip_output = render_video_segment(input_video, temp_folder, start, end)
            clip_output = add_background_music(clip_output, "files/background-lofi.mp3", temp_folder, 0.01)

            # Extract and resize a filler video
            random_video_output = pick_random_filler_video(random_videos, temp_folder, duration)
            random_video = VideoFileClip(random_video_output).resize(height=height_global // 3).set_position(("center", "bottom"))

            # Prepare the main video clip
            clip = VideoFileClip(clip_output).resize(height=height_global - random_video.h).set_position(("center", "top"))
            clip = mirror_x(clip)

            # Combine the clips
            final_clip = CompositeVideoClip([clip, random_video], size=(width_global, height_global))
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            output_path = f"{output_folder}/short_video_{i + 1}_{timestamp}.mp4"
            final_clip.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac")

            # Clean up temporary files
            os.remove(clip_output)
            os.remove(random_video_output)

            logger.info(f"Video saved to: {output_path}")
        except Exception as e:
            logger.error(f"Error processing clip {i + 1}: {e}")

# Ensure ffmpeg is installed
check_ffmpeg()

# Example paths
input_video = "files/doiscarasBR.mkv"
random_videos_folder = "files/fillers"
random_videos = [
    os.path.join(random_videos_folder, f)
    for f in os.listdir(random_videos_folder)
    if f.lower().endswith(('.mp4', '.mkv', '.avi'))
]

if not os.path.isfile(input_video):
    logger.error(f"Input video '{input_video}' does not exist.")
    exit(1)

if not random_videos:
    logger.error("No valid filler video files found in the folder.")
    exit(1)

output_folder = "output"
temp_folder = "temp"

# Create short videos
create_short_videos(input_video, random_videos, output_folder, temp_folder, 70)
