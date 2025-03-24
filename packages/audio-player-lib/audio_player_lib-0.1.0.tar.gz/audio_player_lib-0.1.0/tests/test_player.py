import pytest
from audio_player.player import play_audio

def test_play_audio():
    assert callable(play_audio)
