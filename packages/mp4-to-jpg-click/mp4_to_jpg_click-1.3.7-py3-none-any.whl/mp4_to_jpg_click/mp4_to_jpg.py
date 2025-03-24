import cv2
import os
import concurrent.futures
from pathlib import Path
import rich_click as click
from loguru import logger
import math
import subprocess
import json
import shutil
import time
from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter

# Setup loguru for logging
logger.add("./logs/file_{time}.log", rotation="1 MB", backtrace=True, diagnose=True)


def calculate_frame_skip(
    fps,
    duration,
    skip_fps_logic,
    skip_time_logic,
    max_frames=None,
    remaining_frames=None,
):
    """Calculate frame skip based on FPS, duration, and max_frames with logarithmic scaling."""
    if max_frames and remaining_frames is not None:
        total_frames = fps * duration
        frame_skip = max(1, total_frames // remaining_frames - 1)
        return frame_skip

    if not skip_fps_logic and fps <= 30:
        return 1

    if not skip_time_logic and duration <= 60:
        rounded_fps = round(fps / 30) * 30
        return max(1, (rounded_fps // 30) - 1)

    # For longer videos, use logarithmic scaling based on duration
    target_frames = 750 + (3000 - 750) * (math.log10(duration / 60) / math.log10(30))
    total_frames = fps * duration
    frame_skip = max(1, total_frames // target_frames - 1)

    return frame_skip


def print_progress(current, total, video_name, elapsed_time, frames_saved):
    """Print progress bar in a single line."""
    term_width = shutil.get_terminal_size().columns
    bar_length = min(50, term_width - 40)
    
    progress = current / total if total > 0 else 0
    filled_length = int(bar_length * progress)
    bar = '█' * filled_length + '░' * (bar_length - filled_length)
    
    fps = current / elapsed_time if elapsed_time > 0 else 0
    time_left = (total - current) / fps if fps > 0 else 0
    
    # Create status line but ensure it's not too long for the terminal
    status = f"{video_name}: [{bar}] {current}/{total} frames | {frames_saved} saved | {fps:.1f} fps | ETA: {time_left:.1f}s"
    if len(status) > term_width:
        # Truncate video name if needed
        available_space = term_width - (len(status) - len(video_name))
        if available_space > 20:  # Ensure we have enough space for a meaningful name
            truncated_name = video_name[:available_space-3] + "..."
            status = f"{truncated_name}: [{bar}] {current}/{total} frames | {frames_saved} saved | {fps:.1f} fps | ETA: {time_left:.1f}s"
        else:
            # If terminal is very small, simplify the status
            status = f"[{bar}] {current}/{total} | {frames_saved} saved"
    
    # Clear the line completely before printing
    print(f"\r{' ' * term_width}", end='', flush=True)
    print(f"\r{status}", end='', flush=True)


def extract_frames(
    video_path,
    output_dir,
    frame_skip,
    max_frames=None,
    max_frames_per_video=None,
    total_generated=None,
):
    """Extract frames from a video file based on frame skip value."""
    try:
        # Open the video file
        cap = cv2.VideoCapture(video_path)
        
        # Get original video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        logger.info(f"Video resolution: {width}x{height}")
        
        # Get the pixel aspect ratio (SAR) - note that OpenCV doesn't provide this directly
        # We'll check if height and width are equal (square) but video might actually be portrait/landscape
        is_square = width == height
        needs_resize = False
        target_width, target_height = width, height
        
        # Try to get additional video info using ffprobe if available
        try:
            # Run ffprobe to get detailed video information
            cmd = [
                "ffprobe", "-v", "quiet", "-print_format", "json",
                "-show_format", "-show_streams", video_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                video_info = json.loads(result.stdout)
                # Find the video stream
                video_stream = next((s for s in video_info.get("streams", []) if s.get("codec_type") == "video"), None)
                
                if video_stream:
                    # Check for pixel aspect ratio (SAR) and display aspect ratio (DAR)
                    sar = video_stream.get("sample_aspect_ratio", "1:1")
                    dar = video_stream.get("display_aspect_ratio", "1:1")
                    
                    # Parse ratios to determine true orientation
                    def parse_ratio(ratio_str):
                        if ":" in ratio_str:
                            num, den = map(int, ratio_str.split(":"))
                            return num / den
                        return 1.0
                    
                    sar_value = parse_ratio(sar)
                    dar_value = parse_ratio(dar)
                    
                    # Determine correct orientation based on DAR
                    if is_square and dar_value != 1.0:
                        if dar_value < 1.0:
                            # The video is actually portrait despite square dimensions
                            needs_resize = True
                            target_width = int(width * sar_value)
                            target_height = height
                        elif dar_value > 1.0:
                            # The video is actually landscape despite square dimensions
                            needs_resize = True
                            target_width = width
                            target_height = int(height / sar_value)
        except Exception as e:
            logger.warning(f"Failed to get detailed video info: {e}")
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        logger.info(f"Total frames in {video_path}: {total_frames}")
        frame_count = 0
        frames_saved = 0
        generated_files = []
        
        # Setup progress tracking
        video_name = Path(video_path).stem
        start_time = time.time()
        last_progress_update = 0

        # Print initial empty progress bar
        print_progress(0, total_frames, video_name, 0.1, 0)

        while True:
            if not cap.isOpened():
                break

            if (max_frames is not None and total_generated[0] >= max_frames) or (
                max_frames_per_video is not None
                and frames_saved >= max_frames_per_video
            ):
                break

            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % (frame_skip + 1) == 0:
                # Create frame filename
                frame_file = os.path.join(
                    output_dir, f"{Path(video_path).stem}_frame{frame_count}.jpg"
                )
                
                # Apply necessary transformations to respect aspect ratio
                if needs_resize:
                    frame = cv2.resize(frame, (target_width, target_height), interpolation=cv2.INTER_LANCZOS4)
                
                # Save the frame with highest quality
                cv2.imwrite(frame_file, frame, [cv2.IMWRITE_JPEG_QUALITY, 100])
                
                generated_files.append(frame_file)
                total_generated[0] += 1
                frames_saved += 1

            frame_count += 1
            
            # Update progress at a reasonable rate (no more than 5 updates per second)
            current_time = time.time()
            if current_time - last_progress_update > 0.2 or frame_count == total_frames:
                elapsed = current_time - start_time
                print_progress(frame_count, total_frames, video_name, elapsed, frames_saved)
                last_progress_update = current_time
        
        # Final progress update to ensure 100% is shown
        print_progress(total_frames, total_frames, video_name, time.time() - start_time, frames_saved)
        print()  # Add a newline after progress bar completes
        
        logger.info(f"Saved {frames_saved} frames from {video_path}")
        cap.release()
        return generated_files
    except Exception as e:
        logger.error(f"Error processing {video_path}: {e}")
        return []


def process_video(
    video_path,
    output_dir,
    skip_fps_logic,
    skip_time_logic,
    max_frames=None,
    max_frames_per_video=None,
    total_generated=None,
):
    """Process a single video file to extract frames."""
    try:
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps
        logger.info(
            f"Processing {video_path} with FPS: {fps}, Duration: {duration:.2f} seconds"
        )
        cap.release()

        frame_skip = calculate_frame_skip(
            fps,
            duration,
            skip_fps_logic,
            skip_time_logic,
            max_frames,
            max_frames - total_generated[0] if max_frames else None,
        )

        return extract_frames(
            video_path,
            output_dir,
            frame_skip,
            max_frames,
            max_frames_per_video,
            total_generated,
        )
    except Exception as e:
        logger.error(f"Error processing {video_path}: {e}")
        return []


def find_and_process_videos(
    input_files,
    output_dir,
    skip_fps_logic,
    skip_time_logic,
    max_frames=None,
    max_frames_per_video=None,
):
    """Process video files in parallel and return list of generated JPG files."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    generated_files = []
    total_generated = [0]  # Use a list to keep track of the total frames generated across all videos
    
    print(f"\nProcessing {len(input_files)} video(s)...")
    
    # Process videos one at a time for clearer progress display
    for video_file in input_files:
        result = process_video(
            video_file,
            output_dir,
            skip_fps_logic,
            skip_time_logic,
            max_frames,
            max_frames_per_video,
            total_generated,
        )
        generated_files.extend(result)

    return generated_files


def is_video_file(path):
    """Check if path is a video file with allowed extensions."""
    return path.lower().endswith((".mp4", ".mov")) and not path.startswith(".")


def is_visible_dir(path):
    """Check if path is a visible directory."""
    return os.path.isdir(path) and not os.path.basename(path).startswith(".")


def get_filtered_paths():
    """Get filtered paths for the current directory."""
    paths = []
    try:
        for path in os.listdir("."):
            # Add visible directories
            if is_visible_dir(path):
                paths.append(path + os.sep)  # Add separator for directories
            # Add visible video files
            elif is_video_file(path):
                paths.append(path)
    except Exception as e:
        logger.error(f"Error listing directory: {e}")
    return paths


def cli_select_input_files():
    """Select multiple video files via CLI with path completion."""
    input_files = []
    file_completer = PathCompleter(
        only_directories=False, expanduser=True, min_input_len=0
    )

    print("\nEnter the paths of the video files (type 'done' when finished)")
    print("Tips: - Use Tab for completion")
    print("      - Type '..' for parent directory")
    print("      - Only .mp4/.mov files will be processed\n")

    while True:
        try:
            path = prompt(
                "Video path: ",
                completer=file_completer,
                complete_while_typing=True,
                complete_in_thread=True,
            ).strip()

            if path.lower() == "done":
                break

            if os.path.isfile(path) and is_video_file(path):
                input_files.append(os.path.abspath(path))
                print(f"Added: {path}")
            else:
                print(f"Not a valid video file: {path}")
        except KeyboardInterrupt:
            print("\nInput selection cancelled.")
            break

    return input_files


def cli_select_output_directory():
    """Select output directory via CLI with path completion."""
    dir_completer = PathCompleter(
        only_directories=True, expanduser=True, min_input_len=0
    )

    print("\nSelect the output directory for the extracted frames")
    print("Tips: - Use Tab for completion")
    print("      - Type '..' for parent directory\n")

    while True:
        try:
            output_dir = prompt(
                "Output directory: ",
                completer=dir_completer,
                complete_while_typing=True,
                complete_in_thread=True,
            ).strip()

            if os.path.isdir(output_dir):
                return os.path.abspath(output_dir)
            else:
                create = (
                    prompt(
                        f"Directory '{output_dir}' doesn't exist. Create it? [y/N]: "
                    )
                    .lower()
                    .strip()
                )

                if create == "y":
                    try:
                        os.makedirs(output_dir, exist_ok=True)
                        return os.path.abspath(output_dir)
                    except Exception as e:
                        print(f"Error creating directory: {e}")
                else:
                    print("Please select a valid directory.")
        except KeyboardInterrupt:
            print("\nDirectory selection cancelled.")
            return None


@click.command()
@click.option(
    "--no-fps-skip", is_flag=True, help="Turn off frame skipping based on FPS"
)
@click.option(
    "--no-time-skip", is_flag=True, help="Turn off frame skipping based on time"
)
@click.option(
    "--max-frames",
    default=None,
    type=int,
    help="Maximum number of frames to generate across all videos",
)
@click.option(
    "--max-frames-per-video",
    default=None,
    type=int,
    help="Maximum number of frames to generate per video",
)
def main(
    no_fps_skip,
    no_time_skip,
    max_frames,
    max_frames_per_video,
):
    """Main function to execute the script."""
    logger.info("Starting video frame extraction tool.")

    input_files = cli_select_input_files()
    output_dir = cli_select_output_directory()

    if not input_files:
        logger.error("No input files selected. Exiting.")
        return

    if not output_dir:
        logger.error("No output directory selected. Exiting.")
        return

    generated_files = find_and_process_videos(
        input_files,
        output_dir,
        no_fps_skip,
        no_time_skip,
        max_frames,
        max_frames_per_video,
    )

    if generated_files:
        total_files = len(generated_files)
        logger.info(f"Processing complete. Total JPG files: {total_files}")
        print(f"\nProcessing complete. Total JPG files: {total_files}")
    else:
        logger.error("No JPG files generated. Exiting.")
        print("\nNo JPG files generated. Exiting.")


if __name__ == "__main__":
    main()
