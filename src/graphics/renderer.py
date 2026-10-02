"""
renderer.py

Rendering engine for Virtual Piano Hands.
"""

from __future__ import annotations

from typing import Tuple

import numpy as np
import pygame
import math

from src.utils.data_models import Hand


Color = Tuple[int, int, int]
Point = Tuple[int, int]


LEFT_HAND_COLOR = (80, 170, 255)
RIGHT_HAND_COLOR = (100, 255, 100)

FINGERTIP_COLOR = (255, 90, 90)


class Renderer:

    def __init__(self, screen: pygame.Surface):

        self._screen = screen

    @property
    def screen(self):

        return self._screen

    def clear(self, color: Color):

        self._screen.fill(color)

    def present(self):

        pygame.display.flip()

    def draw_camera(
        self,
        frame: np.ndarray,
        width: int,
        height: int,
    ):

        surface = pygame.image.frombuffer(
            frame.tobytes(),
            frame.shape[1::-1],
            "RGB",
        )

        surface = pygame.transform.scale(
            surface,
            (width, height),
        )

        self._screen.blit(surface, (0, 0))

    def draw_text(
        self,
        text: str,
        font: pygame.font.Font,
        color: Color,
        position: Point,
    ):

        rendered = font.render(text, True, color)

        self._screen.blit(
            rendered,
            position,
        )

    def draw_circle(
        self,
        center: Point,
        radius: int,
        color: Color,
        width: int = 0,
    ):

        pygame.draw.circle(
            self._screen,
            color,
            center,
            radius,
            width,
        )

    def draw_line(
        self,
        start: Point,
        end: Point,
        color: Color,
        width: int = 2,
    ):

        pygame.draw.line(
            self._screen,
            color,
            start,
            end,
            width,
        )
    
    def draw_keyboard(self, keyboard, font: pygame.font.Font | None = None) -> None:
        """Draw an entire circular keyboard."""

        for key in keyboard.keys:
            self.draw_ring_sector(
                keyboard.center,
                keyboard.inner_radius,
                keyboard.outer_radius,
                key.start_angle,
                key.end_angle,
                key.color,
            )

            if font is not None:
                self._draw_key_label(
                    keyboard.center,
                    keyboard.inner_radius,
                    keyboard.outer_radius,
                    key.start_angle,
                    key.end_angle,
                    key.note,
                    font,
                )

    def _draw_key_label(
        self,
        center,
        inner_radius,
        outer_radius,
        start_angle,
        end_angle,
        note,
        font,
    ):
        """Draw the note name centered in a ring sector, in black."""

        cx, cy = center
        mid_angle = math.radians((start_angle + end_angle) / 2)
        mid_radius = (inner_radius + outer_radius) / 2

        x = cx + mid_radius * math.cos(mid_angle)
        y = cy + mid_radius * math.sin(mid_angle)

        rendered = font.render(note, True, (0, 0, 0))
        rect = rendered.get_rect(center=(x, y))
        self._screen.blit(rendered, rect)

    def draw_ring_sector(
        self,
        center,
        inner_radius,
        outer_radius,
        start_angle,
        end_angle,
        color,
        alpha: int = 140,
    ):
        """Draw one translucent ring sector."""

        cx, cy = center

        points = []

        resolution = 18

        start = math.radians(start_angle)
        end = math.radians(end_angle)

    # Outer arc
        for i in range(resolution + 1):

            t = i / resolution
            angle = start + (end - start) * t

            x = cx + outer_radius * math.cos(angle)
            y = cy + outer_radius * math.sin(angle)

            points.append((x, y))

    # Inner arc
        for i in range(resolution, -1, -1):

            t = i / resolution
            angle = start + (end - start) * t

            x = cx + inner_radius * math.cos(angle)
            y = cy + inner_radius * math.sin(angle)

            points.append((x, y))

        overlay = pygame.Surface(self._screen.get_size(), pygame.SRCALPHA)

        pygame.draw.polygon(
            overlay,
            (*color[:3], alpha),
            points,
        )

        pygame.draw.polygon(
            overlay,
            (150, 150, 150, 200),
            points,
            2,
        )

        self._screen.blit(overlay, (0, 0))

    # -------------------------------------------------------


    def _pixel(
        self,
        x: float,
        y: float,
    ) -> Point:

        width = self._screen.get_width()
        height = self._screen.get_height()

        return (
            int(x * width),
            int(y * height),
        )

    # -------------------------------------------------------

    def draw_hand(
        self,
        hand: Hand,
        connections,
    ):

        color = (
            LEFT_HAND_COLOR
            if hand.handedness == "Left"
            else RIGHT_HAND_COLOR
        )

        # Draw Bones

        for start, end in connections:

            start_point = hand.landmarks[start].position
            end_point = hand.landmarks[end].position

            self.draw_line(
                self._pixel(
                    start_point.x,
                    start_point.y,
                ),
                self._pixel(
                    end_point.x,
                    end_point.y,
                ),
                color,
                3,
            )

        # Draw Landmarks

        for landmark in hand.landmarks:

            point = self._pixel(
                landmark.position.x,
                landmark.position.y,
            )

            self.draw_circle(
                point,
                5,
                color,
            )

        # Fingertips

        for tip in hand.fingertips:

            point = self._pixel(
                tip.position.x,
                tip.position.y,
            )

            self.draw_circle(
                point,
                8,
                FINGERTIP_COLOR,
            )

    # -------------------------------------------------------

    def draw_hands(
        self,
        hands: list[Hand],
        connections,
    ):

        for hand in hands:

            self.draw_hand(
                hand,
                connections,
            )