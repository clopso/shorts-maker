# Video Processing Script

This Python script processes a primary video file by dividing it into shorter clips, enhancing the video with filler content, adding background music, and applying effects such as mirroring. It is designed to generate dynamic and engaging short videos, suitable for platforms like TikTok or Instagram.

## Features
- Divides input video into segments of specified duration.
- Adds background music to each segment.
- Incorporates random filler videos resized and positioned at the bottom of the final video.
- Applies mirroring effects to the main video.
- Outputs the processed videos in the specified folder.

## Requirements
- Python 3.8+
- FFmpeg (ensure it's installed and added to the system PATH)
- Python libraries:
  - `moviepy`
  - `argparse`
  - `logging`

Install required libraries using pip:
```bash
pip install moviepy
```

## Installation
1. Clone the repository or download the script.
2. Ensure FFmpeg is installed and accessible from the command line.
3. Create `temp` and `output` folders in the script directory (or specify custom paths via arguments).

## Usage
Run the script using the command line:
```bash
python script.py -i <input_video_path> -r <random_videos_folder> [-o <output_folder>] [-t <temp_folder>] [-d <duration>] [-s <speed_factor>]
```

### Arguments:
- `-i`, `--input` (required): Path to the main input video file.
- `-r`, `--random_videos_folder` (required): Path to the folder containing filler videos.
- `-o`, `--output_folder` (optional): Path to the output folder (default: `output`).
- `-t`, `--temp_folder` (optional): Path to the temporary folder (default: `temp`).
- `-d`, `--duration` (optional): Duration of each short video clip in seconds (default: `30`).
- `-s`, `--speed_factor` (optional): Speed factor for the main video clip (default: `1.0`).

## Example
```bash
python script.py -i videos/main_video.mp4 -r videos/random_clips -o output_clips -t temp_clips -d 15 -s 1.5
```

## How It Works
1. **FFmpeg Check:** Verifies FFmpeg is installed and accessible.
2. **Divide Video:** Splits the input video into segments of the specified duration.
3. **Process Clips:**
   - Adjusts video speed and adds background music.
   - Randomly selects a filler video and resizes it to fit below the main clip.
   - Combines both clips into a single video with a mirrored effect.
4. **Output:** Saves the final video to the specified output folder.

## Notes
- Ensure the filler videos are long enough to extract clips of the specified duration.
- Use high-quality input videos for better results.
- Adjust `height_global`, `width_global`, and `start_time` constants in the script for custom video settings.

## Troubleshooting
- **FFmpeg not found:** Install FFmpeg and ensure it is added to the system PATH.
- **Invalid input or folder paths:** Verify the paths provided for input video and filler videos.
- **No filler videos found:** Ensure the folder contains valid video files (`.mp4`, `.mkv`, `.avi`).

## License
This project is licensed under the MIT License.
