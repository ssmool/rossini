import os
import cv2
import numpy as np
import soundfile as sf
import subprocess

from rossini.core.orchestrator import RossiniEngine
from rossini.core.schemas import RossiniExecutionPlan
from rossini.core.timeline import TimelineEngine
from rossini.core.memory import MemoryManager
from rossini.rag.normalizer import AssetNormalizer
from rossini.dit.dit_engine import VideoDiTEngine

class RossiniPipeline:
    def __init__(self, model_name: str = "llama3:latest", ollama_url: str = "http://localhost:11434"):
        self.orchestrator = RossiniEngine(model_name=model_name, ollama_url=ollama_url)
        self.timeline = TimelineEngine(fps=30.0)
        self.normalizer = AssetNormalizer(target_resolution=(1920, 1080))
        self.dit = VideoDiTEngine()

    def run(self, input_video_path: str, user_prompt: str, output_path: str):
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

        # 1. LLM Planning & Validation
        print("[Rossini] Querying LLM Orchestrator...")
        raw_plan = self.orchestrator.plan_generation(user_prompt)
        plan = RossiniExecutionPlan(**raw_plan)
        print(f"[Rossini] Executing Execution Plan:\n{plan.model_dump_json(indent=2)}")

        # 2. Synthetic DiT or Input Processing
        dit_video_path = "temp_dit_bg.mp4"
        if plan.use_dit_generation:
            print("[Rossini] Spawning Diffusion Transformer (DiT) Video Generation...")
            self.dit.generate_video(
                prompt=plan.visual_prompt,
                output_path=dit_video_path,
                num_frames=150,
                fps=30
            )

        # 3. Audio Synthesis Simulation (RADGRAM Integration)
        audio_data = np.random.uniform(-0.5, 0.5, 44100 * 5)  # 5s simulated audio
        sample_rate = 44100
        temp_audio_path = "temp_audio.wav"
        sf.write(temp_audio_path, audio_data, sample_rate)

        # 4. Processing Video Frames & Audio Reactivity
        video_src = dit_video_path if plan.use_dit_generation and os.path.exists(dit_video_path) else input_video_path
        cap = cv2.VideoCapture(video_src)
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if total_frames <= 0:
            total_frames = 150

        reactivity_curve = self.timeline.calculate_audio_reactivity(audio_data, total_frames)
        beat_map = self.timeline.generate_beat_map(duration_sec=total_frames / 30.0, bpm=plan.tempo_bpm)

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        temp_video_path = "temp_processed_video.mp4"
        out = cv2.VideoWriter(temp_video_path, fourcc, 30.0, (1920, 1080))

        frame_idx = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret or frame_idx >= total_frames:
                break

            norm_frame = self.normalizer.normalize_video_frame(frame)
            reactivity = reactivity_curve[frame_idx] * plan.reactivity_level if frame_idx < len(reactivity_curve) else 0.5
            is_beat = beat_map[frame_idx] if frame_idx < len(beat_map) else False

            # Beat-reactive visual pulse modulation
            if is_beat:
                norm_frame = cv2.addWeighted(norm_frame, 1.2, norm_frame, 0, 15)

            out.write(norm_frame)
            frame_idx += 1

        cap.release()
        out.release()

        # 5. Final Audio/Video Multiplexing
        self._multiplex(temp_video_path, temp_audio_path, output_path)

        # Clean temporary files
        for tmp in [temp_video_path, temp_audio_path, dit_video_path]:
            if os.path.exists(tmp):
                try:
                    os.remove(tmp)
                except Exception:
                    pass

    def _multiplex(self, video_p: str, audio_p: str, output_p: str):
        cmd = ["ffmpeg", "-y", "-i", video_p, "-i", audio_p, "-c:v", "copy", "-c:a", "aac", "-shortest", output_p]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"[Rossini] Rendered output saved to: {output_p}")