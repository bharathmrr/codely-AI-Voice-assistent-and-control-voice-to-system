import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init()

def ai_speck(text):
    engine.say(text)
    engine.runAndWait()

def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print('🎤 Listening...')
        audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            ai_speck("Sorry, I couldn't understand.")
        except sr.RequestError:
            ai_speck("Service unavailable.")
