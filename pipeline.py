# pipeline.py
from keyword_detect import check_keywords
# from arabert_model import predict

def analyze_text(text):
    detected_words = check_keywords(text)

    if detected_words:
        status = "danger_keyword"
    # elif predict(text) == 1:
    #     status = "danger_model"
    else:
        status = "safe"

    return status, detected_words
