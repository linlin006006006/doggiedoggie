"""FastAPI backend for music generation using ElevenLabs."""

import os
import sys
from io import BytesIO
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from elevenlabs import ElevenLabs

# Add parent directory to path to import SDK modules
backend_dir = Path(__file__).parent
sdk_dir = backend_dir.parent
sys.path.insert(0, str(sdk_dir))

# Load environment variables
load_dotenv()

app = FastAPI(title="Music Generation API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MusicGenerationRequest(BaseModel):
    """Request model for music generation."""
    prompt: str
    duration_seconds: float = 30.0
    force_instrumental: bool = True


class PresetListResponse(BaseModel):
    """Response model for preset list."""
    presets: dict[str, str]


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Music Generation API", "status": "running"}


@app.get("/api/presets", response_model=PresetListResponse)
async def get_presets():
    """Get available meditation presets."""
    from elevenlabs_sdk import MeditationGenerator
    
    presets = MeditationGenerator.list_presets()
    return PresetListResponse(presets=presets)


@app.post("/api/generate-music")
async def generate_music(request: MusicGenerationRequest):
    """Generate music from a text prompt using ElevenLabs Music API."""
    api_key = os.getenv("ELEVENLABS_API_KEY")
    
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="ELEVENLABS_API_KEY not configured. Please set it in your .env file."
        )
    
    try:
        client = ElevenLabs(api_key=api_key)
        
        # Convert duration from seconds to milliseconds
        duration_ms = int(request.duration_seconds * 1000)
        
        # Clamp duration between 1 second and 5 minutes (ElevenLabs limit)
        duration_ms = max(1000, min(duration_ms, 300000))
        
        # Generate music
        audio_stream = client.music.compose(
            prompt=request.prompt,
            music_length_ms=duration_ms,
            model_id="music_v1",
            force_instrumental=request.force_instrumental,
        )
        
        # Collect all chunks into bytes
        audio_data = b"".join(chunk for chunk in audio_stream)
        
        # Return as streaming response
        return StreamingResponse(
            BytesIO(audio_data),
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": f'attachment; filename="generated_music.mp3"'
            }
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating music: {str(e)}"
        )


@app.post("/api/generate-from-preset")
async def generate_from_preset(preset: str, duration_seconds: float = 60.0):
    """Generate music from a preset."""
    from elevenlabs_sdk import MeditationGenerator
    
    api_key = os.getenv("ELEVENLABS_API_KEY")
    
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="ELEVENLABS_API_KEY not configured. Please set it in your .env file."
        )
    
    try:
        generator = MeditationGenerator(api_key=api_key)
        
        # Generate from preset
        audio = generator.generate_from_preset(
            preset=preset,
            duration_seconds=duration_seconds
        )
        
        # Return as streaming response
        return StreamingResponse(
            BytesIO(audio.get_bytes()),
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": f'attachment; filename="{preset}_music.mp3"'
            }
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating music: {str(e)}"
        )

