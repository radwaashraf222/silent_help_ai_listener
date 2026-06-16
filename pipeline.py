# pipeline.py
from keyword_detect import check_keywords
from arabert_model import predict
from utils import a_log

def analyze_text(text):
    detected_words = check_keywords(text)

    if detected_words:
        status = "danger_keyword"
    else:
        label, confidence = predict(text)
        a_log(f"📊 confidence: {confidence:.2f}")

        if label == 1 and confidence > 0.8:
            status = "danger_model"
        else:
            status = "safe"

    return status, detected_words
