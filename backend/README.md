# Music Generation Backend

FastAPI backend for generating music using ElevenLabs API.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the backend directory:
```
ELEVENLABS_API_KEY=your_api_key_here
```

3. Run the server:
```bash
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

- `GET /` - Health check
- `GET /api/presets` - Get available meditation presets
- `POST /api/generate-music` - Generate music from custom prompt
- `POST /api/generate-from-preset` - Generate music from preset

## Example Request

```bash
curl -X POST "http://localhost:8000/api/generate-music" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "peaceful ambient piano with soft synthesizer pads",
    "duration_seconds": 30,
    "force_instrumental": true
  }' \
  --output music.mp3
```

