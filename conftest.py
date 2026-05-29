import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture(autouse=True)
def mute_audio_and_tolk():
    patchers = [
        patch('audio.AudioManager.speak', return_value=None),
        patch('audio.AudioManager.play_sound', return_value=None),
        patch('audio.AudioManager.play_music', return_value=None),
        patch('audio.AudioManager.play_loop', return_value=None),
        patch('audio.AudioManager.stop_music', return_value=None),
        patch('audio.AudioManager.stop_loop', return_value=None),
        # Also patch pygame to be completely silent
        patch('pygame.mixer.Sound', return_value=MagicMock()),
        patch('pygame.mixer.music.play', return_value=None),
        patch('pygame.mixer.init', return_value=None),
        patch('pygame.mixer.quit', return_value=None),
        # In case tests directly call Tolk or pyttsx3
        patch('ctypes.windll.LoadLibrary', return_value=MagicMock()),
    ]
    
    for p in patchers:
        try:
            p.start()
        except Exception:
            pass
            
    yield
    
    for p in patchers:
        try:
            p.stop()
        except Exception:
            pass
