import speech_recognition as sr
from translate import Translator
from gtts import gTTS
from playsound import playsound
from pydub import AudioSegment
import io
import time
import os

def recognize_and_translate(recognizer, microphone, translator, target_language='fr'):
    with microphone as source:
        time.sleep(1)
        print("Listening...")
        try:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=10)
            text = recognizer.recognize_google(audio, language='en')
            print(f"You said: {text}")
            translation = translator.translate(text)
            print(f"Translation to {target_language}: {translation}")
            return translation
        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None

def play_translation(audio_data):
    if audio_data:
        tts = gTTS(text=audio_data, lang='kn')
        mp3_data = io.BytesIO()
        tts.write_to_fp(mp3_data)
        mp3_data.seek(0)

        with open("translation.mp3", "wb") as f:
            f.write(mp3_data.read())

        os.system("start translation.mp3")


def main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    target_language = 'kn'

    while True:
        translator = Translator(to_lang=target_language)
        translation = recognize_and_translate(recognizer, microphone, translator, target_language)
        play_translation(translation)

if __name__ == "__main__":
    main()
