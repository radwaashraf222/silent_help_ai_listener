import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F
from utils import fix_arabic, a_log

MODEL_NAME = "aubmindlab/bert-base-arabertv02-twitter"

tokenizer = None
model = None
def get_ara_model():
    global tokenizer, model
    if tokenizer is None or model is None:
        a_log("📦 Loading AraBERT model ...")
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForSequenceClassification.from_pretrained(
            MODEL_NAME,
            num_labels=2
        )
        model.eval()
    return tokenizer, model

def predict(text, threshold=0.75):
    tokenizer, model = get_ara_model()
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
    probs = F.softmax(outputs.logits, dim=1)
    confidence = probs[0][1].item()
    return 1 if confidence > threshold else 0
