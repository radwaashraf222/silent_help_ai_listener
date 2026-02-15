#keyword_detect.py
import re

danger_keywords = [
    "الحقني",
    "ساعدني",
    "خطر",
    "حرامي"
]

def remove_diacritics(text):
    arabic_diacritics = re.compile(r'[\u0617-\u061A\u064B-\u0652]')
    return re.sub(arabic_diacritics, '', text)

def normalize_arabic(text):
    text = re.sub("[إأآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ؤ", "و", text)
    text = re.sub("ئ", "ي", text)
    text = re.sub("ة", "ه", text)
    return text

def simple_stem(word):
    suffixes = ["ني", "نا", "كم", "هم", "ات", "ون", "ين", "ه"]
    for suffix in suffixes:
        if word.endswith(suffix) and len(word) > len(suffix) + 2:
            return word[:-len(suffix)]
    return word


def preprocess(text):
    text = remove_diacritics(text)
    text = normalize_arabic(text)
    return text


def check_keywords(text):
    detected = []

    text = preprocess(text)
    words = text.split()

    processed_keywords = [preprocess(k) for k in danger_keywords]

    for word in words:
        stemmed_word = simple_stem(word)

        for keyword in processed_keywords:
            stemmed_keyword = simple_stem(keyword)
            if stemmed_keyword in stemmed_word:
                detected.append(keyword)

    return list(set(detected))
