#transcribe.py
import tempfile
import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import whisper
from config import SAMPLE_RATE, WHISPER_MODEL
from utils import fix_arabic, a_log
import arabic_reshaper
from bidi.algorithm import get_display
import re


model = None
def get_model():
    global model
    if model is None:
        a_log("📦 Loading Whisper model ...")
        model = whisper.load_model(WHISPER_MODEL)
    return model

def record_audio(duration=5):
    a_log(f"🎤 Recording {duration}s ...")
    recording = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
    sd.wait()
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        wav.write(tmp.name, SAMPLE_RATE, recording)
        a_log(f"💾 Saved recording to {tmp.name}")
        return tmp.name

def trim_silence(audio_path, silence_thresh=-40, chunk_size=10):
    audio = AudioSegment.from_wav(audio_path)
    nonsilent_ranges = detect_nonsilent(audio, min_silence_len=chunk_size, silence_thresh=silence_thresh)
    if nonsilent_ranges:
        start, end = nonsilent_ranges[0][0], nonsilent_ranges[-1][1]
        trimmed = audio[start:end]
    else:
        trimmed = audio
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        trimmed.export(tmp.name, format="wav")
        return tmp.name

def clean_text(text):
    return re.sub(r'([^\w\s\u0600-\u06FF])', r' \1 ', text)

def transcribe_audio(audio_path):
    m = get_model()  
    result = m.transcribe(audio_path, language="ar")
    text = result["text"].replace("\n", " ").strip()
    text = " ".join(text.split())
    text = clean_text(text)
    text = " ".join(text.split())
    return text

def analyze_audio_file(audio_path):
    """دالة واحدة تجمع التحليل وترجع JSON ثابت"""
    try:
        text = transcribe_audio(audio_path)
        from pipeline import analyze_text
        status, detected_words = analyze_text(text)
        return {
            "text": text,
            "status": status,
            "detected_words": detected_words
        }
    except Exception as e:
        return {
            "text": "",
            "status": "error",
            "detected_words": [],
            "error_message": str(e)
        }
