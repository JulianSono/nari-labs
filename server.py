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

def initialize_model():
    """Initialize the DIA model from checkpoint."""
    checkpoint_path = Path("./checkpoints/dia_model.pt")
    
    if not checkpoint_path.exists():
        raise RuntimeError(
            f"Model checkpoint not found at {checkpoint_path}. "
            "Please ensure the checkpoint file exists in the checkpoints directory."
        )
    
    try:
        # Load model checkpoint
        model = torch.load(checkpoint_path, map_location="cpu")
        model.eval()  # Set to evaluation mode
        return model
    except Exception as e:
        raise RuntimeError(f"Failed to load model checkpoint: {str(e)}")

# Global model instance
model = None

@app.on_event("startup")
async def startup_event():
    global model
    try:
        model = initialize_model()
        print("DIA model loaded successfully")
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
        
        # TODO: Replace with actual DIA generation call
        # audio = model.generate(
        #     text=request.text,
        #     emotion=request.emotion,
        #     tone=request.tone,
        #     pace=request.pace
        # )
        # audio.save(output_path)
        
        return GenerationResponse(
            audio_path=str(output_path),
            message="Audio generated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 