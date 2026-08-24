import requests
import gc

class MemoryManager:
    @staticmethod
    def unload_ollama_model(model_name: str, ollama_url: str = "http://localhost:11434"):
        """Forces Ollama to eject the model from VRAM by setting keep_alive to 0."""
        try:
            payload = {"model": model_name, "keep_alive": 0}
            requests.post(f"{ollama_url}/api/generate", json=payload, timeout=5)
            print(f"[MemoryManager] Ejected {model_name} from VRAM.")
        except Exception as e:
            print(f"[MemoryManager] Warning: Could not auto-eject model: {e}")

    @staticmethod
    def clear_cuda_cache():
        """Cleans PyTorch CUDA cache and forces Python garbage collection."""
        try:
            import torch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                torch.cuda.ipc_collect()
            gc.collect()
            print("[MemoryManager] PyTorch CUDA cache cleared.")
        except ImportError:
            pass