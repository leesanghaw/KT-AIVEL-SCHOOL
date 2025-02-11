import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState
from main import main, upload_to_blob_storage, upload_json_to_blob_storage
from pathlib import Path
import uuid
import traceback  # 오류 디버깅용 추가
from fastapi.middleware.cors import CORSMiddleware
import mimetypes
from fastapi.staticfiles import StaticFiles  # 추가

app = FastAPI()

base_path = Path(__file__).resolve().parent
output_base_path = base_path / "outputs"
output_base_path.mkdir(parents=True, exist_ok=True)


@app.websocket("/ws/text_to_webtoon")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    unique_id = uuid.uuid4().hex
    work_dir = output_base_path / unique_id
    work_dir.mkdir(parents=True, exist_ok=True)

    try:
        async def keepalive():
            while True:
                await asyncio.sleep(10)
                if websocket.client_state == WebSocketState.CONNECTED:
                    try:
                        await websocket.send_json({"status": "ping"})
                        print("📡 Keepalive Ping 전송")
                    except Exception:
                        break

        keepalive_task = asyncio.create_task(keepalive())

        # ✅ 파일 데이터 수신 (바이너리 → 텍스트 순서로 시도)
        file_data = None
        input_file_path = None

        try:
            # **먼저 바이너리 데이터 수신 시도**
            file_data = await websocket.receive_bytes()
            # PDF 파일의 경우, 일반적으로 파일의 시작 부분이 b"%PDF"로 시작합니다.
            if file_data.startswith(b"%PDF"):
                input_file_path = work_dir / "input.pdf"
            else:
                input_file_path = work_dir / "input.txt"
            with open(input_file_path, "wb") as f:
                f.write(file_data)
            print(f"📥 바이너리 파일 저장 완료: {input_file_path}")
        except Exception:
            # 텍스트 데이터 수신 시도
            try:
                file_data = await websocket.receive_text()
                input_file_path = work_dir / "input.txt"
                with open(input_file_path, "w", encoding="utf-8") as f:
                    f.write(file_data)
                print(f"📥 텍스트 파일 저장 완료: {input_file_path}")
            except Exception as e:
                print(f"🚨 데이터 수신 오류: {e}")
                if websocket.client_state == WebSocketState.CONNECTED:
                    await websocket.send_json({"error": "파일 수신 실패"})
                return

        if websocket.client_state == WebSocketState.CONNECTED:
            await websocket.send_json({"message": "파일 수신 완료! 모델 실행 중..."})

        # ✅ 모델 실행을 비동기 Task로 실행
        model_task = asyncio.create_task(run_model_and_send_updates(websocket, input_file_path, work_dir, unique_id))

        while not model_task.done():
            await asyncio.sleep(5)
            if websocket.client_state != WebSocketState.CONNECTED:
                print("🚨 WebSocket 연결 끊김 감지. 모델 실행을 중단합니다.")
                model_task.cancel()
                break

        await model_task

    except WebSocketDisconnect:
        print("🚫 WebSocket 연결이 끊어졌습니다.")
    except Exception as e:
        print(f"🚨 WebSocket 처리 중 오류 발생: {e}")
        if websocket.client_state == WebSocketState.CONNECTED:
            await websocket.send_json({"error": str(e)})

    finally:
        keepalive_task.cancel()
        if websocket.client_state == WebSocketState.CONNECTED:
            await websocket.close()




async def run_model_and_send_updates(websocket: WebSocket, input_file_path, work_dir, unique_id):
    try:
        print("🛠️ 모델 실행 시작...")

        loop = asyncio.get_running_loop()
        model_task = asyncio.create_task(main(str(input_file_path), str(work_dir), websocket, str(unique_id)))

        final_output_dir = Path(work_dir) / "final_outputs"
        processed_files = set()

        while not model_task.done():
            if websocket.client_state == WebSocketState.CONNECTED:
                await websocket.send_json({"status": "🔄 모델 실행 중..."})

            image_files = set(final_output_dir.glob("scene_*.png"))
            new_files = image_files - processed_files

            for image_file in new_files:
                blob_name = f"{unique_id}/final_outputs/{image_file.name}"
                blob_url = upload_to_blob_storage(str(image_file), blob_name)

                if blob_url:
                    print(f"✅ 이미지 업로드 완료: {blob_url}")
                    if websocket.client_state == WebSocketState.CONNECTED:
                        await websocket.send_json({"blob_url": blob_url})

                processed_files.add(image_file)

            if websocket.client_state != WebSocketState.CONNECTED:
                print("🚨 WebSocket 연결 끊김 감지. 모델 실행을 중단합니다.")
                model_task.cancel()
                break

            await asyncio.sleep(5)

        await model_task

        # 최종적으로 정렬된 최종 이미지 URL 리스트 전송
        if websocket.client_state == WebSocketState.CONNECTED:
            sorted_files = sorted(
                final_output_dir.glob("scene_*.png"),
                key=lambda x: int(x.stem.split("_")[1])
            )

            sorted_blob_urls = [
                upload_to_blob_storage(str(image_file), f"{unique_id}/final_outputs/{image_file.name}")
                for image_file in sorted_files
            ]

            sorted_blob_urls = [url for url in sorted_blob_urls if url]

            if sorted_blob_urls:
                await websocket.send_json({"status": "completed", "scene_urls": sorted_blob_urls})
                print("🎉 최종 Scene 이미지 URL 리스트 전송 완료!")
                return

    except WebSocketDisconnect:
        print("🚫 WebSocket 연결이 끊어졌습니다. 모델 실행을 중단합니다.")
        model_task.cancel()
    except Exception as e:
        print(f"🚨 모델 실행 중 오류 발생: {e}")
        if websocket.client_state == WebSocketState.CONNECTED:
            await websocket.send_json({"error": str(e)})




#uvicorn api:app --host 0.0.0.0 --port 2235 --reload --timeout-keep-alive 1200
#uvicorn api:app --host 0.0.0.0 --port 2235 --ssl-keyfile=server.key --ssl-certfile=server.crt
#uvicorn api:app --host 0.0.0.0 --port 8000 --reload --timeout-keep-alive 1200

