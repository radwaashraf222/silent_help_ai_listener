# main.py
from transcribe import record_audio, trim_silence, transcribe_audio
from pipeline import analyze_text

from utils import fix_arabic, a_log
from utils import format_arabic_with_symbols
import os  

SAVE_FOLDER = "recordings"
os.makedirs(SAVE_FOLDER, exist_ok=True)

def main():
    a_log("🚀 Smart AI Listener Started...")
    a_log("🛑 اضغط Ctrl+C لإيقاف البرنامج")

    try:
        while True:
            
            audio_file = record_audio(duration=5)

            try:
                audio_file = trim_silence(audio_file)
            except Exception as e:
                a_log(f"⚠️ حدث خطأ أثناء قص الصمت: {e}")

            text = transcribe_audio(audio_file)
            a_log("\n📝 Transcribed text:")
            a_log(text)

            if not text:
                continue

            status, detected_words = analyze_text(text)

            a_log("🎧 تم تسجيل صوت جديد")
            a_log(f"📝 النص: {text}")
            a_log(f"🚦 الحالة: {status}")

            if detected_words:
                a_log(f"🟢 الكلمات المكتشفة: {', '.join(detected_words)}")

            # -------------------------
            if status in ["danger_keyword", "danger_model"]:
                final_path = os.path.join(SAVE_FOLDER, os.path.basename(audio_file))
                os.rename(audio_file, final_path)  
                a_log(f"💾 تم حفظ التسجيل الصوتي لأنه يحتوي على كلمات خطر: {final_path}")
            else:
                try:
                    import sounddevice as sd
                    sd.stop()
                except Exception as e:
                    a_log(f"⚠️ sounddevice غير متاح أو حدث خطأ أثناء إيقاف الصوت: {e}")
                try:
                    if os.path.exists(audio_file):
                        os.remove(audio_file)
                        a_log(f"✅ الملف الآمن تم مسحه من Temp: {audio_file}")
                except Exception as e:
                    a_log(f"⚠️ حدث خطأ أثناء حذف الملف الآمن: {e}")
            # -------------------------

            a_log("-" * 50)

    except KeyboardInterrupt:
        a_log("🛑 تم إيقاف البرنامج بأمان")

if __name__ == "__main__":
    main()



