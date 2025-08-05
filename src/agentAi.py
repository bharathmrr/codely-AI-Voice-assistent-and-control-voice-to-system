import ollama
import speech_recognition as sr
import pyttsx3
import tkinter as tk
from tkinter import scrolledtext
import threading
import queue
import pywhatkit  # <-- Added

# === Ollama Setup === #
client = ollama.Client()
model = 'gemma3:1b-it-qat'

# === Text-to-Speech === #
engine = pyttsx3.init()
def ai_speak(text):
    engine.say(text)
    engine.runAndWait()

# === Voice Recognition === #
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print('🎤 Listening...')
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            ai_speak("Sorry, I couldn't understand.")
            return "None"
        except sr.RequestError:
            ai_speak("Service unavailable.")
            return "None"
        except sr.WaitTimeoutError:
            ai_speak("No command heard.")
            return "None"


def ask_gemma(prompt: str) -> str:
    try:
        system_instruction = (
            "You are Codely, a helpful voice assistant created by Bharath. "
            "You respond briefly and politely like Siri, using 1-2 short sentences. "
            "Speak in a conversational tone, avoid long or technical answers unless asked. "
            "Always stay concise and friendly."
        )
        full_prompt = f"{system_instruction}\nUser: {prompt}\nCodely:"
         
        
        response = client.generate(model=model, prompt=full_prompt)
        return response['response'].strip()
    except Exception as e:
        return f"Error from LLM: {str(e)}"

# === Task Helpers === #
def handle_google_search(query: str):
    try:
        search_term = query.lower().replace("search", "").replace("on google", "").strip()
        ai_speak(f"Searching Google for {search_term}")
        pywhatkit.search(search_term)
    except Exception as e:
        ai_speak(f"Failed to search: {e}")

def handle_youtube_play(query: str):
    try:
        song = query.lower().replace("play", "").replace("on youtube", "").replace("open youtube", "").strip()
        ai_speak(f"Playing {song} on YouTube")
        pywhatkit.playonyt(song)
    except Exception as e:
        ai_speak(f"Failed to play video: {e}")

# === Main Assistant Loop === #
def run_gemma_chat(gui_ref):
    while gui_ref.running:
        user_input = listen_command()
        if user_input == "None":
            continue

        gui_ref.append_message(user_input, "User")
        input_lower = user_input.lower()

        if "play" in input_lower or "youtube" in input_lower:
            handle_youtube_play(user_input)
        elif "search" in input_lower or "google" in input_lower:
            handle_google_search(user_input)
        else:
            response = ask_gemma(user_input)
            gui_ref.append_message(response, "Gemma")
            ai_speak(response)

        gui_ref.root.update()


class VoiceAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CODELY AI VOICE ASSISTANT")
        self.root.geometry("600x400")
        self.root.configure(bg="#2c3e50")

        self.queue = queue.Queue()
        self.running = False

        self.title_label = tk.Label(root, text="CODELY AI VOICE ASSISTANT", font=("Helvetica", 18, "bold"),
                                    bg="#2c3e50", fg="#ecf0f1")
        self.title_label.pack(pady=10)

        self.status_label = tk.Label(root, text="Status: Ready", font=("Helvetica", 12),
                                     bg="#2c3e50", fg="#3498db")
        self.status_label.pack(pady=5)

        self.conversation_area = scrolledtext.ScrolledText(
            root, height=15, width=60, font=("Helvetica", 10),
            bg="#34495e", fg="#ecf0f1", wrap=tk.WORD
        )
        self.conversation_area.pack(pady=10)
        self.conversation_area.config(state='disabled')

        self.start_button = tk.Button(root, text="Start Listening", font=("Helvetica", 12),
                                      bg="#3498db", fg="#ecf0f1", command=self.start_listening)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(root, text="Stop", font=("Helvetica", 12),
                                     bg="#e74c3c", fg="#ecf0f1", command=self.stop_listening, state='disabled')
        self.stop_button.pack(pady=5)

    def append_message(self, message, sender="Gemma"):
        self.conversation_area.config(state='normal')
        self.conversation_area.insert(tk.END, f"{sender}: {message}\n")
        self.conversation_area.see(tk.END)
        self.conversation_area.config(state='disabled')

    def update_status(self, status):
        self.status_label.config(text=f"Status: {status}")

    def start_listening(self):
        if not self.running:
            self.running = True
            self.start_button.config(state='disabled')
            self.stop_button.config(state='normal')
            self.update_status("Listening...")
            threading.Thread(target=run_gemma_chat, args=(self,), daemon=True).start()

    def stop_listening(self):
        self.running = False
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.update_status("Stopped")

# === Main === #
if __name__ == "__main__":
    def custom_print(*args, **kwargs):
        msg = " ".join(map(str, args))
        gui.append_message(msg, "System")

    import builtins
    builtins.print = custom_print

    root = tk.Tk()
    gui = VoiceAssistantGUI(root)
    root.mainloop()
