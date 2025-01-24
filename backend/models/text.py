import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


HF_TOKEN = ""


class LLM():
    def __init__(self, model_path="google/gemma-2-2b-it", device="cpu"):
        # 모델 & 토크나이저
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_path,
            token=HF_TOKEN
        )
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            model_path,
            torch_dtype=torch.bfloat16,
            load_in_8bit=True,
            attn_implementation="flash_attention_2",
            device_map=device,
            token=HF_TOKEN
        )

        # 요약 태스크 프롬프트 포맷
        self.summarizarion_prompt = """
        <bos><start_of_turn>user
        Summarize the content to **a sentence in Korean**.

        This is an example:
        content: 나는 오늘 점심에 놀이공원에 갔다. 저녁에는 맛있는 고기를 먹었다. 정말 행복한 하루였다.
        summary: 오늘 놀이공원에 가고 고기도 먹어 행복한 하루였다.

        You MUST generate 'summary' into a sentence.
        content: {text}<end_of_turn>
        <start_of_turn>model
        summary:
        """.strip().replace("    ", "")

        # 번역 태스크 프롬프트 포맷
        self.translation_prompt = """
        <bos><start_of_turn>user
        Summarize the content to **a sentence in Korean**.

        This is an example:
        content: 오늘 놀이공원에 가고 고기도 먹어 행복한 하루였다.
        translation: Today was a happy day to go to the amusement park and eat meat.

        You MUST generate 'translation' into a sentence.
        content: {text}<end_of_turn>
        <start_of_turn>model
        translation:
        """.strip().replace("    ", "")

    @torch.inference_mode()
    def summarize(self, text, max_length=30):
        # 입력 데이터 준비
        prompt = self.summarizarion_prompt.format(text=text)
        inputs = self.tokenizer(
            prompt, 
            add_special_tokens=False, 
            return_tensors="pt"
        ).to(self.model.device)
        
        # 요약문 생성
        outputs = self.model.generate(
            **inputs, 
            max_length=max_length,
            length_penalty=2.0, 
            early_stopping=True
        )
        summary = self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        ).split("summary:")[-1]
        return summary

    @torch.inference_mode()
    def translate(self, text):
        # 입력 데이터 준비
        prompt = self.translation_prompt.format(text=text)
        inputs = self.tokenizer(
            prompt, 
            add_special_tokens=False, 
            return_tensors="pt"
        ).to(self.model.device)
        
        # 번역문 생성
        outputs = self.model.generate(
            **inputs,
            early_stopping=True
        )
        translation = self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        ).split("translation:")[-1]
        return translation