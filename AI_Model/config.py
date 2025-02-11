# config.py

import os
from pathlib import Path
import torch
from dotenv import dotenv_values
from huggingface_hub import login

# Hugging Face 로그인
token_file = "huggingface_token.txt"
try:
    with open(token_file, "r", encoding="utf-8") as f:
        token = f.read().strip()  # 불필요한 공백 제거
    login(token=token)
    print("Hugging Face 로그인에 성공했습니다.")
except FileNotFoundError:
    print(f"❌ 파일을 찾을 수 없습니다: {token_file}")
except Exception as e:
    print(f"❌ 로그인 중 오류 발생: {e}")

# 디바이스 및 데이터 타입 설정
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
dtype = torch.float16 if device.type == "cuda" else torch.float32

# 기본 경로 및 파일 경로 설정
base_path = Path(__file__).resolve().parent
key_path = base_path / "open_api_key.txt"      # GPT API 키 파일 경로
font_path = base_path / "web.ttf"              # 폰트 파일 경로
unet_path = base_path / "unet"
saved_model_path = base_path / "model_weight" / "best_model.pth"

# Azure 환경 변수 설정 ('.env' 파일에 AZURE_CON_STRING, AZURE_CONTAINER_NAME 정의)
config_env = dotenv_values(".env")
AZURE_CON_STRING = config_env.get("AZURE_CON_STRING")
AZURE_CONTAINER_NAME = config_env.get("AZURE_CONTAINER_NAME")

# 이미지 생성 기본 상수들
DEFAULT_NEGATIVE_PROMPT = '''FastNegativeV2,(bad-artist:1.0),
    (worst quality, low quality:1.4), (bad_prompt_version2:0.8),
    bad-hands-5,lowres, bad anatomy, bad hands, ((text)), (watermark),
    error, missing fingers, extra digit, fewer digits, cropped,
    worst quality, low quality, normal quality, ((username)), blurry,
    (extra limbs), bad-artist-anime, badhandv4, EasyNegative,
    ng_deepnegative_v1_75t, verybadimagenegative_v1.3, BadDream,
    (three hands:1.1),(three legs:1.1),(more than two hands:1.4),
    (more than two legs,:1.2),badhandv4,EasyNegative,ng_deepnegative_v1_75t,verybadimagenegative_v1.3,(worst quality, low quality:1.4),text,words,logo,watermark,(overexposure : 1.3),
    ,speech bubble'''

DEFAULT_NUM_INFERENCE_STEPS = 100
DEFAULT_HEIGHT = 512
DEFAULT_WIDTH = 512

# (선택사항) 작업 디렉토리 구조를 동적으로 생성하는 함수
def setup_paths(base_path):
    paths = {
        "char_save_path": base_path / "char",            # 캐릭터 이미지 저장
        "json_directory": base_path / "text_json",         # JSON 저장
        "output_directory": base_path / "scene_outputs",   # 중간 결과 이미지 저장
        "final_output_directory": base_path / "final_outputs",# 최종 이미지(말풍선 추가) 저장
    }
    for key, path in paths.items():
        if "path" in key and not path.exists():
            path.mkdir(parents=True, exist_ok=True)
    return paths
