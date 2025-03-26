from ultralytics import YOLO
import os
import requests

DEFAULT_MODEL_URL = "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11n.pt"
DEFAULT_MODEL_PATH = os.path.join(os.path.expanduser("~"), ".weights", "yolo11n.pt")

def download_weights(model_path=DEFAULT_MODEL_PATH, url=DEFAULT_MODEL_URL):
    """Download the YOLO model weights if not already present."""
    os.makedirs(os.path.dirname(model_path), exist_ok=True)

    if not os.path.exists(model_path):
        print(f"Downloading YOLO model to {model_path}...")
        response = requests.get(url, stream=True)
        with open(model_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        print("Download complete.")
    
    return model_path

class ModelInference:
    def __init__(self, model_path=None):
        model_path = model_path or download_weights()
        self.model = YOLO(model_path)  # Auto-detects device
        self.class_names = self.model.names if hasattr(self.model, "names") else {}
        self.class_indices = list(self.class_names.keys()) if isinstance(self.class_names, dict) else []

    def track_frame(self, frame, conf=0.5, classes=None, tracker="bytetrack.yaml", persist=True):
        """Track objects in a single frame."""
        classes = classes if classes is not None else self.class_indices  # Default: all classes
        return self.model.track(frame, persist=persist, conf=conf, classes=classes, tracker=tracker)

    def track_batch(self, frames, conf=0.5, classes=None, tracker="bytetrack.yaml", persist=True):
        """Track objects in a batch of frames for faster inference."""
        classes = classes if classes is not None else self.class_indices  # Default: all classes
        return self.model.track(frames, persist=persist, conf=conf, classes=classes, tracker=tracker)
