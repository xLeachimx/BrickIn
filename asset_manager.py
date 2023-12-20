# File: asset_manager.py
# Author: Michael Huelsman
# Copyright: Dr. Michael Andrew Huelsman 2023
# License: GNU GPLv3
# Created On: 28 Nov 2023
# Purpose:
#   A simple singleton class for handling various assets such as sfx and music.
# Notes:
#   Currently only handles sounds

import pygame as pg


class AssetManager:
    """Singleton class for handling assets"""
    __INSTANCE = None
    
    # Singleton methods
    @staticmethod
    def create() -> 'AssetManager':
        AssetManager.__INSTANCE = AssetManager()
        return AssetManager.__INSTANCE
    
    @staticmethod
    def get_instance() -> 'AssetManager':
        if AssetManager.__INSTANCE is None:
            return AssetManager.create()
        return AssetManager.__INSTANCE
    
    @staticmethod
    def destroy():
        AssetManager.__INSTANCE = None
    
    def __init__(self):
        self.sound_dict = {}
        self.music_dict = {}
        self.font_dict = {}
    
    def get_sound(self, name: str) -> pg.mixer.Sound:
        """Retrieves a Pygame sound object based on a registered name."""
        return self.sound_dict[name] if name in self.sound_dict else None
    
    def register_sound(self, name: str, filename: str) -> bool:
        """Registers a new sound file under a given name in the sound library, returns false if this would overwrite."""
        if name in self.sound_dict:
            return False
        self.sound_dict[name] = pg.mixer.Sound(filename)
        return True
        
    def get_music(self, name: str) -> str:
        """Retrieves a filename for music based on a registered name."""
        return self.music_dict[name] if name in self.music_dict else None
    
    def register_music(self, name: str, filename: str) -> bool:
        """Registers a new music filename under a given name in the music library, returns false if this would overwrite."""
        if name in self.music_dict:
            return False
        self.music_dict[name] = filename
        return True

    def get_font(self, name: str) -> pg.font.Font:
        """Retrieves a Font object based on a registered name."""
        return self.font_dict[name] if name in self.font_dict else None

    def register_font(self, name: str, font: pg.font.Font) -> bool:
        """Registers a new Font under a given name in the music library, returns false if this would overwrite."""
        if name in self.font_dict:
            return False
        self.font_dict[name] = font
        return True