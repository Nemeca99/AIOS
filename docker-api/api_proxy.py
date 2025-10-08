"""
AIOS API Proxy - Docker container for LM Studio integration
Acts as a secure middleman between Streamlit Cloud and your local LM Studio
"""

import os
import logging
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AIOS API Proxy",
    description="Secure proxy between Streamlit Cloud and LM Studio",
    version="1.0.0"
)

# CORS middleware for Streamlit Cloud
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Streamlit domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
LM_STUDIO_URL = os.getenv("LM_STUDIO_URL", "http://host.docker.internal:1234")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))

# Pydantic models
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str = "local-model"
    messages: list[ChatMessage]
    temperature: float = 0.7
    max_tokens: int = 500
    stream: bool = False

class ChatResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: list[Dict[str, Any]]
    usage: Dict[str, int]

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "AIOS API Proxy",
        "version": "1.0.0",
        "status": "running",
        "lm_studio_url": LM_STUDIO_URL
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{LM_STUDIO_URL}/v1/models", timeout=5)
            if response.status_code == 200:
                return {"status": "healthy", "lm_studio": "connected"}
            else:
                return {"status": "unhealthy", "lm_studio": "disconnected"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {"status": "unhealthy", "error": str(e)}

@app.get("/v1/models")
async def get_models():
    """Proxy GET /v1/models to LM Studio"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{LM_STUDIO_URL}/v1/models", timeout=API_TIMEOUT)
            return response.json()
    except Exception as e:
        logger.error(f"Error getting models: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatRequest):
    """Proxy chat completions to LM Studio"""
    try:
        logger.info(f"Chat request: {len(request.messages)} messages")
        
        # Prepare request for LM Studio
        lm_studio_request = {
            "model": request.model,
            "messages": [{"role": msg.role, "content": msg.content} for msg in request.messages],
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
            "stream": request.stream
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{LM_STUDIO_URL}/v1/chat/completions",
                json=lm_studio_request,
                timeout=API_TIMEOUT
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Chat response: {result.get('usage', {})}")
                return result
            else:
                logger.error(f"LM Studio error: {response.status_code} - {response.text}")
                raise HTTPException(status_code=response.status_code, detail=response.text)
                
    except httpx.TimeoutException:
        logger.error("Request timeout")
        raise HTTPException(status_code=504, detail="Request timeout")
    except Exception as e:
        logger.error(f"Error in chat completions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/completions")
async def completions(request: Request):
    """Proxy completions to LM Studio"""
    try:
        body = await request.json()
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{LM_STUDIO_URL}/v1/completions",
                json=body,
                timeout=API_TIMEOUT
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)
                
    except Exception as e:
        logger.error(f"Error in completions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/embeddings")
async def embeddings(request: Request):
    """Proxy embeddings to LM Studio"""
    try:
        body = await request.json()
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{LM_STUDIO_URL}/v1/embeddings",
                json=body,
                timeout=API_TIMEOUT
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)
                
    except Exception as e:
        logger.error(f"Error in embeddings: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )

if __name__ == "__main__":
    uvicorn.run(
        "api_proxy:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
