# FFMPEG_Filters

A simple Python library to generate videos with smooth motion effects (Zoom, Scroll, etc.) from a single image using FFMPEG.

## Installation

Install the package directly from PyPI:

```bash
pip install FFMPEG-Filters



## Usage
```
from FFMPEG_Filters.Image import options

video = options()

# Set the export parameters
video.setExportParameters(
    imagePath=r"C:\Users\Tgthegood\Pictures\Overlord\Tg_0.jpg",      # Input image
    pathExport=r"C:\Users\Tgthegood\Documents\Novels\Example.mp4",   # Output video path
    exportResolution=(1280, 720),  # Video resolution (e.g. YouTube = 1280x720)
    exportFfps=30,                 # Frames per second
    duration=10,                   # Duration in seconds
    scale=2                        # Image upscaling for smoother filters (1-2 recommended)
)

# Apply filters (choose any combination, except contradicting ones like zoomIn and zoomOut)
video.zoomIn()
video.scrollTop()

# Generate the video
video.makeVideo()
```

# Available Filters
You can apply any combination of these filters:
zoomIn()
zoomOut()
scrollTop()
scrollBottom()

Do not apply contradictory filters (e.g. zoomIn() and zoomOut() together).


# Requirements
Python 3.7+
FFMPEG must be installed and available in your PATH.

# License
MIT License
