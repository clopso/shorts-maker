import os
import gradio as gr
from utils.ffmpeg_utils import check_ffmpeg
from utils.short_video_creator import create_short_videos

def gradio_process(input_video, start_seconds, max_clip_count, random_videos_folder, duration, speed_factor, background_music, background_volume):
    temp_folder = "temp"
    output_folder = "output"
    if not check_ffmpeg():
        return "FFmpeg not installed. Please install FFmpeg to use this tool."

    # Ensure folders exist
    os.makedirs(temp_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    # Get list of random videos
    random_videos = [
        os.path.join(random_videos_folder, f)
        for f in os.listdir(random_videos_folder)
        if f.lower().endswith((".mp4", ".mkv", ".avi"))
    ]
    if not random_videos:
        return "No valid filler videos found in the folder."

    # Process video
    create_short_videos(input_video, random_videos, start_seconds, output_folder, temp_folder, duration, speed_factor, max_clip_count, background_music, background_volume)

    return "Processing complete!"

def launch_interface():
    interface = gr.Interface(
        fn=gradio_process,
        inputs=[
            gr.File(label="Main Video File", type="filepath", file_types=[".mp4", ".mkv", ".avi"]),
            gr.Number(label="Start Time (in seconds)", value=0, step=1),
            gr.Number(label="Max Clip Count", value=5),
            gr.Textbox(label="Path of Folder with Filler Videos"),
            gr.Slider(10, 120, step=1, value=30, label="Clip Duration (seconds)"),
            gr.Slider(0.5, 1.5, step=0.05, value=1.0, label="Speed Factor"),
            gr.File(label="Background Music File", type="filepath", file_types=[".mp3"]),
            gr.Slider(0.01, 1.0, step=0.01, value=0.1, label="Background Music Volume")
        ],
        outputs="text",
        title="Short Video Creator"
    )
    interface.launch()
