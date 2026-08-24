import cv2
import numpy as np

class FallbackEngine:
    @staticmethod
    def get_default_background(resolution=(1920, 1080)) -> np.ndarray:
        """Generates a dark motion gradient if RAG search fails completely."""
        h, w = resolution
        gradient = np.zeros((h, w, 3), dtype=np.uint8)
        gradient[:, :] = [30, 15, 10]  # Dark cybernetic ambient tone
        return gradient

    @staticmethod
    def safe_read_frame(cap: cv2.VideoCapture, default_resolution=(1920, 1080)):
        """Safely reads a frame, returning a black placeholder if read fails."""
        ret, frame = cap.read()
        if not ret or frame is None:
            return False, np.zeros((default_resolution[1], default_resolution[0], 3), dtype=np.uint8)
        return True, frame