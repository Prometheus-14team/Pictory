from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class Summarizer:
    def __init__(self, model_name="psyche/KoT5-summarization"):
        # 모델과 토크나이저 초기화
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    def summarize(self, text, max_length=100, min_length=30):
        # 입력 데이터 준비
        input_ids = self.tokenizer.encode(text, return_tensors="pt", truncation=True)
        
        # 모델을 이용해 요약 생성
        summary_ids = self.model.generate(input_ids, max_length=max_length, min_length=min_length, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        
        return summary