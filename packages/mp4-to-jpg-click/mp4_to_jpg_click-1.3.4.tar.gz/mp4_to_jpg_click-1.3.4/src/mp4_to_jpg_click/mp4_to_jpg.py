import cv2
import os
import concurrent.futures
from pathlib import Path
import rich_click as click
from loguru import logger
import math
from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter
from tqdm import tqdm

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
        
        # Get orientation
        orientation = "portrait" if height > width else "landscape"
        logger.info(f"Video orientation: {orientation}")
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        logger.info(f"Total frames in {video_path}: {total_frames}")
        frame_count = 0
        generated_files = []

        with tqdm(
            total=total_frames, desc=f"Processing {Path(video_path).name}"
        ) as pbar:
            for i in range(total_frames):
                if not cap.isOpened():
                    break

                if (max_frames is not None and total_generated[0] >= max_frames) or (
                    max_frames_per_video is not None
                    and len(generated_files) >= max_frames_per_video
                ):
                    break

                ret, frame = cap.read()
                if not ret:
                    break

                # Verify the dimensions of the frame
                if frame.shape[0] != height or frame.shape[1] != width:
                    logger.warning(f"Frame dimensions don't match video properties: frame={frame.shape[1]}x{frame.shape[0]}, video={width}x{height}")
                
                if frame_count % (frame_skip + 1) == 0:
                    # Create frame filename
                    frame_file = os.path.join(
                        output_dir, f"{Path(video_path).stem}_frame{frame_count}.jpg"
                    )
                    
                    # For some codec/containers OpenCV might automatically transpose the image
                    # If dimensions are swapped, rotate the frame to correct orientation
                    if orientation == "portrait" and frame.shape[1] > frame.shape[0]:
                        # Rotate image 90 degrees counter-clockwise
                        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
                        logger.info(f"Rotated frame to match portrait orientation: {frame.shape[1]}x{frame.shape[0]}")
                    
                    # Save the frame with highest quality
                    cv2.imwrite(frame_file, frame, [cv2.IMWRITE_JPEG_QUALITY, 100])
                    
                    # Verify saved file dimensions
                    check_img = cv2.imread(frame_file)
                    if check_img is not None:
                        logger.info(f"Saved image dimensions: {check_img.shape[1]}x{check_img.shape[0]}")
                    
                    generated_files.append(frame_file)
                    total_generated[0] += 1

                frame_count += 1
                pbar.update(1)

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
            f"Processing {video_path} with FPS: {fps}, Duration: {duration} seconds"
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
    total_generated = [
        0
    ]  # Use a list to keep track of the total frames generated across all videos

    with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
        futures = [
            executor.submit(
                process_video,
                video_file,
                output_dir,
                skip_fps_logic,
                skip_time_logic,
                max_frames,
                max_frames_per_video,
                total_generated,
            )
            for video_file in input_files
        ]
        for future in concurrent.futures.as_completed(futures):
            try:
                generated_files.extend(future.result())
            except Exception as e:
                logger.error(f"Error in future: {e}")

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
        print(f"Processing complete. Total JPG files: {total_files}")
    else:
        logger.error("No JPG files generated. Exiting.")


if __name__ == "__main__":
    main()
