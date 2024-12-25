from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import openai
import os
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables
load_dotenv()

# Get OpenAI API key and app password from .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LOGIN_PASSWORD = os.getenv("APP_PASSWORD")

# Set the OpenAI API key
openai.api_key = OPENAI_API_KEY

app = FastAPI()

# Set up templates and static files
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/js", StaticFiles(directory="app/js"), name="js")

# Login Route (GET) - Show Login Page
@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Login Route (POST) - Process Login Form
@app.post("/login")
async def login(request: Request, password: str = Form(...)):
    if password == LOGIN_PASSWORD:
        # Set an auth cookie
        response = RedirectResponse(url="/chat", status_code=303)
        response.set_cookie(key="authenticated", value="true")
        return response
    else:
        # Return to login with error
        return templates.TemplateResponse(
            "login.html", 
            {"request": request, "error": "Incorrect password"}
        )

# Protected Chat Route
@app.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request):
    # Check for authentication cookie
    auth_cookie = request.cookies.get("authenticated")
    if auth_cookie == "true":
        return templates.TemplateResponse("chat.html", {"request": request})
    return RedirectResponse(url="/")

# Define a request model
class MessageRequest(BaseModel):
    message: str

# Chatbot Response Route
@app.post("/chat")
async def get_bot_response(request: MessageRequest):
    try:
        # Call OpenAI API to generate a response
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use the correct model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": request.message}
            ],
            temperature=0.3,
            max_tokens=5000
        )

        # Debugging: Print the full response from OpenAI
        print(f"OpenAI Response: {response}")

        # Check if the response contains 'choices' and is not empty
        if 'choices' in response and len(response.choices) > 0:
            # Extract the bot's response
            bot_message = response.choices[0].message["content"]
            print(f"Bot Response: {bot_message}")  # Debugging bot response
            return {"response": bot_message}
        else:
            # If 'choices' is empty or not found, log and return a message
            print(f"No valid choices found in response: {response}")
            return {"response": "Sorry, I didn't get a valid response from the model."}

    except Exception as e:
        # Log any exceptions that occur during the API call
        print(f"Error: {str(e)}")
        return {"error": f"An error occurred: {str(e)}"}

# Logout Route (Optional)
@app.post("/logout")
async def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("authenticated")
    return response
