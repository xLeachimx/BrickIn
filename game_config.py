# File: game_config.py
# Author: Michael Huelsman
# Copyright: Dr. Michael Andrew Huelsman 2023
# License: GNU GPLv3
# Created On: 14 Dec 2023
# Purpose:
#   A "singleton" for holding general game configuration information.
# Notes:


class GameConfig:
    """A wrapped dictionary for holding global game configuration info."""
    __config = {}
    
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
    