import os
import torch
import torchvision.models as models
from ultralytics import YOLO

# Ensure temporary writable directories for PyTorch and Ultralytics
os.environ.setdefault('TORCH_HOME', '/tmp/torch')
os.environ.setdefault('YOLO_CONFIG_DIR', '/tmp/Ultralytics')

_yolo_model = None
_gender_model = None
_holistic_model = None
_mp_holistic = None

def get_mp_holistic():
    """Robust getter for MediaPipe holistic solution module (handles all versions)"""
    global _mp_holistic
    if _mp_holistic is None:
        try:
            from mediapipe.python.solutions import holistic
            _mp_holistic = holistic
        except Exception:
            try:
                import mediapipe as mp
                _mp_holistic = mp.solutions.holistic
            except Exception:
                import mediapipe.python.solutions as solutions
                _mp_holistic = solutions.holistic
    return _mp_holistic

def get_yolo_model():
    """Singleton lazy loader for YOLOv8 model"""
    global _yolo_model
    if _yolo_model is None:
        model_path = os.path.join(os.path.dirname(__file__), "yolov8n.pt")
        print(f"[ModelManager] Loading shared YOLOv8 from {model_path}...")
        _yolo_model = YOLO(model_path)
    return _yolo_model

def get_gender_model():
    """Singleton lazy loader for MobileNetV2 gender model"""
    global _gender_model
    if _gender_model is None:
        print("[ModelManager] Loading shared MobileNetV2...")
        try:
            _gender_model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)
        except Exception:
            _gender_model = models.mobilenet_v2(pretrained=True)
        _gender_model.eval()
    return _gender_model

def get_holistic_model():
    """Singleton lazy loader for MediaPipe Holistic model"""
    global _holistic_model
    if _holistic_model is None:
        print("[ModelManager] Loading shared MediaPipe Holistic...")
        mp_h = get_mp_holistic()
        _holistic_model = mp_h.Holistic(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            model_complexity=1
        )
    return _holistic_model
