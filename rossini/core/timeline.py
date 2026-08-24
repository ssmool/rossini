import numpy as np
from typing import List

class TimelineEngine:
    def __init__(self, fps: float = 30.0):
        self.fps = fps

    def generate_beat_map(self, duration_sec: float, bpm: int) -> List[bool]:
        """Returns a boolean list indicating target beat frames."""
        total_frames = int(duration_sec * self.fps)
        frames_per_beat = (60.0 / bpm) * self.fps
        
        beat_map = [False] * total_frames
        current_frame = 0.0
        
        while int(current_frame) < total_frames:
            beat_map[int(current_frame)] = True
            current_frame += frames_per_beat
            
        return beat_map

    def calculate_audio_reactivity(self, audio_signal: np.ndarray, total_frames: int) -> np.ndarray:
        """Extracts normalized amplitude envelope per frame for reactive FX processing."""
        if total_frames <= 0:
            return np.array([0.5])
            
        samples_per_frame = max(1, len(audio_signal) // total_frames)
        reactivity_curve = []

        for i in range(total_frames):
            chunk = audio_signal[i * samples_per_frame : (i + 1) * samples_per_frame]
            amplitude = np.max(np.abs(chunk)) if len(chunk) > 0 else 0.0
            reactivity_curve.append(amplitude)

        max_amp = np.max(reactivity_curve) if np.max(reactivity_curve) > 0 else 1.0
        return np.array(reactivity_curve) / max_amp