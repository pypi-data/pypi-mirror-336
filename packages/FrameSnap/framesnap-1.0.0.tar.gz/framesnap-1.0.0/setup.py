from setuptools import setup, find_packages

setup(
    name="FrameSnap",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "opencv-python",
    ],
    entry_points={
        "console_scripts": [
            "extract-frames=video_frame_extractor.cli:main",
        ],
    },
    author="Darshil",
    author_email="darshilmahraur67@gmail.com", 
    description="A Python library to extract frames from videos and save them as images.",
    url="https://github.com/darshil89/FrameSnap",
    python_requires=">=3.6",  # ✅ Minimum Python version
)
