import cv2
import os
import argparse
from typing import Optional


def extract_frames(video_path: str, output_dir: str, interval: int = 1, image_format: str = "jpg"):
    """
    Extracts frames from a video and saves them as images.
    
    :param video_path: Path to the input video file.
    :param output_dir: Directory to save extracted frames.
    :param interval: Interval at which to extract frames (in seconds).
    :param image_format: Image format to save frames (jpg or png).
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("Error opening video file")

    fps = int(cap.get(cv2.CAP_PROP_FPS))  # Frames per second
    frame_interval = fps * interval  # Convert seconds to frame count
    frame_count = 0
    extracted_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            frame_filename = os.path.join(output_dir, f"frame_{extracted_count}.{image_format}")
            cv2.imwrite(frame_filename, frame)
            extracted_count += 1

        frame_count += 1

    cap.release()
    print(f"Extracted {extracted_count} frames and saved to {output_dir}")


def main():
    parser = argparse.ArgumentParser(description="Extract frames from a video.")
    parser.add_argument("video_path", type=str, help="Path to the video file.")
    parser.add_argument("output_dir", type=str, help="Directory to save frames.")
    parser.add_argument("--interval", type=int, default=1, help="Interval in seconds to extract frames.")
    parser.add_argument("--format", type=str, choices=["jpg", "png"], default="jpg", help="Image format.")
    
    args = parser.parse_args()
    extract_frames(args.video_path, args.output_dir, args.interval, args.format)


if __name__ == "__main__":
    main()
