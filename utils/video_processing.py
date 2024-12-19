import os
import random
from .ffmpeg_utils import get_video_duration

def divide_video_into_clips(input_video, start_time, clip_duration, max_clip_count):
    """Divides the input video into segments of a specific duration."""
    video_duration = get_video_duration(input_video)
    if video_duration < start_time:
        raise ValueError(f"Start time ({start_time}s) is greater than the video duration ({video_duration}s).")
    clips = [(start, min(start + clip_duration, video_duration)) for start in range(start_time, int(video_duration), clip_duration - 5)]
    if len(clips) > max_clip_count:
        clips = random.sample(clips, max_clip_count)
    return clips

def render_video_segment(input_video, temp_folder, start, end, speed_factor):
    """Renders a specific portion of the input video with a speed change."""
    clip_output = f"{temp_folder}/temp_clip.mp4"
    video_filter = f"setpts=PTS/{speed_factor}"
    audio_filter = f"atempo={speed_factor}" if 0.5 <= speed_factor <= 2.0 else "atempo=1.0"
    cmd = (
        f'ffmpeg -i "{input_video}" -ss {start} -to {end} '
        f'-filter:v "{video_filter}" -filter:a "{audio_filter}" '
        f'-c:v libx264 -crf 27 -preset veryfast -c:a aac "{clip_output}" -y'
    )
    os.system(cmd)
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
    cmd = f'ffmpeg -i "{random_video}" -ss {start} -to {end} -c:v copy -an "{random_video_output}" -y'
    os.system(cmd)
    return random_video_output
