import torch
from PIL import Image
from diffusers import (
    ControlNetModel, 
    StableDiffusionControlNetPipeline, 
    UniPCMultistepScheduler
)


class ControlNet():
    def __init__(self, controlnet_path, diffusion_path="runwayml/stable-diffusion-v1-5", device="cpu"):
        """
        controlnet_path -> str
        diffusion_path -> str
        device -> str or torch.device

        """
        # load model and pipeline
        controlnet = ControlNetModel.from_pretrained(controlnet_path)
        self.pipe = StableDiffusionControlNetPipeline.from_pretrained(
            diffusion_path, controlnet=controlnet)
        self.pipe.scheduler = UniPCMultistepScheduler.from_config(self.pipe.scheduler.config)

        # set device
        self.pipe.to(device)

    @torch.no_grad()
    def generate(self, img, prompt="transfer to scribble style.", num_inference_steps=20):
        """
        img -> PIL.Image.Image
        prompt -> str
        num_inference_steps -> int

        """
        output = self.pipe(prompt, img, num_inference_steps=num_inference_steps).images[0]
        return output   # PIL.Image.Image