"""
keyboard.py

Circular ring keyboard.
"""

from __future__ import annotations
from src.piano.piano_key import PianoKey

import math

import pygame


class CircularKeyboard:

    def __init__(
        self,
        center: tuple[int, int],
        outer_radius: int,
        inner_radius: int,
        sectors: int = 12,
        octave: int = 4,
    ) -> None:

        self.center = center

        self.outer_radius = outer_radius
        self.inner_radius = inner_radius

        self.sectors = sectors
        self.octave = octave

        self.rotation = -90
        notes = [
            "C",
            "C#",
            "D",
            "D#",
            "E",
            "F",
            "F#",
            "G",
            "G#",
            "A",
            "A#",
            "B",
        ]

        self.keys = []

        angle_step = 360 / self.sectors

        for i, note in enumerate(notes):

            self.keys.append(

                PianoKey(

                    note,

                    self.rotation + i * angle_step,

                    self.rotation + (i + 1) * angle_step,

                )

            )

    def update(self):

        for key in self.keys:

            if not key.pressed:

                key.animation *= 0.90

    def get_key_at(
        self,
        point: tuple[int, int],
    ):
            """
            Return the PianoKey currently under the given point.

            Returns None if the point is outside the keyboard.
            """

            px, py = point

            cx, cy = self.center

            dx = px - cx
            dy = py - cy

            distance = math.hypot(dx, dy)

            # Outside the ring?
            if (
                distance < self.inner_radius
                or distance > self.outer_radius
            ):
                return None

            angle = math.degrees(
                math.atan2(dy, dx)
            )

            angle = (angle + 360) % 360

            angle = (angle - self.rotation) % 360

            sector_size = 360 / self.sectors

            index = int(angle // sector_size)

            return self.keys[index]