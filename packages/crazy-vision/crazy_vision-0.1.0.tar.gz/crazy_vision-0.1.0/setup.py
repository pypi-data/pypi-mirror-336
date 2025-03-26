from setuptools import setup, find_packages
import os

# Read the long description from README.md if available
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="crazy-vision",
    version="0.1.0",
    description="A video decoding and model inference package using YOLO, OpenCV, and PyTorch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",  # Change to your name
    author_email="your.email@example.com",  # Change to your email
    url="https://github.com/yourusername/crazy-vision",  # Update with your repo URL
    packages=find_packages(),  # This will include crazy_vision and any subpackages
    install_requires=[
        "av",
        "opencv-python",
        "torch",
        "numpy",
        "requests",
        "ultralytics",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Make sure your LICENSE file is consistent
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
