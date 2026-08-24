import argparse
import sys
import os
from rossini.core.pipeline import RossiniPipeline
from rossini.core.memory import MemoryManager
from rossini.core.image_engine import RossiniImageEngine

def main():
    parser = argparse.ArgumentParser(
        description="Rossini GenAI — Next-Gen Audio-Visual AI Generation Pipeline"
    )
    
    # Parâmetros principais
    parser.add_argument("--prompt", "-p", type=str, required=True, help="Prompt describing scene, style or audio.")
    parser.add_argument("--input", "-i", type=str, default="", help="Path to input source video (required for video processing).")
    parser.add_argument("--output", "-o", type=str, default="outputs/rossini_output.mp4", help="Output file path.")
    
    # Tipo de mídia e formatos adicionais (Integração Grand Theatre)
    parser.add_argument("--type", "-t", choices=["video", "image", "gif"], default="video", help="Output media type.")
    parser.add_argument("--format", choices=["png", "jpg", "jpeg"], default="png", help="Static image export format.")
    parser.add_argument("--mode", type=str, default="wallpaper", choices=["banner", "video_cover", "wallpaper", "cd_cover", "photo_album", "business_card"], help="Canvas resolution preset for images.")
    parser.add_argument("--bg", type=str, default="wine", choices=["white", "golden", "olive", "wine", "clean"], help="Semantic background color for images.")
    parser.add_argument("--pos", type=str, default="right", choices=["right", "left", "top", "bottom"], help="Main subject position for images.")
    
    # Parâmetros de infraestrutura
    parser.add_argument("--model", "-m", type=str, default="llama3:latest", help="Ollama model name.")
    parser.add_argument("--ollama-url", type=str, default="http://localhost:11434", help="Ollama API URL.")
    parser.add_argument("--unload-vram", action="store_true", help="Unload Ollama model from VRAM after processing.")

    args = parser.parse_args()

    print("\n==========================================")
    print("      ROSSINI GENAI MULTIMODAL PIPELINE    ")
    print("==========================================\n")

    try:
        # GERAÇÃO DE IMAGEM (Grand Theatre)
        if args.type == "image":
            print(f"[*] Generating {args.format.upper()} image via Grand Theatre Engine...")
            RossiniImageEngine.generate_image(
                prompt=args.prompt,
                output_path=args.output,
                mode=args.mode,
                bg_name=args.bg,
                pos=args.pos,
                export_format=args.format
            )

        # GERAÇÃO DE GIF ANIMADO
        elif args.type == "gif":
            print("[*] Generating base video sequence for GIF conversion...")
            temp_video = "outputs/temp_gif_source.mp4"
            pipeline = RossiniPipeline(model_name=args.model, ollama_url=args.ollama_url)
            pipeline.run(
                input_video_path=args.input,
                user_prompt=args.prompt,
                output_path=temp_video
            )
            print("[*] Converting video sequence to animated GIF...")
            RossiniImageEngine.create_gif_from_video(temp_video, args.output)
            
            if os.path.exists(temp_video):
                os.remove(temp_video)

        # GERAÇÃO DE VÍDEO (MP4 Padrão)
        else:
            if not args.input:
                print("[WARNING] No input video provided (--input). Running text-to-video generation mode.")
            
            pipeline = RossiniPipeline(model_name=args.model, ollama_url=args.ollama_url)
            pipeline.run(
                input_video_path=args.input,
                user_prompt=args.prompt,
                output_path=args.output
            )

        # Liberar VRAM do Ollama se solicitado
        if args.unload_vram and args.type in ["video", "gif"]:
            MemoryManager.unload_ollama_model(model_name=args.model, ollama_url=args.ollama_url)

        print("\n[SUCCESS] Pipeline execution finished.")

    except Exception as e:
        print(f"\n[FATAL ERROR] Pipeline failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()