# char_generation.py

import json
from googletrans import Translator
from image_generation import generate_char

def gen_char(json_path, save_dir):
    # JSON 파일 로드
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    characters = data.get('characters', [])
    char_list = [char['name'] for char in characters]
    
    translator = Translator()
    translated_features = []
    for char in characters:
        features = char.get('appearance', '')
        try:
            translation = translator.translate(features, src='ko', dest='en')
            translated_features.append({
                "name": char['name'],
                "translated_features": translation.text
            })
        except Exception as e:
            print(f"번역 중 오류 발생: {e}")
            translated_features.append({
                "name": char['name'],
                "translated_features": features
            })
    
    for i, char in enumerate(translated_features):
        name = char['name']
        prompt = char['translated_features']
        output_path = f"{save_dir}/{name}.png"
        generate_char(prompt, output_path)
        print(f'캐릭터 이미지 생성 중입니다: {i + 1}/{len(translated_features)}')
    
    print("모든 캐릭터 생성이 완료되었습니다.")
    return char_list

def run_gen_char(json_path, save_dir):
    char_list = gen_char(json_path, save_dir)
    return char_list
