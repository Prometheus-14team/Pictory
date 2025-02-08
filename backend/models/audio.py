import torch
from diffusers import AudioLDM2Pipeline


AUDIO_PROMPT = ""
AUDIO_NEGATIVE_PROMPT = ""


class AudioLDM():
    def __init__(self, device="cpu"):
        # 모델 파이프라인
        self.pipe = AudioLDM2Pipeline.from_pretrained(
            "cvssp/audioldm2-large",
            torch_dtype=torch.float16
        )

        # 모델 디바이스 이동
        self.pipe.to(device)
    
    @torch.inference_mode()
    def generate(self, prompt):
        # 오디오 생성
        output = self.pipe(
            prompt,
            negative_prompt=AUDIO_NEGATIVE_PROMPT,
            num_inference_steps=100,
            audio_length_in_s=10.0,
        ).audios[0]
        return output