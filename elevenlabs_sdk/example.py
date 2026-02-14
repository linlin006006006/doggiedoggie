"""Example: Generate AI meditation sounds with ElevenLabs."""

import os

from dotenv import load_dotenv

from elevenlabs_sdk import MeditationGenerator


def main():
    print("=" * 60)
    print("ElevenLabs SDK - AI Meditation Sounds Demo")
    print("=" * 60)
    print()

    # Check for API key
    load_dotenv()
    if not os.getenv("ELEVENLABS_API_KEY"):
        print("ELEVENLABS_API_KEY not set!")
        print()
        print("To use this SDK:")
        print("1. Get an API key at: https://elevenlabs.io")
        print("2. Add to .env file: ELEVENLABS_API_KEY=your_key_here")
        print()
        print("Demo will show available features without API calls.")
        print("-" * 40)
        print()

        # Show sound presets even without API key
        print("Available Sound Presets:")
        sound_presets = [
            "nature_rain",
            "ocean_waves",
            "forest_morning",
            "tibetan_bowls",
        ]
        for name in sound_presets:
            config = MeditationGenerator.PRESETS.get(name, {})
            print(f"  {name}: {config.get('description', '')}")
        print()
        return

    generator = MeditationGenerator()

    # Generate nature sounds
    print("Generating nature sound (20 seconds)...")
    print("-" * 40)
    print("  Description: peaceful forest stream with birds")
    print()

    nature = generator.generate_nature_sound(
        description="peaceful forest stream with birds",
        duration_seconds=20,
    )

    nature.save("forest_stream.mp3")
    print()

    # Generate transition sound
    print("Generating transition bell...")
    print("-" * 40)

    bell = generator.generate_transition_sound(
        sound_type="bowl",
        duration_seconds=5,
    )

    bell.save("meditation_bell.mp3")
    print()

    # Generate ocean waves from preset
    print("Generating from 'ocean_waves' preset...")
    print("-" * 40)

    ocean = generator.generate_from_preset(
        preset="ocean_waves",
        duration_seconds=30,
    )

    ocean.save("ocean_waves.mp3")
    print()

    print("=" * 60)
    print("Demo complete!")
    print()
    print("Generated files:")
    print("  - forest_stream.mp3")
    print("  - meditation_bell.mp3")
    print("  - ocean_waves.mp3")
    print()
    print("See example_music.py for AI music generation!")
    print("=" * 60)


if __name__ == "__main__":
    main()
