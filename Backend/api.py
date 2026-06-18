#api.py
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
#from child_chatbot import child_chatbot
import shutil
import os
import uuid
import time
import logging
from datetime import datetime

from transcribe import analyze_audio_file as original_analyze_audio_file

app = FastAPI(title="Audio Analyzer API")
logging.info("🚀 API Service Started Successfully")

# Models are loaded lazily on the first request (see analyze_audio_file)
# instead of at startup, so the health check passes quickly and the
# deploy does not time out while downloading the models from HuggingFace.

@app.get("/")
def root():
    return {"status": "ok", "service": "Audio Analyzer API"}

@app.on_event("startup")
def load_models():
#    from arabert_model import get_ara_model
#    from transcribe import get_model

#    get_model()
#    get_ara_model()
    pass

@app.get("/health")
def health():
    return {"status": "healthy"}

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
#model_loaded = False
@app.get("/warmup")
def warmup():
#    from transcribe import get_model
#    get_model()
    return {"status": "OK"}


def analyze_audio_file(file_path):
    global model_loaded, original_analyze_audio_file

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

        if result["status"] in ["danger_keyword", "danger_model"]:
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
        if mode == "background" and result["status"] in ["danger_keyword", "danger_model"]:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_name = f"file_{timestamp}.wav"
            final_path = os.path.join(SAVE_FOLDER, unique_name)
            os.rename(temp_path, final_path)
            logging.info(f"💾 Saved danger recording: {final_path}")
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

#@app.post("/chat")
#def chat(message: str):
#    response = child_chatbot(
#        "test_user",
#        message
#    )

#    return {"response": response}



# ----------------------------------------
# uvicorn Backend.api:app --port 8001  "open it"
# ----------------------------------------
#ctrl+c  "close it"
