# Nari Labs DIA Voice Generation Server

This is a FastAPI-based server that hosts the Nari Labs DIA voice generation model on RunPod. The server provides an API endpoint for generating expressive speech audio from text input.

## Setup Instructions

### RunPod Deployment

1. Create a new RunPod instance with the following specifications:
   - GPU: NVIDIA A100 or similar
   - Container: Custom
   - Base Image: PyTorch 2.1.0 with CUDA 11.8

2. Upload the model checkpoints to the `./checkpoints/` directory in the container.

3. Build and deploy the container:
   ```bash
   docker build -t nari-dia-server .
   docker run -d -p 8000:8000 nari-dia-server
   ```

### Local Development

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Place model checkpoints in the `./checkpoints/` directory.

4. Start the server:
   ```bash
   python server.py
   ```

## API Usage

### Generate Audio

**Endpoint:** `POST /generate`

**Request Body:**
```json
{
    "text": "Text to convert to speech",
    "emotion": "happy",
    "tone": "friendly",
    "pace": 1.0
}
```

**Response:**
```json
{
    "audio_path": "/path/to/generated/audio.wav",
    "message": "Audio generated successfully"
}
```

### Example Usage

Using curl:
```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, this is a test.",
    "emotion": "happy",
    "tone": "friendly",
    "pace": 1.0
  }'
```

Using Python:
```python
import requests

response = requests.post(
    "http://localhost:8000/generate",
    json={
        "text": "Hello, this is a test.",
        "emotion": "happy",
        "tone": "friendly",
        "pace": 1.0
    }
)
print(response.json())
```

## Local Testing

Run the included test script:
```bash
python generate_local.py
```

## Directory Structure

```
.
├── server.py           # Main FastAPI server
├── generate_local.py   # Local testing script
├── requirements.txt    # Python dependencies
├── Dockerfile         # Container configuration
├── checkpoints/       # Model checkpoints directory
└── output/           # Generated audio files directory
```

## Notes

- The server automatically creates an `output` directory for generated audio files
- Each generated audio file has a unique UUID filename
- Make sure to have sufficient disk space for generated audio files
- The server uses port 8000 by default
