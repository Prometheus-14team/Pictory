import scipy
from diffusers import AudioLDM2Pipeline
import torch
from diffusers import StableDiffusionPipeline
import scipy.io.wavfile as wavfile

class Text2Audio:
    def __init__(self, model_name="cvssp/audioldm2-large"):
        # 모델 초기화
        self.pipe = AudioLDM2Pipeline.from_pretrained(model_name)

    def generate_audio(self, prompt, num_inference_steps=200, audio_length_in_s=10.0, file_name="output.wav"):
        
        # set the seed
        generator = torch.Generator("cuda").manual_seed(0)

        # run the generation
        audio = self.pipe(
            prompt,
            num_inference_steps=num_inference_steps,
            audio_length_in_s=audio_length_in_s,
            generator=generator,
            # num_waveforms_per_prompt=3,
        ).audios
        
        
       # save the best audio sample (index 0) as a .wav file
        scipy.io.wavfile.write("14teams_output.wav", rate=16000, data=audio[0])
        print(f"{file_name}로 오디오 파일이 저장")
