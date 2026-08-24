
```markdown
# Rossini GenAI — Multimodal AI Framework

> **Next-Generation Audio-Visual AI Orchestrator Powered by DiT, RADCAM, RADGRAM, Grand Theatre & Local LLMs**

Rossini GenAI is an enterprise-grade multimodal orchestration framework designed for generative media production. It bridges local Large Language Models (via Ollama) with state-of-the-art synthetic generation motors (**DiT / Diffusion Transformers**), vision compositing (**RADCAM**), audio synthesis engines (**RADGRAM**), high-end graphic design tools (**Grand Theatre**), and dynamic Retrieval-Augmented Generation (**RAG**).

Maintained by: **#asytric** (`eusmool@gmail.com`).

---

## 📁 Repository Directory Structure

```text
rossini/
├── config/             # Global configuration files and default parameters
├── core/               # Core orchestration & execution modules
│   ├── __init__.py
│   ├── orchestrator.py  # Ollama LLM integration & prompt parsing
│   ├── pipeline.py      # Master execution pipeline
│   ├── image_engine.py  # Grand Theatre integration (PNG, JPEG & GIF export)
│   ├── schemas.py       # Pydantic JSON schema guardrails
│   ├── timeline.py      # A/V sync and beat-reactivity engine (BPM)
│   ├── memory.py        # VRAM management & model unloading
│   └── fallback.py      # Fallback scene generator for error recovery
├── dit/                # Diffusion Transformer Engine
│   ├── __init__.py
│   └── dit_engine.py    # Sora-level synthetic video generation engine
├── models/             # Local Modelfiles and quantized GGUF weights
├── rag/                # Retrieval-Augmented Generation
│   ├── __init__.py
│   ├── normalizer.py    # Frame rate, resolution, and Alpha channel normalizer
│   ├── cache.py         # MD5-hash asset caching system
│   ├── vector_store.py  # Local vector database engine (FAISS)
│   └── online_search.py # Web search engine for video overlays & loops
├── .gitignore          # Git ignore rules for cached assets & binaries
├── __init__.py         # Python package entrypoint
├── cli.py              # Command Line Interface (CLI)
├── Dockerfile          # CUDA-enabled Docker container specification
├── README.md           # Documentation & user manual
├── requirements.txt    # Python dependencies list
└── setup.py            # Editable package installation script (`pip install -e .`)

```

---

## ⚡ Setup & Installation

### Prerequisites

* **Python**: 3.10+
* **CUDA**: 11.8 / 12.1+ (NVIDIA GPU required)
* **FFmpeg**: System binary installed and added to system `PATH`
* **Ollama**: Installed and running locally (`http://localhost:11434`)

### 1. Ollama Setup & Model Pulling

Ensure Ollama is running and download your preferred orchestration LLM (e.g., `llama3` or `mistral`):

```bash
# Start Ollama service (if not running as a daemon)
ollama serve

# Pull the default LLM model used by Rossini
ollama pull llama3:latest

```

### 2. Environment Installation

```bash
# Clone the repository
git clone [https://github.com/asytric/rossini-genai.git](https://github.com/asytric/rossini-genai.git)
cd rossini

# Create and activate virtual environment
python -m venv venv
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies and local package
pip install -r requirements.txt
pip install -e .

```

---

## 📖 User Manual & CLI Examples

### 1. Beat-Reactive Video Processing (MP4)

Processes a source video by synchronizing visual FX and overlays to the audio rhythm via local Ollama planning:

```bash
python -m rossini.cli \
    --input "assets/input.mp4" \
    --prompt "Cyberpunk rain with fast synthwave beat" \
    --model "llama3:latest" \
    --output "outputs/cyberpunk.mp4"

```

### 2. Synthetic Generation via DiT (Diffusion Transformer)

Generates synthetic video sequences directly from text prompts using the `dit` module:

```bash
python -m rossini.cli \
    --prompt "A cinematic futuristic robot driving through neon desert" \
    --output "outputs/dit_render.mp4"

```

### 3. Graphic Design & Covers (PNG / JPEG via Grand Theatre)

Generates formatted promotional banners, video covers, and high-res static layouts:

```bash
python -m rossini.cli \
    --type image \
    --prompt "an elegant woman inside a historic theatre" \
    --mode video_cover \
    --format png \
    --bg wine \
    --pos right \
    --output "outputs/theatre_cover.png"

```

### 4. Animated GIF Generation

Creates lightweight animated GIF loops:

```bash
python -m rossini.cli \
    --type gif \
    --prompt "subtle cinematic smoke and flickering golden lights" \
    --output "outputs/animation.gif"

```

### 5. High-Performance VRAM Auto-Unload

Unloads the Ollama model from VRAM immediately after scene planning, freeing 100% of GPU memory for heavy CUDA rendering tasks (DiT and RADCAM):

```bash
python -m rossini.cli \
    --prompt "Deep space nebula floating with ambient audio" \
    --model "llama3:latest" \
    --unload-vram \
    --output "outputs/space.mp4"

```

---

## 🌐 API Integration Example (FastAPI + Ollama)

You can serve Rossini GenAI as a production web API endpoint using FastAPI. Create a file named `app.py` in your root folder:

```python
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
import uvicorn

from rossini.core.pipeline import RossiniPipeline
from rossini.core.image_engine import RossiniImageEngine
from rossini.core.memory import MemoryManager

app = FastAPI(
    title="Rossini GenAI API Engine",
    description="REST API interface for multimodal generation powered by local Ollama & Grand Theatre.",
    version="2.0.0"
)

class RenderRequest(BaseModel):
    prompt: str
    type: str = "video"  # Options: "video", "image", "gif"
    input_video: str = ""
    output_path: str = "outputs/api_render.mp4"
    model: str = "llama3:latest"
    unload_vram: bool = True

def run_async_generation(req: RenderRequest):
    try:
        if req.type == "image":
            RossiniImageEngine.generate_image(
                prompt=req.prompt,
                output_path=req.output_path,
                export_format="PNG"
            )
        else:
            pipeline = RossiniPipeline(model_name=req.model)
            pipeline.run(
                input_video_path=req.input_video,
                user_prompt=req.prompt,
                output_path=req.output_path
            )
            if req.unload_vram:
                MemoryManager.unload_ollama_model(model_name=req.model)
    except Exception as e:
        print(f"[API Error] Generation failed: {e}")

@app.post("/api/v1/generate")
async def generate_media(request: RenderRequest, background_tasks: BackgroundTasks):
    """
    Triggers an asynchronous multimodal generation job.
    """
    background_tasks.add_task(run_async_generation, request)
    return {
        "status": "queued",
        "message": f"Task queued successfully for media type '{request.type}'.",
        "target_output": request.output_path
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

```

### Launching the API Service

```bash
# Install uvicorn if needed
pip install uvicorn

# Start the Web API Server
python app.py

```

Send a request using `curl`:

```bash
curl -X POST "http://localhost:8000/api/v1/generate" \
     -H "Content-Type: application/json" \
     -d '{
       "prompt": "Futuristic neon cyberpunk city",
       "type": "video",
       "model": "llama3:latest",
       "unload_vram": true,
       "output_path": "outputs/neon_city.mp4"
     }'

```

---

## 📄 License & Support

* **Author**: **#asytric**
* **Contact**: `eusmool@gmail.com`
* **License**: MIT License

```

```
