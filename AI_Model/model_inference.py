import torch
from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration

def load_model_and_tokenizer():
    """
    모델과 토크나이저를 로드하고 GPU로 이동합니다.
    """
    model_path = "C:/Users/minkyu/Desktop/img2webtoon/kobart-summarization-finetuned"
    tokenizer = PreTrainedTokenizerFast.from_pretrained(model_path)
    model = BartForConditionalGeneration.from_pretrained(model_path)

    # GPU 사용 여부 확인
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    return tokenizer, model, device

def generate_output(tokenizer, model, text, max_length=512):
    """
    모델을 통해 텍스트를 처리하고 출력합니다. (GPU 사용 가능)
    """
    device = next(model.parameters()).device  # 모델이 있는 장치 가져오기
    inputs = tokenizer(text, return_tensors="pt", padding="max_length", truncation=True, max_length=max_length)
    inputs = {key: value.to(device) for key, value in inputs.items()}  # GPU로 이동

    output_ids = model.generate(
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_length=max_length,
        num_beams=4,
        length_penalty=1.0,
        early_stopping=True,
    )

    return tokenizer.decode(output_ids[0], skip_special_tokens=True)

def load_prompt_model_and_tokenizer():
    """
    모델과 토크나이저를 로드하고 GPU로 이동합니다.
    """
    model_path = "C:/Users/minkyu/Desktop/img2webtoon/prompt-model"
    tokenizer = PreTrainedTokenizerFast.from_pretrained(model_path)
    model = BartForConditionalGeneration.from_pretrained(model_path)

    # GPU 사용 여부 확인
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    return tokenizer, model, device

def prompt_generate(tokenizer, model, text):
    """
    Prompt 생성 시 CPU/GPU 일관성 유지
    """
    device = next(model.parameters()).device  # ✅ 모델이 있는 장치 확인
    inputs = tokenizer(
        text,
        return_tensors="pt",
        padding="max_length",
        truncation=True,
        max_length=512
    ).to(device)  # ✅ 입력을 모델의 장치로 이동

    # ✅ 모델이 있는 장치와 동일한 곳에서 실행
    output_ids = model.generate(
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_length=512,
        num_beams=4,
        length_penalty=1.0,
        early_stopping=True,
    )

    return tokenizer.decode(output_ids[0], skip_special_tokens=True)
    
