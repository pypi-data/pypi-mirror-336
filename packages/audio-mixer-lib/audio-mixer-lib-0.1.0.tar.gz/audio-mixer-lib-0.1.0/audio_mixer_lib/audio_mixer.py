from pydub import AudioSegment

def mix_audios(file1, file2, output):
    """Mixes two audio files and exports the result."""
    # Load audio files
    audio1 = AudioSegment.from_file(file1, format="mp3")
    audio2 = AudioSegment.from_file(file2, format="mp3")

    # Mix the audio files
    mixed = audio1.overlay(audio2)

    # Export with proper MP3 codec
    mixed.export(output, format="mp3", codec="libmp3lame")

    print(f"✅ Audio mixed and saved as {output}")
