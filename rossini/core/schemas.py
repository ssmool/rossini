from pydantic import BaseModel, Field, field_validator
from typing import Optional

class RossiniExecutionPlan(BaseModel):
    visual_prompt: str = Field(..., description="Prompt for asset search and DiT rendering")
    audio_genre: str = Field(..., description="Music genre targeted for RADGRAM audio synthesis")
    tempo_bpm: int = Field(default=120, description="Music track tempo in BPM")
    fx_style: str = Field(default="hollywood", description="Visual post-processing style filter")
    vertical_format: bool = Field(default=False, description="Crop to 9:16 aspect ratio for vertical video")
    reactivity_level: float = Field(default=0.5, description="Intensity of visual response to audio dynamics (0.0 to 1.0)")
    use_dit_generation: bool = Field(default=True, description="Enable Diffusion Transformer for synthetic generation")

    @field_validator("tempo_bpm")
    @classmethod
    def validate_bpm(cls, v: int) -> int:
        return max(60, min(v, 180))

    @field_validator("reactivity_level")
    @classmethod
    def validate_reactivity(cls, v: float) -> float:
        return max(0.0, min(v, 1.0))