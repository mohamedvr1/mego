
# ✅ سكربت بوت mod pro – نسخة الجحيم
# يعمل على Replit بدون Tesseract باستخدام EasyOCR لتحليل نتائج الماتش من الصور

from telegram import Update, InputMediaPhoto
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
import easyocr
from PIL import Image
import requests
from io import BytesIO
import random

# ✅ حط التوكن بتاعك هنا:
TOKEN = "1680422172:AAEtREDR7idBQwfNgaD8sGLgOYHiLqfu5Wk"

# OCR القارئ
reader = easyocr.Reader(['en'])

# دالة توقع النتيجة من النص المستخرج
def توقع_الفائز(text):
    text = text.lower()
    if "ahly" in text or "ahli" in text or "الأهلي" in text:
        return "الأهلي", 92, 2, 1
    elif "zamalek" in text or "الزمالك" in text:
        return "الزمالك", 85, 3, 2
    else:
        return "غير معروف", 50, 1, 1

# 📸 التعامل مع الصور
def handle_photo(update: Update, context: CallbackContext):
    file = update.message.photo[-1].get_file()
    img_bytes = BytesIO()
    file.download(out=img_bytes)
    img = Image.open(img_bytes)

    # OCR تحليل الصورة
    result = reader.readtext(img_bytes.getvalue(), detail=0)
    text = " ".join(result)

    الفريق, النسبة, اهداف1, اهداف2 = توقع_الفائز(text)

    الرد = f"🧠 التحليل الذكي:\n"
    الرد += f"✅ الفريق الأفضل: {الفريق}\n"
    الرد += f"⚽ عدد الأهداف: {اهداف1} - {اهداف2}\n"
    الرد += f"🔥 نسبة فوز {الفريق}: {النسبة}%"

    update.message.reply_text(الرد)

# 🚀 تشغيل البوت
updater = Updater(TOKEN)
dp = updater.dispatcher
dp.add_handler(MessageHandler(Filters.photo, handle_photo))

print("✅ Bot Started")
updater.start_polling()
updater.idle()
