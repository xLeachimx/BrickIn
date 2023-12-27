# File: game_config.py
# Author: Michael Huelsman
# Copyright: Dr. Michael Andrew Huelsman 2023
# License: GNU GPLv3
# Created On: 14 Dec 2023
# Purpose:
#   A "singleton" for holding general game configuration information.
# Notes:

import pygame as pg


class GameConfig:
    """A wrapped dictionary for holding global game configuration info."""
    __config = {}

    @staticmethod
    def create():
        GameConfig.__config = {'controller': "KEYBOARD"}
        GameConfig.__detect_snes_gamepad()
    
    @staticmethod
    def add_value(name, value):
        """Adds a named value to the config dictionary."""
        GameConfig.__config[name] = value
        return value
    
    @staticmethod
    def get_value(name):
        """Gets a named value from the config dictionary."""
        if name in GameConfig.__config:
            return GameConfig.__config[name]
        return None

    @staticmethod
    def __detect_snes_gamepad():
        """Checks for and registers a Vilros USB SNES gamepad in the configuration."""
        if not pg.joystick.get_init():
            pg.joystick.init()
        if pg.joystick.get_count() == 0:
            return
        for i in range(pg.joystick.get_count()):
            stick = pg.joystick.Joystick(i)
            stick.init()
            if stick.get_name() == 'USB Gamepad':
                GameConfig.__config['controller'] = "GAMEPAD"
                GameConfig.__config['gamepad'] = stick
                GameConfig.__config['X'] = 0
                GameConfig.__config['A'] = 1
                GameConfig.__config['B'] = 2
                GameConfig.__config['Y'] = 3
                GameConfig.__config['L'] = 4
                GameConfig.__config['R'] = 5
                GameConfig.__config['SELECT'] = 8
                GameConfig.__config['START'] = 9
                GameConfig.__config['X-axis'] = 0
                GameConfig.__config['Y-axis'] = 4
                break
            stick.quit()
    