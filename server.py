from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
import os
from pathlib import Path
import uuid
from typing import Optional

# Initialize FastAPI app
app = FastAPI(title="Nari Labs DIA Voice Generation API")

# Define request model
class GenerationRequest(BaseModel):
    text: str
    emotion: str
    tone: str
    pace: float

# Define response model
class GenerationResponse(BaseModel):
    audio_path: str
    message: str

class FakeModel:
    def generate(self, **kwargs):
        return b"FAKEAUDIO"

def initialize_model():
    print("⚠️ Using FakeModel instead of real DIA model.")
    model = FakeModel()
    return model

# Global model instance
model = None

@app.on_event("startup")
async def startup_event():
    global model
    try:
        model = initialize_model()
        print("Fake model initialized successfully")
    except Exception as e:
        print(f"Error initializing model: {e}")
        raise

@app.post("/generate", response_model=GenerationResponse)
async def generate_audio(request: GenerationRequest):
    if not model:
        raise HTTPException(status_code=500, detail="Model not initialized")
    
    try:
        # Generate unique filename
        output_dir = Path("./output")
        output_dir.mkdir(exist_ok=True)
        filename = f"{uuid.uuid4()}.wav"
        output_path = output_dir / filename
        
        # Fake audio generation
        with open(output_path, "wb") as f:
            f.write(model.generate())
        
        return GenerationResponse(
            audio_path=str(output_path),
            message="Audio generated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 