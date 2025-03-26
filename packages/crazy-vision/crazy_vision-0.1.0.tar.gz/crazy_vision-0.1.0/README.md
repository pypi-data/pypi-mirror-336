# crazy-vision

A video decoding and model inference package that utilizes YOLO, OpenCV, and PyTorch. The package provides classes for GPU/CPU video decoding, frame processing (including resizing and letterboxing), and model inference using YOLO with convenient API wrappers.

## Features

- **Video Decoding:** Supports GPU decoding (NVDEC/CUVID) with a CPU fallback.
- **Frame Processing:** Resize and pad frames while preserving aspect ratio.
- **Model Inference:** Object tracking with YOLO, including batch processing.
- **Easy Integration:** Designed to be modular and extendable.

## Installation

```bash
pip install crazy-vision
