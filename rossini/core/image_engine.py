import os
import cv2
from PIL import Image
from typing import Optional, List
from grandtheatre.editor import generate_composition

class RossiniImageEngine:
    """
    Motor de geração de mídia estática (PNG, JPEG) e sequências animadas (GIF)
    integrado ao repositório Grand Theatre.
    """
    
    @staticmethod
    def generate_image(
        prompt: str,
        output_path: str,
        mode: str = "wallpaper",
        title: str = "ROSSINI GENAI",
        subtitle: str = "VISUAL STUDIO",
        text: str = "",
        bg_name: str = "wine",
        pos: str = "right",
        export_format: str = "PNG"
    ) -> str:
        """
        Gera uma imagem estática e converte para o formato desejado (PNG, JPEG).
        """
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        
        # 1. Executa a geração de composição pelo Grand Theatre
        temp_img_path = generate_composition(
            prompt=prompt,
            bg_name=bg_name,
            pos=pos,
            h1=title,
            h3=subtitle,
            h5=text,
            mode=mode,
            style="luxury cinematic editorial",
            lighting="warm golden theatrical lighting",
            atmosphere="subtle cinematic smoke",
            negative="text, watermark, duplicate subjects, distorted faces"
        )
        
        # 2. Converte e salva no formato/extensão de destino
        with Image.open(temp_img_path) as img:
            fmt = export_format.upper()
            if fmt in ["JPG", "JPEG"]:
                img = img.convert("RGB")
                img.save(output_path, "JPEG", quality=95)
            else:
                img.save(output_path, "PNG")
                
        print(f"[Rossini ImageEngine] Imagem salva em: {output_path}")
        return output_path

    @staticmethod
    def create_gif_from_video(
        video_path: str, 
        output_gif_path: str, 
        fps: int = 15, 
        scale_width: int = 480
    ) -> str:
        """
        Extrai um trecho do vídeo gerado pelo Rossini e converte em um GIF animado leve.
        """
        cap = cv2.VideoCapture(video_path)
        frames: List[Image.Image] = []
        
        step = max(1, int(cap.get(cv2.CAP_PROP_FPS) / fps))
        frame_idx = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret or len(frames) >= 150:  # Limite para evitar GIFs gigantes
                break
                
            if frame_idx % step == 0:
                # Redimensiona para manter o GIF leve
                h, w = frame.shape[:2]
                new_h = int(h * (scale_width / w))
                frame_resized = cv2.resize(frame, (scale_width, new_h), interpolation=cv2.INTER_AREA)
                
                # BGR para RGB
                rgb_frame = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
                frames.append(Image.fromarray(rgb_frame))
                
            frame_idx += 1
            
        cap.release()

        if frames:
            frames[0].save(
                output_gif_path,
                save_all=True,
                append_images=frames[1:],
                optimize=True,
                duration=int(1000 / fps),
                loop=0
            )
            print(f"[Rossini ImageEngine] GIF Animado gerado em: {output_gif_path}")
            return output_gif_path
        else:
            raise ValueError("Não foi possível extrair frames para gerar o GIF.")