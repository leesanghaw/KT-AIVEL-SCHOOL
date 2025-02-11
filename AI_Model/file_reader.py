import os
import fitz  

def read_text_file(file_path):
    """
    텍스트 파일을 읽어 내용을 반환합니다.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def read_pdf_file(file_path):
    """
    PDF 파일을 읽어 내용을 텍스트로 변환하여 반환합니다.
    """
    text = ""
    try:
        with fitz.open(file_path) as pdf_document:
            for page in pdf_document:
                text += page.get_text("text") + "\n"
    except Exception as e:
        print(f"PDF 파일을 읽는 중 오류 발생: {e}")
    return text

def read_file(file_path, slice_num=10000):
    """
    파일 확장자를 확인하고 적절한 읽기 함수 호출
    """
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    if file_extension == ".txt":
        return read_text_file(file_path)
    elif file_extension == ".pdf":
        return read_pdf_file(file_path)
    else:
        print("지원되지 않는 파일 형식입니다. (.txt, .pdf만 지원)")
        return None