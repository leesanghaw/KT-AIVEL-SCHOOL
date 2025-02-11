import re
from model_inference import load_prompt_model_and_tokenizer, prompt_generate
def clean_text(text, allow_empty=True):
    """
    텍스트에서 불필요한 문자나 특수 문자를 제거합니다.
    """
    if not isinstance(text, str):
        return text
    
    # 앞뒤 공백 제거
    text = text.strip()
    
    # 백슬래시 제거
    text = text.replace("\\", "")
    
    # 따옴표 정리
    text = re.sub(r'^["\']|["\']$', '', text)  # 문자열 시작과 끝의 따옴표 제거
    text = re.sub(r'\\?"$', '', text)  # 문장 끝의 \" 제거
    text = re.sub(r'\\?"', '"', text)  # \" → " 변환
    text = re.sub(r"\\?'", "'", text)  # \' → ' 변환
    
    # 불필요한 ']', '[', 개행 문자 제거
    text = text.replace("]", "").replace("[", "").replace("\n", " ").strip()

    # 추가된 로직: 문장 끝에 있는 " 또는 '를 삭제
    text = re.sub(r'["\']$', '', text)

    # 단독 큰따옴표(") 또는 작은따옴표(')만 남았을 경우 빈 문자열로 변경
    if text in ['"', "'"]:
        text = ""

    # 빈 문자열 처리를 허용할지 여부 (빈 값 유지)
    if not allow_empty and text == "":
        return None

    return text

prompt_tokenizer, prompt_model, prompt_device = load_prompt_model_and_tokenizer()

def parse_output_to_json(generated_output):
    """
    모델의 출력 결과를 JSON 형식으로 변환하며, caption을 이용해 prompt를 생성합니다.
    """
    parsed_data = {}
    try:
        location_match = re.search(r"\[location\]\s*(.+)", generated_output)
        parsed_data["location"] = clean_text(location_match.group(1)) if location_match else None

        caption_match = re.search(r"\[caption\]\s*(.+)", generated_output)
        caption_text = clean_text(caption_match.group(1)) if caption_match else None
        parsed_data["caption"] = caption_text

        # ✅ caption이 존재하는 경우만 Prompt 생성
        if caption_text:
            print(f"📢 Caption 기반 Prompt 생성 중...: {caption_text}")
            prompt_text = prompt_generate(prompt_tokenizer, prompt_model, caption_text)
            
            # ✅ 기존 clean_text() 적용하여 불필요한 문자 제거
            cleaned_prompt = clean_text(prompt_text)
            
            print("✅ 정리된 Prompt:", cleaned_prompt)
            parsed_data["prompt"] = cleaned_prompt  # ✅ prompt 추가
        else:
            print("⚠️ Caption 없음: Prompt 생성 생략")

        dialogues_match = re.search(r"\[dialogues\]\s*(\[.+)", generated_output, re.DOTALL)
        if dialogues_match:
            dialogues_raw = dialogues_match.group(1).strip()
            dialogue_list = re.findall(r"\[speaker\]\s*(.*?)\s*\[dialogue\]\s*(.*?)(?=\[speaker\]|\Z)", dialogues_raw, re.DOTALL)

            parsed_dialogues = []
            for speaker, dialogue in dialogue_list:
                parsed_dialogues.append({
                    "speaker": clean_text(speaker.strip(), allow_empty=True),
                    "dialogue": clean_text(dialogue.strip(), allow_empty=True)
                })

            parsed_data["dialogues"] = parsed_dialogues
        else:
            parsed_data["dialogues"] = []

        return parsed_data
    except Exception as e:
        print(f"❌ JSON 디코딩 실패! 출력: {generated_output}")
        print(f"❌ 에러 메시지: {e}")
        return {}

def parse_gpt_result_to_json(result):
    """
    GPT 모델 결과를 JSON 형태로 변환
    """
    try:
        # 텍스트를 라인별로 분리
        lines = result.strip().split("\n")

        # 시대적 배경 추출
        background = None
        characters = []

        for line in lines:
            if line.startswith("[시대적 배경]"):
                background = line.replace("[시대적 배경] ", "").strip()
            elif line.startswith("[") and "]" in line:
                name, appearance = line.split("]", 1)
                characters.append({
                    "name": name.replace("[", "").strip(),
                    "appearance": appearance.strip()
                })

        # 모든 캐릭터 포함한 JSON 반환
        data = {
            "background": background,
            "characters": characters
        }
        return data

    except Exception as e:
        return {"error": f"Failed to parse result: {e}"}