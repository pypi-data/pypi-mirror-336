import av
import cv2
import torch
import numpy as np
import subprocess
from queue import Queue
from threading import Thread


class VideoDecoder:
    def __init__(self, source, use_gpu=True):
        self.source = source
        self.use_gpu_flag = use_gpu
        self.use_gpu = None
        self.decoder = None
        self.frame_queue = Queue(maxsize=10)  # Pre-buffer frames
        self.running = True

        if self.use_gpu_flag:
            self.use_gpu = self._check_gpu_availability()

        self._initialize_decoder()
        self.thread = Thread(target=self._frame_reader, daemon=True) # read frame seperate thread
        self.thread.start()

    def _check_gpu_availability(self):
        """Check if CUDA and NVDEC are available for hardware acceleration."""
        if not torch.cuda.is_available():
            return None
        if torch.cuda.is_available():
            try:
                result = subprocess.run(
                    ["ffmpeg", "-decoders"],
                    capture_output=True,
                    text=True,
                )
                if "h264_nvdec" in result.stdout:
                    print("Using GPU NVDEC for decoding.")
                    return "nvdec"
                elif "h264_cuvid" in result.stdout:
                    print("Using GPU CUVID for decoding.")
                    return "cuda"
            except Exception:
                pass

        print("Using CPU FFmpeg for decoding.")
        return None

    def _initialize_decoder(self):
        """Initialize the video decoder with NVDEC, CUDA, or CPU fallback."""
        if self.use_gpu:
            print("Initializing GPU decoding...")
            self.decoder = av.open(
                self.source,
                options={
                    "hwaccel": self.use_gpu,
                    "flags": "low_delay",
                    "fflags": "nobuffer",
                    "rtsp_transport": "tcp"
                }
            )
        else:
            print("Initializing CPU decoding...")
            self.decoder = cv2.VideoCapture(self.source, cv2.CAP_FFMPEG)
            self.decoder.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce buffer lag

    def _frame_reader(self):
        """Continuously reads frames and stores them in a queue for smooth playback."""
        if self.use_gpu:
            stream = next((s for s in self.decoder.streams if s.type == "video"), None)
            if stream is None:
                raise RuntimeError("No video stream found!")

            for frame in self.decoder.decode(stream):
                if not self.running:
                    break
                img = frame.to_ndarray(format="bgr24")
                if img is None:
                    print("Warning: Received an empty frame!")
                    continue
                if not self.frame_queue.full():
                    self.frame_queue.put(img)

        else:
            while self.running and self.decoder.isOpened():
                ret, frame = self.decoder.read()
                if not ret or frame is None:
                    print("Warning: Frame not read successfully.")
                    continue
                if not self.frame_queue.full():
                    self.frame_queue.put(frame)

    def get_frames(self):
        """Generator function to yield video frames smoothly."""
        # while self.running:
        #     if not self.frame_queue.empty():
        #         yield self.frame_queue.get()

        while self.running:
            try:
                yield self.frame_queue.get(timeout=1)  # Avoid indefinite waiting
            except:
                pass

    def close(self):
        """Stops decoding and releases resources."""
        self.running = False
        self.thread.join()
        if self.use_gpu:
            self.decoder.close()
        else:
            self.decoder.release()