"""
MediaPipe hand tracking wrapper.

This module isolates MediaPipe from the rest of the application.
The rest of the project only communicates through the HandTracker
class and our own data models.
"""

from __future__ import annotations

from typing import Final

import mediapipe as mp
import numpy as np

from src.utils.data_models import Hand, Landmark, Point


class HandTracker:
    """High-level wrapper around MediaPipe Hands."""

    MAX_HANDS: Final[int] = 2

    def __init__(
        self,
        max_num_hands: int = 2,
        min_detection_confidence: float = 0.7,
        min_tracking_confidence: float = 0.7,
    ) -> None:
        """Create the MediaPipe hand tracker."""

        self._mp_hands = mp.solutions.hands

        self._hands = self._mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_num_hands,
            model_complexity=1,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

    @property
    def connections(self):
        """Return the MediaPipe hand connection graph."""
        return self._mp_hands.HAND_CONNECTIONS

    def detect(self, frame: np.ndarray) -> list[Hand]:
        """
        Detect hands inside an RGB frame.

        Parameters
        ----------
        frame:
            RGB frame from the camera.

        Returns
        -------
        list[Hand]
            List containing every detected hand.
        """

        results = self._hands.process(frame)

        detected_hands: list[Hand] = []

        if (
            results.multi_hand_landmarks is None
            or results.multi_handedness is None
        ):
            return detected_hands

        for hand_landmarks, handedness in zip(
            results.multi_hand_landmarks,
            results.multi_handedness,
        ):

            hand_points: list[Landmark] = []

            for landmark in hand_landmarks.landmark:

                point = Point(
                    x=landmark.x,
                    y=landmark.y,
                )

                hand_points.append(
                    Landmark(
                        position=point,
                        z=landmark.z,
                    )
                )

            detected_hands.append(
                Hand(
                    handedness=handedness.classification[0].label,
                    confidence=handedness.classification[0].score,
                    landmarks=hand_points,
                )
            )

        return detected_hands

    def close(self) -> None:
        """Release MediaPipe resources."""
        self._hands.close()