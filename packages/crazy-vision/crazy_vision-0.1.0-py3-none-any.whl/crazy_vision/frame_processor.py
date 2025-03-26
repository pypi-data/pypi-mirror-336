import cv2
import numpy as np

class FrameProcessor:
    def __init__(self, target_width=640, target_height=640, letterbox=True, batch_size=1):
        self.target_width = target_width
        self.target_height = target_height
        self.letterbox = letterbox
        self.batch_size = batch_size  # Controls batch processing

    def _process_single_frame(self, frame):
        """Resize and pad a single frame while maintaining aspect ratio."""
        original_h, original_w = frame.shape[:2]

        # Early exit if frame is already at target size
        if original_w == self.target_width and original_h == self.target_height:
            return frame, 1.0, 0, 0

        if not self.letterbox:
            # Direct resize without maintaining aspect ratio
            resized = cv2.resize(frame, (self.target_width, self.target_height), interpolation=cv2.INTER_AREA)
            return resized, 1.0, 0, 0

        # Compute scaling factor
        scale = min(self.target_width / original_w, self.target_height / original_h)
        new_w, new_h = int(original_w * scale), int(original_h * scale)
        resized = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA)

        # Compute padding
        pad_w_total = self.target_width - new_w
        pad_h_total = self.target_height - new_h
        left = pad_w_total // 2
        right = pad_w_total - left
        top = pad_h_total // 2
        bottom = pad_h_total - top

        # Apply padding
        padded = cv2.copyMakeBorder(resized, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(0, 0, 0))
        return padded, scale, left, top

    def process_frames(self, frames):
        """Process a batch of frames or a single frame depending on batch size."""
        if isinstance(frames, list):  # Batch processing
            processed_frames = []
            scales = []
            pad_ws = []
            pad_hs = []

            for frame in frames:
                processed, scale, pad_w, pad_h = self._process_single_frame(frame)
                processed_frames.append(processed)
                scales.append(scale)
                pad_ws.append(pad_w)
                pad_hs.append(pad_h)

            return processed_frames, scales, pad_ws, pad_hs  # Return as separate lists

        else:  # Single frame processing
            processed, scale, pad_w, pad_h = self._process_single_frame(frames)
            return [processed], [scale], [pad_w], [pad_h]  # Return as lists for consistency
