import argparse
from .extractor import extract_frames

def main():
    parser = argparse.ArgumentParser(description="Extract frames from a video using FrameSnap.")
    parser.add_argument("video_path", type=str, help="Path to the video file.")
    parser.add_argument("output_dir", type=str, help="Directory to save extracted frames.")
    parser.add_argument("--interval", type=int, default=1, help="Interval in seconds to extract frames.")
    parser.add_argument("--format", type=str, choices=["jpg", "png"], default="jpg", help="Image format (jpg or png).")

    args = parser.parse_args()
    extract_frames(args.video_path, args.output_dir, args.interval, args.format)

if __name__ == "__main__":
    main()