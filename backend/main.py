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

app = FastAPI(title="Audio Generation API")

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
    return {
        "message": "Audio Generation API", 
        "status": "running",
        "note": "Using Sound Effects API (free tier compatible)"
    }


@app.get("/api/presets", response_model=PresetListResponse)
async def get_presets():
    """Get available meditation presets."""
    from elevenlabs_sdk import MeditationGenerator
    
    presets = MeditationGenerator.list_presets()
    return PresetListResponse(presets=presets)


@app.post("/api/generate-music")
async def generate_music(request: MusicGenerationRequest):
    """Generate audio from a text prompt using ElevenLabs Sound Effects API (works on free tier)."""
    api_key = os.getenv("ELEVENLABS_API_KEY")
    
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="ELEVENLABS_API_KEY not configured. Please set it in your .env file."
        )
    
    try:
        client = ElevenLabs(api_key=api_key)
        
        # Enhance prompt for better music-like results
        enhanced_prompt = request.prompt
        if request.force_instrumental:
            enhanced_prompt = f"{request.prompt}, instrumental, no vocals"
        
        # Generate sound effects (available on free tier)
        # This can create music-like sounds, nature sounds, and ambient audio
        audio_stream = client.text_to_sound_effects.convert(
            text=enhanced_prompt,
            duration_seconds=request.duration_seconds,
        )
        
        # Collect all chunks into bytes
        audio_data = b"".join(chunk for chunk in audio_stream)
        
        # Return as streaming response
        return StreamingResponse(
            BytesIO(audio_data),
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": f'attachment; filename="generated_audio.mp3"'
            }
        )
    
    except Exception as e:
        # Provide more helpful error messages
        error_msg = str(e)
        if "payment_required" in error_msg or "paid_plan" in error_msg.lower():
            raise HTTPException(
                status_code=402,
                detail="This feature requires a paid ElevenLabs plan. The Sound Effects API should work on free tier - please check your API key and account status."
            )
        raise HTTPException(
            status_code=500,
            detail=f"Error generating audio: {error_msg}"
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

