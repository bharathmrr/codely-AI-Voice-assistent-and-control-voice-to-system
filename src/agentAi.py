from langchain.agents import Tool, AgentType, initialize_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.tools import tool
from langgraph.graph import StateGraph, END

import pywhatkit as kit
import speech_recognition as sr
import pyttsx3
from typing import TypedDict
from pydantic import BaseModel, Field

# === TTS and STT === #
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

# === Gemini LLM === #
llm = ChatGoogleGenerativeAI(
    model='gemini-2.0-flash',
    api_key=""
)

# === Tool: Google/Wiki search === #
@tool
def search_google(query: str) -> str:
    """Search Wikipedia or Google for the query."""
    return kit.info(query, lines=10)

# === LangChain Agent === #
agent = initialize_agent(
    llm=llm,
    tools=[search_google],
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# === State for LangGraph === #
class State(TypedDict):
    query: str
    operator: str

# === Operator Classification Model === #
class Operater(BaseModel):
    agent_decs: str = Field(
        ...,
        description=(
            "Classify the user query:\n"
            "- 'youtube': play a song or video\n"
            "- 'whatsapp': send a WhatsApp message\n"
            "- 'google': search something\n"
            "- 'chat': general conversation\n"
            "- 'end': end session"
        )
    )

llm_s = llm.with_structured_output(Operater)

# === Step 1: Listen & Classify === #
def listen_ai(state: State) -> State:
    data = listen_command()
    if not data:
        return {"query": "None", "operator": "end"}
    res = llm_s.invoke(data)
    return {
        "query": data,
        "operator": res.agent_decs.lower()
    }

# === Step 2: Decision Node === #
def des_node(state: State) -> State:
    return {
        "query": state["query"],
        "operator": state["operator"]
    }

# === Step 3: General Chat === #
def assistent_ai(state: State) -> State:
    print('User:', state['query'])
    response = agent.invoke(state['query'])
    ai_speck(str(response))
    return state

# === WhatsApp Messaging === #
@tool
def whatapp_respode_tool(message: str, number: str) -> str:
    """Send WhatsApp message to known numbers."""
    kit.sendwhatmsg_instantly(number, message, wait_time=10, tab_close=True)
    return f"Sent: {message} to {number}"

whatapp_prompt = PromptTemplate(
    template="Send WhatsApp message: {message}\nKnown: gowtham:+919014183896, imran khan:+917032885667",
    input_variables=['message']
)

def whatsapp_agent(state: State) -> State:
    chain = whatapp_prompt | llm.bind_tools([whatapp_respode_tool]) | StrOutputParser()
    chain.invoke({'message': state['query']})
    return state

# === YouTube === #
format_prompt = PromptTemplate(
    template="Convert to a clean one-line search query: {user_query}",
    input_variables=['user_query']
)

def youtube_search(state: State) -> State:
    chain = format_prompt | llm | StrOutputParser()
    query_ = chain.invoke({'user_query': state['query']})
    kit.playonyt(query_)
    return state

# === Google Search === #
def live_google_search(state: State) -> State:
    chain = format_prompt | llm | StrOutputParser()
    query_ = chain.invoke({'user_query': state['query']})
    kit.search(query_)
    return state

# === LangGraph Workflow === #
workflow = StateGraph(State)

# Nodes
workflow.add_node('Listen.AI', listen_ai)
workflow.add_node('Decision.AI', des_node)
workflow.add_node('Assistant.AI', assistent_ai)
workflow.add_node('Whatsapp.AI', whatsapp_agent)
workflow.add_node('Youtube.AI', youtube_search)
workflow.add_node('Google.AI', live_google_search)

# Edges
workflow.add_edge('Listen.AI', 'Decision.AI')

workflow.add_conditional_edges(
    'Decision.AI',
    lambda state: state["operator"],
    {
        'youtube': 'Youtube.AI',
        'google': 'Google.AI',
        'chat': 'Assistant.AI',
        'whatsapp': 'Whatsapp.AI',
        'end': END
    }
)

workflow.add_edge('Assistant.AI', 'Listen.AI')
workflow.add_edge('Whatsapp.AI', 'Listen.AI')
workflow.add_edge('Youtube.AI', 'Listen.AI')
workflow.add_edge('Google.AI', 'Listen.AI')

workflow.set_entry_point('Listen.AI')
graph = workflow.compile()

# === Run Assistant === #
if __name__ == "__main__":
    print("🎙️ Codely Voice Assistant started. Say something!")
    graph.invoke({})
