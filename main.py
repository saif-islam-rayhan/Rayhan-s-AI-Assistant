
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Define the request body model
class ChatRequest(BaseModel):
    user_query: str
    session_id: str

# n8n webhook URL
WEBHOOK_URL = "https://mujhid36.app.n8n.cloud/webhook/b1049294-a45c-491a-8cba-ffeb5394755d"

@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Forward chat requests to n8n webhook
    """
    try:
        # Prepare the payload
        payload = {
            "user_query": request.user_query,
            "session_id": request.session_id
        }
        
        # Send POST request to n8n webhook
        async with httpx.AsyncClient() as client:
            response = await client.post(WEBHOOK_URL, json=payload, timeout=30.0)
            response.raise_for_status()
            
            # Return the webhook response directly
            return response.json() if response.text else {}
    
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Error forwarding to webhook: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/")
async def root():
    """
    Health check endpoint
    """
    return {"message": "FastAPI Chat Endpoint is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)