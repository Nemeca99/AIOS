# voice_interface.py
# Archive auditory interface scaffold (for offline use)

import speech_recognition as sr
import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("🎤 Listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "❌ I couldn't understand that."
    except sr.RequestError:
        return "❌ Speech recognition service is unavailable."

if __name__ == "__main__":
    command = listen()
    print("🗣️ You said:", command)
    speak(f"You said: {command}")
