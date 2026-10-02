"""
camera.py

Camera abstraction built on top of OpenCV.

Responsibilities
----------------
- Open and configure the webcam
- Read frames
- Mirror frames (optional)
- Convert BGR -> RGB
- Cleanly release resources

The rest of the application should never call cv2.VideoCapture()
directly. It should interact only with this class.
"""

from __future__ import annotations

from typing import Optional

import cv2
import numpy as np

from src.core.config import CameraConfig


class Camera:
    """Webcam manager."""

    def __init__(self, config: CameraConfig) -> None:
        self._config = config

        self._capture: Optional[cv2.VideoCapture] = None
        self._is_running = False

    @property
    def is_running(self) -> bool:
        """Return True if the camera is active."""
        return self._is_running

    def start(self) -> None:
        """Open the webcam."""

        if self._is_running:
            return

        self._capture = cv2.VideoCapture(self._config.index)

        if not self._capture.isOpened():
            raise RuntimeError(
                f"Unable to open camera {self._config.index}"
            )

        self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        self._is_running = True

    def stop(self) -> None:
        """Release the webcam."""

        if self._capture is not None:
            self._capture.release()

        self._capture = None
        self._is_running = False

    def get_frame(self) -> Optional[np.ndarray]:
        """
        Capture one frame.

        Returns
        -------
        np.ndarray | None
            RGB image or None if capture failed.
        """

        if not self._is_running:
            return None

        assert self._capture is not None

        success, frame = self._capture.read()

        if not success:
            return None

        if self._config.mirror:
            frame = cv2.flip(frame, 1)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        return frame

    def __enter__(self) -> "Camera":
        """Context manager support."""
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        """Context manager cleanup."""
        self.stop()