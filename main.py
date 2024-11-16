import os
import random
import subprocess
from moviepy.editor import VideoFileClip, CompositeVideoClip
from moviepy.video.fx.all import mirror_x

height_global = 1920
width_global = 1080

# Ensure temp and output folders exist
os.makedirs("temp", exist_ok=True)
os.makedirs("output", exist_ok=True)

def get_video_duration(video_path):
    """Returns the duration of a video file."""
    cmd = f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {video_path}"
    try:
        return float(subprocess.check_output(cmd, shell=True).decode().strip())
    except Exception as e:
        print(f"Error getting duration of {video_path}: {e}")
        return 0

def divide_video_into_clipes_duration(input_video, clip_duration=50):
    """Divides the input video into segments of a specific duration."""
    video_duration = get_video_duration(input_video)
    clips = [(start, min(start + clip_duration, video_duration)) for start in range(645, int(video_duration), clip_duration - 5)]
    return clips

def divide_video_into_clipes_rendered(input_video, temp_folder, start, end):
    """Renders a specific portion of the input video."""
    clip_output = f"{temp_folder}/temp_clip.mp4"
    cmd = f"ffmpeg -i {input_video} -ss {start} -to {end} -c:v libx264 -crf 27 -preset veryfast -c:a copy {clip_output} -y"
    subprocess.run(cmd, shell=True)
    return clip_output

def pick_random_filler_video(random_videos, temp_folder, clip_duration):
    """Selects a random filler video and extracts a random segment matching the clip duration."""
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

def create_short_videos(input_video, random_videos, output_folder, temp_folder, duration=30):
    """Creates short videos by combining segments from the input video and filler videos."""
    clips = divide_video_into_clipes_duration(input_video, duration)

    for i, (start, end) in enumerate(clips):
        try:
            # Extract the main video clip
            clip_output = divide_video_into_clipes_rendered(input_video, temp_folder, start, end)

            # Select and extract a random segment from a filler video
            random_video_output = pick_random_filler_video(random_videos, temp_folder, duration)

            # # Combine the two video clips
            random_video = VideoFileClip(random_video_output).resize(height_global//3).set_position(("center", "bottom"))
            clip = VideoFileClip(clip_output).resize(height=height_global - random_video.h).set_position(("center", "top"))
            clip = mirror_x(clip)

            final_clip = CompositeVideoClip([clip, random_video], size=(width_global, height_global))  # 9:16 resolution
            output_path = f"{output_folder}/short_video_{i + 1}.mp4"
            final_clip.write_videofile(output_path, fps=30, codec="libx264", threads=8)

            # Clean up temporary files
            os.remove(clip_output)
            os.remove(random_video_output)

            print(f"Video saved to: {output_path}")
        except Exception as e:
            print(f"Error processing clip {i + 1}: {e}")

# Example paths
input_video = "files/familyGuy.mkv"
random_videos_folder = "files/fillers"
random_videos = [
    os.path.join(random_videos_folder, f)
    for f in os.listdir(random_videos_folder)
]

if not random_videos:
    print("No video files found in the folder.")

output_folder = "output"
temp_folder = "temp"

# Create short videos
create_short_videos(input_video, random_videos, output_folder, temp_folder, 50)