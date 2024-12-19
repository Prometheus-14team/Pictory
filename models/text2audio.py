import torch
from diffusers import AudioLDM2Pipeline


class Text2Audio():
    def __init__(self, model_name="cvssp/audioldm2-large", device="cpu"):
        # 모델 초기화
        self.pipe = AudioLDM2Pipeline.from_pretrained(
            model_name,
            torch_dtype=torch.bfloat16
        )

        # device setting
        self.pipe.to(device)
    
    @torch.no_grad()
    def generate_audio(self, prompt, num_inference_steps=200, audio_length_in_s=10.0, seed=0):
        # set the seed
        generator = torch.Generator("cuda").manual_seed(seed)

        # run the generation
        audio = self.pipe(
            prompt,
            num_inference_steps=num_inference_steps,
            audio_length_in_s=audio_length_in_s,
            generator=generator,
            # num_waveforms_per_prompt=3,
        ).audios[0]
        return audio