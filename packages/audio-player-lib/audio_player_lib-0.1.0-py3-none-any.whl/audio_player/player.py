from pydub import AudioSegment
from pydub.playback import play

def play_audio(file_path):
    """Plays an audio file."""
    try:
        sound = AudioSegment.from_file(file_path)
        play(sound)
    except Exception as e:
        print(f"Error playing audio: {e}")
