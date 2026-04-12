from fastapi import FastAPI, UploadFile, File
import whisper
import shutil
from googletrans import Translator
from gtts import gTTS
import os
import uuid

app = FastAPI()

model = whisper.load_model("tiny")
translator = Translator()

@app.get("/")
def home():
    return {"message": "AI Voice Translator API is running 🚀"}

@app.post("/translate-audio/")
async def translate_audio(file: UploadFile = File(...)):
    filename = f"temp_{uuid.uuid4()}.wav"

    with open(filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = model.transcribe(filename)
    text = result["text"]
    lang = result["language"]

    if lang != "en":
        translated = translator.translate(text, dest="en")
        english_text = translated.text
    else:
        english_text = text

    output_audio = f"output_{uuid.uuid4()}.mp3"
    tts = gTTS(text=english_text, lang="en")
    tts.save(output_audio)

    os.remove(filename)

    return {
        "original_text": text,
        "detected_language": lang,
        "translated_text": english_text,
        "audio_file": output_audio
    }
