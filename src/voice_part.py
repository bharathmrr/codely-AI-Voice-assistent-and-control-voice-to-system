import speech_recognition as sr
import pyttsx3
engine=pyttsx3.init()

def ai_speck(text):
    engine.say(text)
    engine.runAndWait()


def listen_command():
    
    recongzer=sr.Recognizer()
    with sr.Microphone() as source:
        print('listening')
        audio=recongzer.listen(source)
        try:
            return recongzer.recognize_google(audio)
        except sr.UnknownValueError:
            ai_speck("sorry i can't listen any thing")
        
        except sr.RequestError:
            ai_speck("unable to avaliable now")



    