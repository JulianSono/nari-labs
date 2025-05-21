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
        duration_seconds = len(text) * 0.1 / pace
        num_samples = int(duration_seconds * sample_rate)
        
        # Create time array
        t = torch.linspace(0, duration_seconds, num_samples)
        
        # Generate a more speech-like waveform
        # Base frequency varies between 100-300 Hz (typical human voice range)
        base_freq = 200.0
        
        # Add some frequency variation to simulate speech
        freq_variation = torch.sin(2 * torch.pi * 2 * t) * 50  # 2 Hz modulation
        frequency = base_freq + freq_variation
        
        # Generate the main carrier wave
        carrier = torch.sin(2 * torch.pi * frequency * t)
        
        # Add amplitude modulation to simulate speech patterns
        am_freq = 5.0  # Amplitude modulation frequency
        am = 0.5 + 0.5 * torch.sin(2 * torch.pi * am_freq * t)
        
        # Combine carrier and amplitude modulation
        waveform = carrier * am
        
        # Add subtle noise for breathiness
        noise = torch.randn(num_samples) * 0.05
        waveform = waveform + noise
        
        # Add emotion-based variations
        if emotion.lower() == "happy":
            waveform = waveform * (1.0 + 0.2 * torch.sin(2 * torch.pi * 10 * t))
        elif emotion.lower() == "sad":
            waveform = waveform * (0.8 + 0.1 * torch.sin(2 * torch.pi * 5 * t))
        elif emotion.lower() == "angry":
            waveform = waveform * (1.2 + 0.3 * torch.sin(2 * torch.pi * 15 * t))
            
        # Add some random pauses to simulate speech
        pause_mask = torch.ones(num_samples)
        num_pauses = len(text) // 5  # Add a pause roughly every 5 characters
        for _ in range(num_pauses):
            pause_start = torch.randint(0, num_samples - int(0.1 * sample_rate), (1,))
            pause_length = int(0.1 * sample_rate)  # 0.1 second pause
            pause_mask[pause_start:pause_start + pause_length] = 0
            
        waveform = waveform * pause_mask
        
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