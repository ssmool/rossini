"""
Rossini GenAI — Multimodal Video, Audio, and Image AI Generation Framework.
"""

__version__ = "1.0.0"
__author__ = "#asytric"

from rossini_genai.core.pipeline import RossiniPipeline
from rossini_genai.core.orchestrator import RossiniEngine

__all__ = ["RossiniPipeline", "RossiniEngine"]