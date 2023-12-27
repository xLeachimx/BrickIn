# File: main.py
# Author: Michael Huelsman
# Copyright: Dr. Michael Andrew Huelsman 2023
# License: GNU GPLv3
# Created On: 14 Dec 2023
# Purpose:
#   Main game loop for BrickIn
# Notes:

import pygame as pg
from time import perf_counter
from game_config import GameConfig
from asset_manager import AssetManager
from scene import Scene
from level import Level
from menus import MainMenu
from leaderboard import Leaderboard


def main():
    pg.init()
    # Setup some baseline info.
    GameConfig.create()
    GameConfig.add_value("fps", 60)
    GameConfig.add_value("frame_delta", 1/GameConfig.get_value("fps"))
    disp_info = pg.display.Info()
    window_width = 700
    window_height = window_width * (disp_info.current_h/disp_info.current_w)
    GameConfig.add_value("screen_dim", (window_width, window_height))
    # Setup assets
    AssetManager.create()
    prim_font_giant = pg.font.SysFont("Impact", 60)
    prim_font_large = pg.font.SysFont("Impact", 40)
    prim_font_medium = pg.font.SysFont("Impact", 28)
    prim_font_small = pg.font.SysFont("Impact", 18)
    AssetManager.get_instance().register_font("primary-giant", prim_font_giant)
    AssetManager.get_instance().register_font("primary-large", prim_font_large)
    AssetManager.get_instance().register_font("primary-medium", prim_font_medium)
    AssetManager.get_instance().register_font("primary-small", prim_font_small)
    # Setup pygame
    screen_surf = pg.display.set_mode(GameConfig.get_value("screen_dim"), flags=pg.SCALED | pg.FULLSCREEN)
    pg.display.set_caption("BrickIn", "BrickIn")
    pg.display.set_icon(pg.Surface((32, 32)))
    frame_timer = perf_counter()
    running = True
    current_scene = MainMenu()
    while running:
        frame_delta = perf_counter() - frame_timer
        if frame_delta >= GameConfig.get_value("frame_delta"):
            frame_timer = perf_counter()
            screen_surf.fill((0, 0, 0))
            if current_scene is not None:
                if not current_scene.finished():
                    # Update Scene
                    current_scene.update(frame_delta)
                    current_scene.draw(screen_surf)
                else:
                    current_scene = current_scene.next_scene()
                    if current_scene is None:
                        running = False
            for event in pg.event.get(pg.QUIT):
                running = False
            pg.display.flip()
    # Close everything
    pg.quit()
    Leaderboard.quit()
    

if __name__ == '__main__':
    main()