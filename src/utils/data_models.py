"""
Shared data models used throughout the project.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Point:
    """Normalized 2D point."""

    x: float
    y: float


@dataclass(slots=True)
class Landmark:
    """Single MediaPipe landmark."""

    position: Point
    z: float


@dataclass(slots=True)
class Hand:
    """Represents one detected hand."""

    handedness: str
    confidence: float
    landmarks: list[Landmark]

    @property
    def thumb_tip(self) -> Landmark:
        return self.landmarks[4]

    @property
    def index_tip(self) -> Landmark:
        return self.landmarks[8]

    @property
    def middle_tip(self) -> Landmark:
        return self.landmarks[12]

    @property
    def ring_tip(self) -> Landmark:
        return self.landmarks[16]

    @property
    def pinky_tip(self) -> Landmark:
        return self.landmarks[20]

    @property
    def fingertips(self) -> list[Landmark]:
        return [
            self.thumb_tip,
            self.index_tip,
            self.middle_tip,
            self.ring_tip,
            self.pinky_tip,
        ]