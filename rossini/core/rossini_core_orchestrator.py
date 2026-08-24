import json
import requests
from typing import Dict, Any
from rossini.core.schemas import RossiniExecutionPlan

class RossiniEngine:
    def __init__(self, model_name: str = "llama3:latest", ollama_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.ollama_url = f"{ollama_url}/api/generate"

    def plan_generation(self, user_prompt: str) -> Dict[str, Any]:
        """Queries local Ollama instance and enforces structured JSON output matching schema."""
        system_prompt = (
            "You are Rossini GenAI Orchestrator. Convert user requests into a valid JSON "
            "matching the following exact schema keys: "
            "'visual_prompt' (str), 'audio_genre' (str), 'tempo_bpm' (int 60-180), "
            "'fx_style' (str), 'vertical_format' (bool), 'reactivity_level' (float 0.0-1.0), "
            "'use_dit_generation' (bool)."
        )
        
        payload = {
            "model": self.model_name,
            "prompt": f"{system_prompt}\nUser Request: {user_prompt}",
            "format": "json",
            "stream": False,
            "options": {
                "temperature": 0.2
            }
        }

        try:
            response = requests.post(self.ollama_url, json=payload, timeout=30)
            response.raise_for_status()
            response_data = response.json()
            
            raw_json = json.loads(response_data.get("response", "{}"))
            validated_plan = RossiniExecutionPlan(**raw_json)
            return validated_plan.model_dump()

        except Exception as e:
            print(f"[Ollama Error] Connection or parsing failed: {e}. Falling back to default plan.")
            return RossiniExecutionPlan(
                visual_prompt=user_prompt,
                audio_genre="synthwave",
                tempo_bpm=120,
                use_dit_generation=True
            ).model_dump()
