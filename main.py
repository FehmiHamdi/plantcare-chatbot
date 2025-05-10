from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import requests

app = FastAPI()

# Sert les fichiers statiques (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuration
API_KEY = "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"
MODEL = "mistralai/mistral-7b-instruct"




class ChatRequest(BaseModel):
    message: str

def system_prompt():
    return (
        """
        You are Noubaita, a helpful and friendly virtual assistant specialized in plant care. You work for the website "Noubaita", an online plant shop. Always speak as Noubaita. Begin your first response with a warm welcome like: "Welcome to Noubaita!" or its equivalent in the user's language. Your goal is to provide expert, personalized advice about plant watering, lighting, soil types, and general care. respond in the same language. Maintain a natural, reassuring, and professional tone, and be concise and practical in your answers.
"""

    )

def build_prompt(user_message):
    return user_message

@app.post("/chat")
def chat(request: ChatRequest):
    print("Message reçu :", request.message)

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt()},
            {"role": "user", "content": build_prompt(request.message)}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=body, headers=headers)
    
    print("Réponse brute de l'API :", response.text)

    #  Extraction propre de la réponse
    chatbot_reply = response.json()["choices"][0]["message"]["content"]

    #  Réponse claire vers le frontend
    return {"response": chatbot_reply}



# Serve HTML interface
@app.get("/", response_class=HTMLResponse)
def index():
    with open("index.html", "r", encoding="utf-8") as file:
        return file.read()
