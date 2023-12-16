# File: scene.py
# Author: Michael Huelsman
# Copyright: Dr. Michael Andrew Huelsman 2023
# License: GNU GPLv3
# Created On: 14 Dec 2023
# Purpose:
#   An abstract base class for a game "scene."
# Notes:


from abc import ABC, abstractmethod
from typing import Any
import pygame as pg


class Scene(ABC):
    @abstractmethod
    def update(self, delta: float) -> None:
        """Function called once a frame, before drawing."""
        pass
    
    @abstractmethod
    def draw(self, screen: pg.Surface) -> None:
        """Function called once a frame, after updating."""
        pass
    
    @abstractmethod
    def finished(self) -> bool:
        """Returns true when the scene has ended."""
        pass
    
    @abstractmethod
    def next_scene(self) -> 'Scene':
        """Returns the next scene after this scene is finished."""
        pass
    