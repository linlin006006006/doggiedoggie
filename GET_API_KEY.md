# How to Get an ElevenLabs API Key

## Step-by-Step Instructions

### 1. Sign Up / Log In
- Go to [https://elevenlabs.io](https://elevenlabs.io)
- Sign up for a new account or log in if you already have one

### 2. Navigate to API Keys
- Once logged in, go to your **Profile/Settings**
- Look for **"API Keys"** or **"Settings"** → **"API Keys"**
- Direct link: [https://elevenlabs.io/app/settings/api-keys](https://elevenlabs.io/app/settings/api-keys)

### 3. Create Your API Key
- Click **"Create API Key"** or **"Generate New Key"**
- Give it a name (e.g., "Music Generator App")
- Copy the API key immediately - **you won't be able to see it again!**

### 4. Add to Your Backend
Create a `.env` file in the `backend/` directory:

```bash
cd backend
touch .env
```

Add your API key to the `.env` file:
```
ELEVENLABS_API_KEY=your_actual_api_key_here
```

**Important**: 
- Never commit the `.env` file to git
- Keep your API key secret
- The `.env` file should already be in `.gitignore`

### 5. Verify It Works
Restart your backend server if it's running, then try generating music in the app.

## Important Notes

⚠️ **Music Generation Requires Paid Plan**
- The Music API (used by this app) requires a **paid ElevenLabs subscription**
- Free tier accounts can use Text-to-Speech and Sound Effects, but not Music Generation
- Check [ElevenLabs pricing](https://elevenlabs.io/pricing) for current plans

## Troubleshooting

If you get an error about the API key:
1. Make sure the `.env` file is in the `backend/` directory (not the root)
2. Check that the key is copied correctly (no extra spaces)
3. Restart the backend server after adding the key
4. Verify your ElevenLabs account has access to the Music API

