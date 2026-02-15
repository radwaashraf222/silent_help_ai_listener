#api.py
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import shutil
import os
import uuid
import time
import logging

from transcribe import analyze_audio_file as original_analyze_audio_file

app = FastAPI(title="Audio Analyzer API")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

UPLOAD_FOLDER = os.path.join("uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

SAVE_FOLDER = os.path.join("recordings")
os.makedirs(SAVE_FOLDER, exist_ok=True)

# -----------------------------
model_loaded = False

def analyze_audio_file(file_path):
    global model_loaded, original_analyze_audio_file
    if not model_loaded:
        logging.info("📦 Loading Whisper model for the first time (lazy load)...")
        model_loaded = True

    start_time = time.time()
    result = original_analyze_audio_file(file_path)
    end_time = time.time()

    logging.info(f"⏱ Analysis time: {end_time - start_time:.2f}s for file {file_path}")
    return result
# -----------------------------


@app.post("/analyze_audio")
async def analyze_audio(
    file: UploadFile = File(...),
    mode: str = Form("background")  # background or manual
):
    temp_path = os.path.join(UPLOAD_FOLDER, file.filename)

    try:
        for old_file in os.listdir(UPLOAD_FOLDER):
            old_file_path = os.path.join(UPLOAD_FOLDER, old_file)
            if os.path.isfile(old_file_path):
                try:
                    os.remove(old_file_path)
                except Exception as e:
                    logging.warning(f"⚠️ Could not delete old temp file {old_file_path}: {e}")

        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = analyze_audio_file(temp_path)

        # -----------------------------
        result["mode"] = mode

        if result["status"] == "danger_keyword":
            result["alert"] = True
            result["alert_type"] = "danger"
        elif mode == "manual":
            result["alert"] = True
            result["alert_type"] = "manual_check"
        else:
            result["alert"] = False
            result["alert_type"] = None
        # -----------------------------

        # -----------------------------
        if mode == "background" and result["status"] == "danger_keyword":
            unique_name = f"{uuid.uuid4()}_{file.filename}"
            final_path = os.path.join(SAVE_FOLDER, unique_name)
            os.rename(temp_path, final_path)
        else:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        # -----------------------------

    except Exception as e:
        result = {
            "text": "",
            "status": "error",
            "detected_words": [],
            "error_message": str(e),
            "mode": mode,
            "alert": False,
            "alert_type": None
        }

        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass

    return JSONResponse(result)

