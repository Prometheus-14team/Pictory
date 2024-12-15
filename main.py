import os
import argparse
import scipy
import torch
import numpy as np
from PIL import Image

from konlpy.tag import Okt
from models import (
    ControlNet,
    Summarizer,
    Text2Audio
)


def parse_args():
    parser = argparse.ArgumentParser()

    # diary text
    parser.add_argument("--text", type=str)

    # model setting
    parser.add_argument("--summarizer", default="psyche/KoT5-summarization", type=str)
    parser.add_argument("--controlnet", default="lllyasviel/sd-controlnet-scribble", type=str)
    parser.add_argument("--diffusion", default="runwayml/stable-diffusion-v1-5", type=str)
    parser.add_argument("--audio_ldm", default="cvssp/audioldm2-large", type=str)

    # summarize task hyperparameter setting

    # img2img task hyperparameter setting
    
    # text2audio hyperparameter setting

    # directory setting
    parser.add_argument("--output_dir", default="./outputs", type=str)

    args = parser.parse_args()
    return args


def main():
    # load arguments 
    args = parse_args()
    content = args.text

    # load models
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

    okt = Okt()
    summarizer = Summarizer(
        args.summarizer, 
        device=device
    )
    img2img = ControlNet(
        args.controlnet, 
        args.diffusion, 
        device=device)
    text2audio = Text2Audio(
        args.audio_ldm,
        device=device
    )

    # sketch drawings
    keywords = list(set(okt.nouns(content)))

    sketch = Image.fromarray(np.zeros((512,512,3), dtype=np.uint8))
    img = img2img.generate(sketch)

    # summarize text
    summarized_content = summarizer.summarize(content)

    # generate audio
    audio = text2audio.generate_audio(summarized_content)

    # save files
    os.makedirs(args.output_dir, exist_ok=True)
    img.save(os.path.join(args.output_dir, "image.png"))
    scipy.io.wavfile.write(os.path.join(args.output_dir, "audio.wav"), rate=16000, data=audio)

    print("Saved Files!")


if __name__ == "__main__":
    main()