# AI Music Generator

A full-stack application for generating music using ElevenLabs AI. Features a React frontend and FastAPI backend.

## Quick Start

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your ElevenLabs API key:
```
ELEVENLABS_API_KEY=your_api_key_here
```

4. Start the FastAPI server:
```bash
uvicorn main:app --reload --port 8000
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Features

- **Custom Music Generation**: Enter any text description to generate music
- **Preset Sounds**: Use pre-configured meditation and nature sound presets
- **Adjustable Duration**: Set duration from 1 to 300 seconds (5 minutes max)
- **Audio Preview**: Built-in audio player to preview generated music
- **Download**: Download generated music as MP3 files

## API Endpoints

- `GET /` - Health check
- `GET /api/presets` - Get available meditation presets
- `POST /api/generate-music` - Generate music from custom prompt
  ```json
  {
    "prompt": "peaceful ambient piano with soft synthesizer pads",
    "duration_seconds": 30,
    "force_instrumental": true
  }
  ```
- `POST /api/generate-from-preset?preset=<preset_name>&duration_seconds=<duration>` - Generate from preset

## Notes

- You need an ElevenLabs API key to use this application
- Music generation requires a paid ElevenLabs plan
- Maximum duration is 300 seconds (5 minutes)

