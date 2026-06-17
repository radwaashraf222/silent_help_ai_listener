#main.py
# Entry point for Railway / production.
# Railway runs `python main.py`, so this file boots the FastAPI app
# defined in Backend/api.py using uvicorn on the port Railway provides.

import os
import uvicorn

# The FastAPI app lives in Backend/api.py and imports modules from the
# project root (transcribe, arabert_model, config). Running from the
# project root keeps those imports working.
from Backend.api import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
