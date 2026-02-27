from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware 
from google import genai
import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
async def chat_with_gemini(request: ChatRequest):
    try:
        response = client.models.generate_content(
            model='gemini-3-flash-preview', 
            contents=request.message
            )

        return {"reply": response.text}
    except Exception as e:
        return {"error": f"Bir hata oluştu: {str(e)}"}