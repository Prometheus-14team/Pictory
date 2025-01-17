import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from konlpy.tag import Okt


class Summarizer():
    def __init__(self, model_name="psyche/KoT5-summarization", device="cpu"):
        # 모델과 토크나이저 초기화
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            model_name,
            torch_dtype=torch.bfloat16
        )

        # device setting
        self.model.to(device)

    @torch.no_grad()
    def summarize(self, text, max_length=30, min_length=10):
        # 입력 데이터 준비
        inputs = self.tokenizer(
            text, return_tensors="pt").to(self.model.device)
        
        # 모델을 이용해 요약 생성
        outputs = self.model.generate(
            **inputs, 
            max_length=max_length, 
            min_length=min_length, 
            length_penalty=2.0, 
            num_beams=4, 
            early_stopping=True
        )
        summary = self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )
        return summary


def stemmer(sentence):
    okt = Okt()  
    nouns = okt.nouns(sentence)  
    return nouns