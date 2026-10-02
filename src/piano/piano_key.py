"""
piano_key.py

Represents one piano key on a circular keyboard.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class PianoKey:
    """Single ring sector."""

    note: str

    start_angle: float

    end_angle: float

    hovered: bool = False

    pressed: bool = False

    animation: float = 0.0

    base_color: tuple[int, int, int] = field(
        default=(255, 0, 0)
    )

    hover_color: tuple[int, int, int] = field(
        default=(90, 150, 255)
    )

    pressed_color: tuple[int, int, int] = field(
        default=(255, 180, 70)
    )

    @property
    def color(self):

        if self.pressed:
            return self.pressed_color

        if self.hovered:
            return self.hover_color

        return self.base_color