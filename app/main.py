# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from fastapi import Request

# Load your OpenAI API key
openai.api_key = "your-openai-api-key"

app = FastAPI()

# Setup Jinja2 template and static files
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Your custom information about yourself (e.g., resume details)
custom_context = """
I am a software engineer with experience in Cloud Engineering, Systems Engineering, Networking, and Security.
I am skilled in Python, FastAPI, Kubernetes, and Linux. I have a passion for building efficient, scalable systems.
"""

class ChatRequest(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/ask")
async def ask_question(request: ChatRequest):
    user_message = request.message
    # Combining user input with custom context to guide the model's responses
    full_input = f"{custom_context}\nUser: {user_message}\nAI:"

    try:
        # Query OpenAI's GPT-4 API
        response = openai.Completion.create(
            engine="gpt-4",  # Change to "gpt-3.5-turbo" if needed
            prompt=full_input,
            max_tokens=150,
            n=1,
            stop=["User:", "AI:"]
        )
        model_answer = response.choices[0].text.strip()
        return {"response": model_answer}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
