from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
import os
from pathlib import Path
import uuid
from typing import Optional
from fastapi.staticfiles import StaticFiles
import torchaudio

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

class VoiceModel:
    def __init__(self, model_path: str, device: str = "cpu"):
        self.device = device
        # TODO: Implement actual model loading
        print("⚠️ Using placeholder model. Please implement actual model loading.")
        
    def generate(self, text: str, emotion: str, tone: str, pace: float) -> dict:
        # TODO: Implement actual generation
        # Placeholder implementation
        sample_rate = 22050
        # Estimate audio length based on text length (roughly 0.1 seconds per character)
        # Adjust pace factor (0.5 to 2.0) to make it faster or slower
        duration_seconds = len(text) * 0.1 / pace
        num_samples = int(duration_seconds * sample_rate)
        
        # Generate a more interesting waveform (sine wave with varying frequency)
        t = torch.linspace(0, duration_seconds, num_samples)
        frequency = 440.0  # A4 note
        waveform = torch.sin(2 * torch.pi * frequency * t)
        
        # Add some variation based on emotion and tone
        if emotion.lower() == "happy":
            frequency *= 1.2
        elif emotion.lower() == "sad":
            frequency *= 0.8
            
        # Add some noise for realism
        noise = torch.randn(num_samples) * 0.1
        waveform = waveform + noise
        
        # Normalize and reshape to match torchaudio format (channels, samples)
        waveform = waveform / torch.max(torch.abs(waveform))
        waveform = waveform.unsqueeze(0)  # Add channel dimension
        
        return {
            "waveform": waveform,
            "sample_rate": sample_rate
        }

def initialize_model():
    model_path = Path("./checkpoints/dia_model.pt")
    if not model_path.exists():
        print("⚠️ Model checkpoint not found. Using placeholder model.")
        return VoiceModel("placeholder")
    
    try:
        model = VoiceModel(str(model_path), device="cpu")
        print("✅ Model loaded successfully.")
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        print("⚠️ Falling back to placeholder model.")
        return VoiceModel("placeholder")

# Global model instance
model = None

@app.on_event("startup")
async def startup_event():
    global model
    try:
        model = initialize_model()
        print("Model initialized successfully")
    except Exception as e:
        print(f"Error initializing model: {e}")
        raise

@app.post("/generate", response_model=GenerationResponse)
async def generate_audio(request: GenerationRequest):
    if not model:
        raise HTTPException(status_code=500, detail="Model not initialized")
    
    try:
        output_dir = Path("./output")
        output_dir.mkdir(exist_ok=True)
        filename = f"{uuid.uuid4()}.wav"
        output_path = output_dir / filename

        print("🧠 Generating audio...")
        audio = model.generate(
            text=request.text,
            emotion=request.emotion,
            tone=request.tone,
            pace=request.pace,
        )

        # Save using torchaudio
        torchaudio.save(str(output_path), audio["waveform"], sample_rate=audio["sample_rate"])

        return GenerationResponse(
            audio_path=f"/output/{filename}",
            message="✅ Audio generated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio generation failed: {str(e)}")

# Mount the output directory for static file serving
app.mount("/output", StaticFiles(directory="output"), name="output")

# Mount the frontend static files
frontend_path = Path(__file__).parent / "frontend" / "dist"
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 