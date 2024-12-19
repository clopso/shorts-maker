from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip

def add_background_music(video_path, music_path, temp_folder, volume=0.1):
    """Adds background music to a video clip."""
    background_music_video = f"{temp_folder}/temp_clip_with_music.mp4"
    video = VideoFileClip(video_path)
    music = AudioFileClip(music_path).volumex(volume)
    music = music.subclip(0, min(video.duration, music.duration))
    
    mixed_audio = CompositeAudioClip([video.audio, music])
    video = video.set_audio(mixed_audio)
    video.write_videofile(background_music_video, codec="libx264", audio_codec="aac")
    return background_music_video