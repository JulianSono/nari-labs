from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
import os
from pathlib import Path
import uuid
from typing import Optional
from fastapi.staticfiles import StaticFiles
from dia.model import DiffusionVocoderModel  # Adjust based on real class
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

def initialize_model():
    model_path = Path("./checkpoints/dia_model.pt")  # Adjust to your actual model path
    if not model_path.exists():
        raise FileNotFoundError("Model checkpoint not found.")

    model = DiffusionVocoderModel.load_model(model_path, device="cpu")  # or "cuda" if on GPU
    model.eval()
    print("✅ DIA model loaded successfully.")
    return model

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