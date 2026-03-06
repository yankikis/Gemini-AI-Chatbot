from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware 
from google import genai
import os
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse 


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
    history: list


@app.post("/chat")
async def chat_with_gemini(request: ChatRequest):
    try:
        response_stream = client.models.generate_content_stream(
            model='gemini-3-flash-preview',
            contents=request.history
        )

        def generate():
            for chunk in response_stream:
                if chunk.text:
                    yield chunk.text

        return StreamingResponse(generate(), media_type="text/plain")
    
    except Exception as e:
        return {"error": f"Bir hata oluştu: {str(e)}"}