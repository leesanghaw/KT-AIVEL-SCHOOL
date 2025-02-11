# main.py

import os
import json
import glob
import asyncio
from pathlib import Path
from fastapi.websockets import WebSocketState

from config import key_path
from gpt_api import call_gpt_to_extract_features, initialize_openai
from file_reader import read_file
from azure_utils import upload_to_blob_storage, upload_json_to_blob_storage
from char_generation import gen_char
from scene_processing import process_scene
from image_postprocessing import add_bubble_text
from text_chunk_processing import slice_and_process_text, save_json
from model_inference import load_prompt_model_and_tokenizer, prompt_generate

async def process_all_json_and_generate_images(json_directory, raw_output_directory, final_output_directory, char_list, char_save_path, websocket=None, unique_id=None):
    json_files = sorted(
        glob.glob(os.path.join(json_directory, "scene_*.json")),
        key=lambda x: int(os.path.splitext(os.path.basename(x))[0].split("_")[-1])
    )
    print(f"🔍 {len(json_files)}개의 JSON 파일을 발견했습니다. 이미지 생성 시작...")
    for json_file_path in json_files:
        try:
            idx = os.path.splitext(os.path.basename(json_file_path))[0].split("_")[-1]
            gen_file_name = f"scene_{idx}"
            raw_image_path = os.path.join(raw_output_directory, f"{gen_file_name}.png")
            final_image_path = os.path.join(final_output_directory, f"{gen_file_name}.png")
            print(f"📂 {json_file_path} → {raw_image_path} 이미지 생성 중...")
            # 원본 이미지 생성 (말풍선 없음)
            process_scene(json_file_path, raw_image_path, char_list, char_save_path)
            # JSON 데이터 읽고 말풍선 추가 이미지 생성
            with open(json_file_path, "r", encoding="utf-8") as f:
                json_data = json.load(f)
            add_bubble_text(raw_image_path, json_data, final_image_path)
            # 생성된 파일 업로드
            image_blob_name = f"{unique_id}/final_outputs/{gen_file_name}.png"
            image_blob_url = upload_to_blob_storage(final_image_path, image_blob_name)
            json_blob_name = f"{unique_id}/final_outputs/{gen_file_name}.json"
            json_blob_url = upload_json_to_blob_storage(json_file_path, json_blob_name)
            if websocket and websocket.client_state == WebSocketState.CONNECTED:
                message = {
                    "json_url": json_blob_url,
                    "image_url": image_blob_url,
                    "processed_chunks": idx
                }
                await websocket.send_json(message)
                print(f"✅ WebSocket 전송 완료: {message}")
        except Exception as e:
            print(f"❌ {json_file_path} 처리 중 오류 발생: {e}")
    print("✅ 모든 JSON 파일 및 이미지 처리가 완료되었습니다!")

async def main(input_path, work_dir, websocket, unique_id):
    work_dir = Path(work_dir)
    # 디렉토리 설정
    char_save_path = str(work_dir / "char")
    json_directory = str(work_dir / "final_outputs")
    raw_output_directory = str(work_dir / "raw_outputs")
    final_output_directory = str(work_dir / "final_outputs")
    for path in [char_save_path, json_directory, raw_output_directory, final_output_directory]:
        Path(path).mkdir(parents=True, exist_ok=True)
    # OpenAI API 초기화
    initialize_openai(key_path)
    print("✅ OpenAI API 키 로딩 완료!")
    # 텍스트 청크 분할 및 처리 (WebSocket 전송 포함)
    final_output, input_txt = await slice_and_process_text(
        input_path, json_directory, raw_output_directory, final_output_directory, char_save_path, char_save_path, websocket, unique_id
    )
    if final_output:
        print("📤 OpenAI GPT를 통해 추가 분석 진행 중...")
        gpt_result = call_gpt_to_extract_features(input_txt, final_output)
        if gpt_result:
            print("✅ GPT 분석 완료! JSON 변환 중...")
            from json_parser import parse_gpt_result_to_json
            parsed_data = parse_gpt_result_to_json(gpt_result)
            char_json_path = os.path.join(char_save_path, "char.json")
            save_json(parsed_data, char_json_path)
            print(json.dumps(parsed_data, ensure_ascii=False, indent=4))
        else:
            print("❌ GPT 분석 실패!")
        save_json(final_output, os.path.join(json_directory, "final_txt.json"))
        # 캐릭터 이미지 생성
        char_list = gen_char(char_json_path, char_save_path)
        # 모든 JSON에 대해 이미지 생성 및 말풍선 추가
        await process_all_json_and_generate_images(
            json_directory, raw_output_directory, final_output_directory, char_list, char_save_path, websocket, unique_id
        )
    print("🎉 모든 작업이 완료되었습니다!")

if __name__ == "__main__":
    import sys
    # 예시: 명령행 인자로 input_path, work_dir, unique_id 전달 (websocket은 None)
    if len(sys.argv) < 3:
        print("Usage: python main.py <input_path> <work_dir> [unique_id]")
        sys.exit(1)
    input_path = sys.argv[1]
    work_dir = sys.argv[2]
    unique_id = sys.argv[3] if len(sys.argv) > 3 else "default_id"
    asyncio.run(main(input_path, work_dir, websocket=None, unique_id=unique_id))
