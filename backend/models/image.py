import torch
from PIL import ImageOps
from diffusers import ControlNetModel, StableDiffusionControlNetPipeline, UniPCMultistepScheduler


IMAGE_PROMPT = """
crayon painting, bold crayon strokes, kindergarten's drawing style, bright colors, children's book illustration, drawing diar
""".strip()

IMAGE_NEGATIVE_PROMPT = """
high resolution, 3D rendering, photograph, realistic painting, digital art, abstract, surrealism, adult's drawing style, detailed and complex, dark colors
""".strip()


class ControlNet():
    def __init__(self, device="cpu"):
        # 모델 파이프라인
        controlnet = ControlNetModel.from_pretrained(
            "Dohyeon1/Pictory-controlnet-crayon-r8-edge-lr1e-4-ep10",
            torch_dtype=torch.bfloat16,
            device_map=device
        )
        self.self.pipe = StableDiffusionControlNetPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5", 
            controlnet=controlnet,
            torch_dtype=torch.bfloat16,
            device_map=device
        )
        self.pipe.scheduler = UniPCMultistepScheduler.from_config(self.pipe.scheduler.config)

    @torch.inference_mode()
    def generate(self, image):
        # 이미지 전처리
        image = ImageOps.invert(image).convert("RGB")

        # 그림일기의 그림 생성
        output = self.pipe(
            image=image,
            prompt=IMAGE_PROMPT,
            negative_prompt=IMAGE_NEGATIVE_PROMPT,
            width=1024,
            height=512,
            num_inference_steps=30
        ).images[0]
        return output   # PIL.Image.Image