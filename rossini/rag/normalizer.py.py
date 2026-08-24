import cv2
import numpy as np

class AssetNormalizer:
    def __init__(self, target_resolution=(1920, 1080), target_fps=30.0):
        self.target_w, self.target_h = target_resolution
        self.target_fps = target_fps

    def normalize_image(self, image_path: str, require_alpha: bool = False) -> np.ndarray:
        """Loads and resizes image assets while preserving or adding alpha channels."""
        read_flag = cv2.IMREAD_UNCHANGED if require_alpha else cv2.IMREAD_COLOR
        img = cv2.imread(image_path, read_flag)
        
        if img is None:
            raise FileNotFoundError(f"Asset not found at path: {image_path}")

        return cv2.resize(img, (self.target_w, self.target_h), interpolation=cv2.INTER_AREA)

    def normalize_video_frame(self, frame: np.ndarray) -> np.ndarray:
        """Resizes incoming real-time video frames to match project dimensions."""
        h, w = frame.shape[:2]
        if (w, h) != (self.target_w, self.target_h):
            return cv2.resize(frame, (self.target_w, self.target_h), interpolation=cv2.INTER_LINEAR)
        return frame