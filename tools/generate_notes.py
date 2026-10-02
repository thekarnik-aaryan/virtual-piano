"""
generate_notes.py

Synthesizes simple piano-like note samples (additive harmonics + ADSR
envelope) and writes them as 16-bit PCM WAV files under assets/audio/notes/.
Run once; the project ships with the generated files so this is not
needed at runtime.
"""

from __future__ import annotations

import math
import struct
import wave
from pathlib import Path

SAMPLE_RATE = 44100
DURATION = 1.6  # seconds
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# Harmonic amplitudes (fundamental + overtones) -> gives a warmer,
# less "beepy" tone than a pure sine wave.
HARMONICS = [(1.0, 1.0), (2.0, 0.55), (3.0, 0.30), (4.0, 0.18), (5.0, 0.10)]

OUT_DIR = Path(__file__).resolve().parents[1] / "assets" / "audio" / "notes"


def note_frequency(note_index_from_a4: int) -> float:
    """A4 = 440Hz reference, 12-tone equal temperament."""
    return 440.0 * (2.0 ** (note_index_from_a4 / 12.0))


def adsr(n_samples: int) -> list[float]:
    attack = int(0.01 * SAMPLE_RATE)
    decay = int(0.15 * SAMPLE_RATE)
    release_start = int(n_samples * 0.55)
    env = [0.0] * n_samples

    for i in range(n_samples):
        if i < attack:
            env[i] = i / max(attack, 1)
        elif i < attack + decay:
            t = (i - attack) / max(decay, 1)
            env[i] = 1.0 - 0.35 * t
        elif i < release_start:
            env[i] = 0.65
        else:
            t = (i - release_start) / max(n_samples - release_start, 1)
            env[i] = 0.65 * (1.0 - t)

    return env


def synth_note(freq: float) -> bytes:
    n_samples = int(SAMPLE_RATE * DURATION)
    env = adsr(n_samples)
    samples = bytearray()

    for i in range(n_samples):
        t = i / SAMPLE_RATE
        value = 0.0
        for harmonic_mult, amp in HARMONICS:
            value += amp * math.sin(2 * math.pi * freq * harmonic_mult * t)
        value *= env[i]
        value *= 0.28  # headroom so summed harmonics don't clip
        sample = max(-1.0, min(1.0, value))
        samples += struct.pack("<h", int(sample * 32767))

    return bytes(samples)


def write_wav(path: Path, pcm_data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(pcm_data)


def main() -> None:
    # C4 is 9 semitones below A4.
    c4_offset = -9

    for octave in (3, 4):
        octave_offset = (octave - 4) * 12
        for i, name in enumerate(NOTE_NAMES):
            semitones_from_a4 = c4_offset + i + octave_offset
            freq = note_frequency(semitones_from_a4)
            pcm = synth_note(freq)
            safe_name = name.replace("#", "s")
            out_path = OUT_DIR / f"{safe_name}{octave}.wav"
            write_wav(out_path, pcm)
            print(f"wrote {out_path.name} ({freq:.2f} Hz)")


if __name__ == "__main__":
    main()
