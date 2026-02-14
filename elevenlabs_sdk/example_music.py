"""Example: Generate AI meditation music with ElevenLabs Music API."""

import os

from dotenv import load_dotenv
from elevenlabs import ElevenLabs


def main():
    print("=" * 60)
    print("ElevenLabs SDK - AI Music Generation Demo")
    print("=" * 60)
    print()

    # Check for API key
    load_dotenv()
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        print("ELEVENLABS_API_KEY not set!")
        print()
        print("To use this SDK:")
        print("1. Get an API key at: https://elevenlabs.io")
        print("2. Add to .env file: ELEVENLABS_API_KEY=your_key_here")
        print()
        print("Note: Music generation requires a paid ElevenLabs plan.")
        print("=" * 60)
        return

    client = ElevenLabs(api_key=api_key)

    # Generate meditation music from a simple prompt
    print("Generating meditation music (30 seconds)...")
    print("-" * 40)
    prompt = "peaceful ambient meditation music with soft piano and gentle pads, slow tempo, calming atmosphere"
    print(f"  Prompt: {prompt}")
    print()

    audio_data = client.music.compose(
        prompt=prompt,
        music_length_ms=30000,
        model_id="music_v1",
        force_instrumental=True,
    )

    # Save the generated audio
    output_path = "meditation_music.mp3"
    with open(output_path, "wb") as f:
        for chunk in audio_data:
            f.write(chunk)
    print(f"  Saved to: {output_path}")
    print()

    # Generate ambient drone music
    print("Generating ambient drone (20 seconds)...")
    print("-" * 40)
    drone_prompt = "deep ambient drone, warm synthesizer pads, evolving textures, no rhythm, meditation background"
    print(f"  Prompt: {drone_prompt}")
    print()

    drone_audio = client.music.compose(
        prompt=drone_prompt,
        music_length_ms=20000,
        model_id="music_v1",
        force_instrumental=True,
    )

    with open("ambient_drone.mp3", "wb") as f:
        for chunk in drone_audio:
            f.write(chunk)
    print("  Saved to: ambient_drone.mp3")
    print()

    # Generate morning meditation music
    print("Generating morning meditation music (30 seconds)...")
    print("-" * 40)
    morning_prompt = "gentle morning meditation music, soft acoustic guitar and flute, peaceful sunrise atmosphere, hopeful"
    print(f"  Prompt: {morning_prompt}")
    print()

    morning_audio = client.music.compose(
        prompt=morning_prompt,
        music_length_ms=30000,
        model_id="music_v1",
        force_instrumental=True,
    )

    with open("morning_meditation.mp3", "wb") as f:
        for chunk in morning_audio:
            f.write(chunk)
    print("  Saved to: morning_meditation.mp3")
    print()

    print("=" * 60)
    print("Demo complete!")
    print()
    print("Generated files:")
    print("  - meditation_music.mp3")
    print("  - ambient_drone.mp3")
    print("  - morning_meditation.mp3")
    print()
    print("Tips for better results:")
    print("  - Describe genre, mood, instruments, and tempo")
    print("  - Use 'force_instrumental=True' for no vocals")
    print("  - Max duration is 5 minutes (300000 ms)")
    print("=" * 60)


if __name__ == "__main__":
    main()
