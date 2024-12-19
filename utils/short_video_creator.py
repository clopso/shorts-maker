from moviepy.editor import VideoFileClip, CompositeVideoClip
from moviepy.video.fx.all import mirror_x
from datetime import datetime
import os
import logging
from utils.video_processing import divide_video_into_clips, render_video_segment, pick_random_filler_video
from utils.audio_processing import add_background_music
from utils.constants import HEIGHT_GLOBAL, WIDTH_GLOBAL

logger = logging.getLogger()

height_global = HEIGHT_GLOBAL
width_global = WIDTH_GLOBAL

def create_short_videos(input_video, random_videos, start_seconds, output_folder, temp_folder, duration=30, speed_factor=1.0, max_clip_count=10, background_music="", background_volume=0.1):
    """Creates short videos by combining segments from the input video and filler videos."""
    clips = divide_video_into_clips(input_video, start_seconds, duration, max_clip_count)

    for i, (start, end) in enumerate(clips):
        try:
            print(f"Processing clip {i + 1} ({start}-{end}s)")
            logger.info(f"Processing clip {i + 1} ({start}-{end}s)")

            # Extract the main video clip
            clip_output = render_video_segment(input_video, temp_folder, start, end, speed_factor=speed_factor)
            clip_output = add_background_music(clip_output, background_music, temp_folder, background_volume)

            print(clip_output)

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