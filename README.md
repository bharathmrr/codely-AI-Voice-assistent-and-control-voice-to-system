# codely-AI-Voice-assistent-and-control-voice-to-system
codely-AI Voice assistent and control voice to system(like open youtube,search on google,wiki,send messages to spectfic person automatic chat option)
🎙️ Codely – Your AI Voice Assistant
“Code that listens. Intelligence that responds.”

🔥 What is Codely?
Codely is a powerful, extensible, and modern AI voice assistant built using Python, LangChain, and LangGraph, with real-time voice interaction and LLM-powered reasoning.

It allows users to speak natural language commands, which are processed using state-of-the-art language models, and executes meaningful actions like:

🎵 Playing songs on YouTube

🕒 Telling the current time

🔍 Searching on Google

🔄 Extensible to any future function — such as sending messages, opening apps, and more

It’s designed to be lightweight, developer-friendly, and privacy-conscious — running entirely on your local device (except for API calls to LLMs).

🎯 Vision
Codely stands at the intersection of voice interfaces, agent orchestration, and LLM-driven task automation.

It’s designed to demonstrate how small, modular AI tools can replicate large-scale assistant behaviors (like Siri, Alexa, or Google Assistant) in a transparent and customizable way.

⚙️ Architecture Overview
vbnet
Copy
Edit
 ┌─────────────┐      ┌───────────────┐       ┌────────────┐       ┌──────────────┐
 │ Your Voice  ├─────▶ Speech-to-Text ├──────▶ LangChain    ├─────▶ LangGraph     │
 └─────────────┘      └───────────────┘       └────┬───────┘       └────┬─────────┘
                                                   ▼                   ▼
                                             Action Detection      Intent Routing
                                                   ▼                   ▼
                                               Command Logics ───▶ Final Execution
🔧 Tools & Technologies Used
Component	Tech Used
Voice Recognition	SpeechRecognition, PyAudio
TTS (Speech Output)	pyttsx3
LLM	OpenAI, can be replaced by Gemini
Action Execution	pywhatkit, webbrowser, datetime
Flow Orchestration	LangGraph
Language Reasoning	LangChain

🧠 Codely's Brain: LangGraph + LangChain
🧩 LangChain
LangChain allows Codely to interpret free-form user text into structured instructions.

Codely uses it to:

Parse user intent

Extract action types (e.g., play_music, tell_time)

Help route command execution

“Play Naatu Naatu on YouTube” → LangChain predicts: play_music

🔄 LangGraph
LangGraph allows Codely to follow logical workflows and multi-step tasks. It defines nodes like:

ParseCommand: Use LLM to determine what action is needed.

Execute: Based on the parsed action, do something (e.g., open YouTube, speak time, etc.).

END: Stop after execution, unless in continuous listening mode.

This design makes Codely modular and future-proof.

✨ Functillo (Capabilities & Commands)
Here’s what Codely can currently do — and how to use it.

Category	Example Command	Action Taken
🎵 Music	“Play Naatu Naatu on YouTube”	Opens YouTube and plays the song
🔍 Web Search	“Search who is the prime minister of India”	Opens Google search
🕒 Time	“What is the time now?”	Replies with the current time
🔚 Exit	“Stop”, “Exit”, “Quit”	Gracefully ends the assistant

Future functions will include:

Opening apps
Reading emails
Sending WhatsApp messages
Checking weather
Running Python code or system commands

🧬 Detailed Workflow
Let’s walk through what happens when you say:
“Open YouTube and play Naatu Naatu”
1. 🎙️ Voice Recognition
SpeechRecognition module captures your voice.
It uses Google Speech API to convert to text.
2. 🧠 Command Understanding
LangChain takes the spoken text and asks the LLM:
"What should I do with this?"
It maps your command to one of:
play_music
search_google
tell_time
unknown

3. 🕹️ LangGraph Routing
The flow graph routes the parsed action to the correct node.

If action = play_music, go to the play_music node.

4. 🚀 Action Execution
Codely uses pywhatkit.playonyt("Naatu Naatu") to open YouTube and play.

It gives you a spoken confirmation using pyttsx3.

5. 🔁 Loop or End
After execution, it returns to listening for the next command (until you say “exit”).

🛠️ Extending Codely
You can easily add more functionality by modifying execute_action():

python
Copy
Edit
elif action == "open_gmail":
    webbrowser.open("https://mail.google.com")
    speak("Opening your Gmail.")
Or teach new intents in parse_command() using few-shot prompt tuning.

Want multi-turn dialogues? Add memory support via LangChain.

💡 Why Codely?
Feature	Description
✅ Customizable	Easy to add new voice commands or LLM behaviors
🧠 LLM-Powered	Understands natural, flexible commands
🔄 Modular Workflow	LangGraph makes the system organized and traceable
🧩 Plugin-Ready	Add any Python function or web automation easily
🔒 Runs Locally	Your voice and commands aren’t stored in the cloud

🔄 Coming Soon
✅ Wake word detection (e.g., “Hey Codely”)

✅ Whisper-based local transcription

✅ GPT-4o or Gemini 1.5 Pro integration

✅ Chat with documents

✅ Streamlit GUI for desktop experience

✅ Full offline version with local LLM

🚀 Getting Started
bash
Copy
Edit
git clone https://github.com/your-username/codely.git
cd codely
pip install -r requirements.txt
Add your OpenAI API key to config.py, then run:

bash
Copy
Edit
python main.py
📢 Branding Ideas
Tagline: "Talk Code. Live Smart."

Logo: Sound wave + circuit or microphone + LangGraph node visual

Mascot Idea: Futuristic glowing orb or cube with voice aura

📁 Directory (Standard Layout)
graphql
Copy
Edit
codely/
├── main.py           # Main assistant script
├── README.md         # Docs
├── requirements.txt  # Dependencies
🙋 Author
Bharathsimha Reddy Putta
Final Year CSE | AI/ML Engineer
Project Builder | AI Researcher
GitHub: https://github.com/bharathmrr
LinkedIn: https://www.linkedin.com/in/bharathsimha-reddy-putta-a2292a211
