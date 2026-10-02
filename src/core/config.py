"""
Configuration loader.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json


@dataclass(slots=True)
class WindowConfig:
    title: str
    width: int
    height: int
    fps: int
    fullscreen: bool


@dataclass(slots=True)
class CameraConfig:
    index: int
    mirror: bool


@dataclass(slots=True)
class KeyboardConfig:
    radius: int
    gap: int
    keys: int


@dataclass(slots=True)
class AudioConfig:
    volume: float
    polyphony: int


@dataclass(slots=True)
class DebugConfig:
    show_fps: bool
    show_camera: bool


@dataclass(slots=True)
class Config:
    window: WindowConfig
    camera: CameraConfig
    keyboard: KeyboardConfig
    audio: AudioConfig
    debug: DebugConfig


def load_config() -> Config:
    root = Path(__file__).resolve().parents[2]
    config_path = root / "config" / "settings.json"

    with config_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return Config(
        window=WindowConfig(**data["window"]),
        camera=CameraConfig(**data["camera"]),
        keyboard=KeyboardConfig(**data["keyboard"]),
        audio=AudioConfig(**data["audio"]),
        debug=DebugConfig(**data["debug"]),
    )