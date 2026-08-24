Here is the updated `README.md` strictly aligned with your actual directory structure shown in the screenshot (removing Flux completely and anchoring to **Ollama**, **RADCAM**, and **RADGRAM**).

---

```markdown
# Rossini GenAI — Multimodal AI Framework

> **Next-Generation Audio-Visual AI Orchestrator Powered by RADCAM, RADGRAM & Local LLMs**

Rossini GenAI is an enterprise-grade multimodal orchestration framework designed for generative media production. It bridges local Large Language Models (via Ollama) with state-of-the-art vision compositing (**RADCAM**), audio synthesis engines (**RADGRAM**), and dynamic Retrieval-Augmented Generation (**RAG**).

Whether you are compositing real-time video streams, executing background matting, or synchronizing audio-reactive video effects to synthesized music tracks, Rossini GenAI delivers a unified, memory-efficient Python pipeline.

Created by **#asytric** (`eusmool@gmail.com`).

---

## Technical Features & Core Capabilities

* **Local LLM Orchestration**: Direct inference through Ollama with automatic JSON output validation using Pydantic schema guardrails.
* **Beat-Reactive Video Processing**: Automatic audio amplitude extraction and BPM beat-mapping for real-time visual FX modulation in RADCAM.
* **Dynamic Online & Offline RAG**: Hybrid search engine querying local FAISS vector stores or live web endpoints for alpha-channel overlays and MP4 video loops.
* **VRAM Memory Optimization**: Intelligent model ejector (`MemoryManager`) that unloads Ollama LLMs from VRAM before spawning heavy CUDA rendering tasks.
* **Asset Normalization Layer**: Automatic resolution, framerate, and alpha-channel standardization across heterogeneous media inputs.

---

## Directory Architecture

This structure matches the native `rossini` package layout:

```text
rossini/
├── config/             # Environment setup and default pipeline parameters
├── core/
│   ├── __init__.py
│   ├── orchestrator.py  # Ollama LLM integration & prompt parsing
│   ├── pipeline.py      # Master execution pipeline
│   ├── schemas.py       # Pydantic JSON guardrails
│   ├── timeline.py      # A/V sync, BPM, and reactivity engine
│   ├── memory.py        # VRAM unload and resource manager
│   └── fallback.py      # Error recovery & default scene generator
├── models/             # Custom Modelfiles and quantized GGUF weights
├── rag/
│   ├── __init__.py
│   ├── normalizer.py    # Frame and resolution standardization
│   ├── cache.py         # MD5 hash-based asset caching
│   ├── vector_store.py  # Local vector database engine
│   └── online_search.py # Web search engine for video loops
├── __init__.py         # Package entrypoint
├── cli.py              # Command Line Interface
└── README.md           # Documentation

```

---

## Prerequisites & Installation

### System Requirements

* **OS**: Windows / Linux / macOS
* **Python**: 3.10+
* **CUDA**: 11.8 / 12.1+ (For GPU acceleration)
* **FFmpeg**: System binary installed and added to `PATH`
* **Ollama**: Running locally on `http://localhost:11434`

### Installation

```bash
# Clone repository
git clone [https://github.com/asytric/rossini-genai.git](https://github.com/asytric/rossini-genai.git)
cd rossini

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

```

---

## Quickstart CLI Commands

### 1. Basic Multimodal Rendering

Run a full generation pipeline passing a raw input video and natural language prompt:

```bash
python -m rossini.cli \
    --input "assets/input_speaker.mp4" \
    --prompt "Cyberpunk city rain with heavy fast synthwave music" \
    --output "outputs/cyberpunk_render.mp4"

```

### 2. High-Performance GPU Mode (Auto-Unload VRAM)

Unload Ollama from GPU VRAM before launching RADCAM rendering pipelines:

```bash
python -m rossini.cli \
    --input "assets/input_speaker.mp4" \
    --prompt "Futuristic space station nebula float" \
    --model "llama3:latest" \
    --unload-vram \
    --output "outputs/space_render.mp4"

```

---

## Python API Usage

### 1. Running the Full Rossini Multimodal Pipeline

Programmatically control the full pipeline in Python:

```python
from rossini.core.pipeline import RossiniPipeline
from rossini.core.memory import MemoryManager

# Initialize Pipeline with local Ollama
pipeline = RossiniPipeline(
    model_name="llama3:latest",
    ollama_url="http://localhost:11434"
)

# Run full multimodal transformation
pipeline.run(
    input_video_path="raw_speaker.mp4",
    user_prompt="Vertical TikTok video with neon cyberpunk rain and fast synthwave music",
    output_path="outputs/final_short.mp4"
)

# Free up VRAM after generation
MemoryManager.unload_ollama_model(model_name="llama3:latest")

```

### 2. Direct LLM Planning & Validation

Use the LLM Orchestrator to parse natural language into structured execution parameters:

```python
from rossini.core.orchestrator import RossiniEngine

orchestrator = RossiniEngine(model_name="llama3:latest")

# Generate JSON plan validated via Pydantic
execution_plan = orchestrator.plan_generation(
    user_prompt="Astronaut in deep space with ambient lo-fi music"
)

print(execution_plan)

```

---

## REST API Integration (FastAPI Endpoint)

Deploy Rossini GenAI as a microservice endpoint for production backends:

```python
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from rossini.core.pipeline import RossiniPipeline

app = FastAPI(title="Rossini GenAI API Engine", version="1.0.0")

class GenerationRequest(BaseModel):
    input_video_path: str
    prompt: str
    output_path: str
    model_name: str = "llama3:latest"

def process_video_task(request: GenerationRequest):
    pipeline = RossiniPipeline(model_name=request.model_name)
    pipeline.run(
        input_video_path=request.input_video_path,
        user_prompt=request.prompt,
        output_path=request.output_path
    )

@app.post("/api/v1/generate")
async def generate_media(request: GenerationRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_video_task, request)
    return {
        "status": "processing",
        "message": "Video processing task queued successfully.",
        "target_output": request.output_path
    }

```

---

## License & Support

* **Maintainer**: **#asytric**
* **Contact**: `eusmool@gmail.com`
* **License**: MIT License

```

```