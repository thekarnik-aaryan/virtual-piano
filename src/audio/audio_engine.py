"""
audio_engine.py

Loads the generated note samples and plays them through pygame's mixer,
respecting the configured volume and polyphony (max simultaneous voices).
"""

from __future__ import annotations

from pathlib import Path

import pygame

from src.core.config import AudioConfig

ASSETS_DIR = Path(__file__).resolve().parents[2] / "assets" / "audio" / "notes"


def _safe_note_name(note: str) -> str:
    return note.replace("#", "s")


class AudioEngine:
    """Loads note samples once and plays them back on demand."""

    def __init__(self, config: AudioConfig) -> None:
        self.config = config

        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=44100, size=-16, channels=1)

        pygame.mixer.set_num_channels(max(config.polyphony, 8))

        self._sounds: dict[str, pygame.mixer.Sound] = {}
        self._load_sounds()

    def _load_sounds(self) -> None:
        if not ASSETS_DIR.exists():
            return

        for wav_path in ASSETS_DIR.glob("*.wav"):
            sound = pygame.mixer.Sound(str(wav_path))
            sound.set_volume(self.config.volume)
            self._sounds[wav_path.stem] = sound

    def play(self, note: str, octave: int) -> None:
        """Play the given note (e.g. 'C#') at the given octave."""

        key = f"{_safe_note_name(note)}{octave}"
        sound = self._sounds.get(key)

        if sound is None:
            return

        sound.set_volume(self.config.volume)
        sound.play()

    def stop_all(self) -> None:
        pygame.mixer.stop()
