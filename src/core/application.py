"""
Main application.
"""

from __future__ import annotations

import pygame

from src.audio.audio_engine import AudioEngine
from src.camera.camera import Camera
from src.core.config import load_config
from src.core.constants import (
    BACKGROUND_COLOR,
    DEFAULT_FONT,
    TEXT_COLOR,
)
from src.graphics.renderer import Renderer
from src.tracking.hand_tracker import HandTracker
from src.piano.keyboard import CircularKeyboard


class Application:
    """Main application class."""

    def __init__(self) -> None:
        pygame.init()

        self.config = load_config()

        self.screen = pygame.display.set_mode(
            (
                self.config.window.width,
                self.config.window.height,
            )
        )

        pygame.display.set_caption(self.config.window.title)
        print(self.screen.get_size())

        self.clock = pygame.time.Clock()
        self.running = True

        self.background_color = BACKGROUND_COLOR
        self.text_color = TEXT_COLOR

        self.font = pygame.font.SysFont(DEFAULT_FONT, 28)

        # Camera
        self.camera = Camera(self.config.camera)
        self.camera.start()

        # Hand tracker
        self.hand_tracker = HandTracker()

        # Renderer
        self.renderer = Renderer(self.screen)

        # Audio
        self.audio_engine = AudioEngine(self.config.audio)

        self.left_keyboard = CircularKeyboard(
            center=(230, 360),
            outer_radius=150,
            inner_radius=90,
            octave=3,
        )

        self.right_keyboard = CircularKeyboard(
            center=(1050, 360),
            outer_radius=150,
            inner_radius=90,
            octave=4,
        )

    def run(self) -> None:
        """Main application loop."""

        while self.running:

            # ----------------------------
            # Handle Events
            # ----------------------------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # ----------------------------
            # Clear Screen
            # ----------------------------
            self.renderer.clear(self.background_color)

            # ----------------------------
            # Camera
            # ----------------------------
            frame = self.camera.get_frame()

            hands = []

            if frame is not None:

                # Detect hands
                hands = self.hand_tracker.detect(frame)
                # Reset hover state every frame
                for key in self.left_keyboard.keys:
                    key.hovered = False

                for key in self.right_keyboard.keys:
                    key.hovered = False
                if hands:

                    fingertip = hands[0].landmarks[8].position

                    x = int(fingertip.x * self.screen.get_width())
                    y = int(fingertip.y * self.screen.get_height())

                    for hand in hands:

                        fingertip = hand.landmarks[8].position

                        x = int(fingertip.x * self.screen.get_width())
                        y = int(fingertip.y * self.screen.get_height())

                        if hand.handedness == "Left":
                            keyboard = self.left_keyboard
                        else:
                            keyboard = self.right_keyboard

                        key = keyboard.get_key_at((x, y))

                        if key:
                             was_hovered = key.hovered
                             key.hovered = True

                             if not was_hovered:
                                 self.audio_engine.play(key.note, keyboard.octave)

                # TEMP DEBUG
                #if hands:
                   # print(
                      #  f"{len(hands)} hand(s):",
                      #  [hand.handedness for hand in hands],
                    #)
                # Draw camera
                self.renderer.draw_camera(
                    frame,
                    self.config.window.width,
                    self.config.window.height,
                )

                self.renderer.draw_hands(
                    hands,
                    self.hand_tracker.connections,
                )

                self.renderer.draw_keyboard(
                    self.left_keyboard, self.font
                )

                self.renderer.draw_keyboard(
                    self.right_keyboard, self.font
                )

                # Draw hands afterwards

            # ----------------------------
            # UI
            # ----------------------------
            fps = self.clock.get_fps()

            self.renderer.draw_text(
                self.config.window.title,
                self.font,
                self.text_color,
                (40, 40),
            )

            self.renderer.draw_text(
                f"FPS: {fps:.1f}",
                self.font,
                self.text_color,
                (40, 80)
            )

            # ----------------------------
            # Present
            # ----------------------------
            self.renderer.present()

            self.clock.tick(self.config.window.fps)

        # ----------------------------
        # Cleanup
        # ----------------------------
        self.hand_tracker.close()
        self.camera.stop()

        pygame.quit()