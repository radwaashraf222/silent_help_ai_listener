#utils.py
import arabic_reshaper
from bidi.algorithm import get_display
import logging
import re


def fix_arabic(text):
    reshaped_text = arabic_reshaper.reshape(str(text))
    bidi_text = get_display(reshaped_text)
    return bidi_text

def format_arabic_with_symbols(text):
    parts = re.split(r'([^\w\s\u0600-\u06FF])', text)
    formatted = ''.join([fix_arabic(p) if re.search(r'[\u0600-\u06FF]', p) else p for p in parts])
    return formatted

#def a_print(*args):
#    fixed_args = [fix_arabic(arg) for arg in args]
#    print(*fixed_args)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)


def a_log(message):
    logging.info(format_arabic_with_symbols(message))
