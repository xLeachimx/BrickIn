# File: menus.py
# Project: BrickIn
# Author: Michael Huelsman
# Copyright: Dr. Michael Andrew Huelsman 2023
# License: GNU GPLv3
# Date: 20 Dec 2023
# Purpose:
#   A set of scene classes for handling the menus of BrickIn
# Notes:
import pygame as pg

from scene import Scene
import level
from user_interface import Label, Button, CompoundUIElement
from typing import Type
import pygame as pg
from leaderboard import Leaderboard


class MainMenu(Scene):
    __PLAY = 1
    __QUIT = -1
    __LEADERBOARD = 2

    def __init__(self):
        self.title_label = Label("BRICK IN", Label.GIANT_TEXT, (250, 0, 0))
        self.play_button = Button("Start", Label.LARGE_TEXT, padding=5)
        self.leaderboard_button = Button("High Scores", Label.LARGE_TEXT, padding=5)
        self.quit_button = Button("Exit", Label.LARGE_TEXT, padding=5)
        self.compound = CompoundUIElement([self.title_label, self.play_button, self.leaderboard_button, self.quit_button])
        self.active = True
        self.selection = 0

    def update(self, delta: float) -> None:
        for event in pg.event.get(pg.MOUSEBUTTONDOWN):
            if event.button == pg.BUTTON_LEFT:
                press_pos = event.pos[0] - self.compound.pos[0], event.pos[1] - self.compound.pos[1]
                if self.play_button.inside(press_pos):
                    self.selection = MainMenu.__PLAY
                elif self.quit_button.inside(press_pos):
                    self.selection = MainMenu.__QUIT
                elif self.leaderboard_button.inside(press_pos):
                    self.selection = MainMenu.__LEADERBOARD
        for event in pg.event.get(pg.MOUSEMOTION):
            mouse_pos = event.pos[0] - self.compound.pos[0], event.pos[1] - self.compound.pos[1]
            if self.play_button.inside(mouse_pos):
                self.play_button.highlight(True)
            else:
                self.play_button.highlight(False)
            if self.quit_button.inside(mouse_pos):
                self.quit_button.highlight(True)
            else:
                self.quit_button.highlight(False)
            if self.leaderboard_button.inside(mouse_pos):
                self.leaderboard_button.highlight(True)
            else:
                self.leaderboard_button.highlight(False)

    def draw(self, screen: pg.Surface) -> None:
        self.compound.center((screen.get_width(), screen.get_height()))
        self.compound.draw(screen)

    def finished(self) -> bool:
        return self.selection != 0

    def next_scene(self) -> Scene | None:
        if self.selection == MainMenu.__PLAY:
            return DifficultyMenu()
        elif self.selection == MainMenu.__LEADERBOARD:
            return LeaderboardDisplay()
        return None


class DifficultyMenu(Scene):
    __EASY = 1
    __MEDIUM = 2
    __HARD = 3

    def __init__(self):
        self.easy_btn = Button("EASY", Label.LARGE_TEXT, padding=10)
        self.med_btn = Button("MEDIUM", Label.LARGE_TEXT, padding=10)
        self.hard_btn = Button("HARD", Label.LARGE_TEXT, padding=10)
        self.btns = [self.easy_btn, self.med_btn, self.hard_btn]
        self.compound = CompoundUIElement(self.btns)
        self.active = True
        self.selection = 0

    def update(self, delta: float) -> None:
        for event in pg.event.get(pg.MOUSEBUTTONDOWN):
            if event.button == pg.BUTTON_LEFT:
                press_pos = event.pos[0] - self.compound.pos[0], event.pos[1] - self.compound.pos[1]
                if self.easy_btn.inside(press_pos):
                    self.selection = DifficultyMenu.__EASY
                elif self.med_btn.inside(press_pos):
                    self.selection = DifficultyMenu.__MEDIUM
                elif self.hard_btn.inside(press_pos):
                    self.selection = DifficultyMenu.__HARD
        for event in pg.event.get(pg.MOUSEMOTION):
            mouse_pos = event.pos[0] - self.compound.pos[0], event.pos[1] - self.compound.pos[1]
            for btn in self.btns:
                if btn.inside(mouse_pos):
                    btn.highlight(True)
                else:
                    btn.highlight(False)

    def draw(self, screen: pg.Surface) -> None:
        self.compound.center((screen.get_width(), screen.get_height()))
        self.compound.draw(screen)

    def finished(self) -> bool:
        return self.selection != 0

    def next_scene(self) -> Scene | None:
        if self.selection == DifficultyMenu.__EASY:
            return level.Level(level.Level.EASY)
        elif self.selection == DifficultyMenu.__MEDIUM:
            return level.Level(level.Level.MEDIUM)
        elif self.selection == DifficultyMenu.__HARD:
            return level.Level(level.Level.HARD)
        return None


class LeaderboardAdd(Scene):
    def __init__(self, score: int):
        self.name = ["A", "A", "A"]
        self.score = score
        self.active = Leaderboard.check(self.score)
        name_str = "".join(self.name)
        self.label_str = f"{name_str}     {self.score:09d}"
        self.label = Label(self.label_str, Label.LARGE_TEXT)
        self.underline = 0

    def update(self, delta: float) -> None:
        for event in pg.event.get(pg.KEYDOWN):
            if event.key == pg.K_DOWN:
                alt = chr(ord(self.name[self.underline]) - 1)
                if self.name[self.underline] == "A":
                    alt = "Z"
                self.name[self.underline] = alt
            elif event.key == pg.K_UP:
                alt = chr(ord(self.name[self.underline]) + 1)
                if self.name[self.underline] == "Z":
                    alt = "A"
                self.name[self.underline] = alt
            elif event.key == pg.K_LEFT:
                self.underline -= 1
                self.underline = self.underline % 3
            elif event.key == pg.K_RIGHT:
                self.underline += 1
                self.underline = self.underline % 3
            elif event.key == pg.K_RETURN:
                self.active = False
                Leaderboard.register("".join(self.name), self.score)

    def draw(self, screen: pg.Surface) -> None:
        name_str = "".join(self.name)
        self.label_str = f"{name_str}     {self.score:09d}"
        self.label = Label(self.label_str, Label.LARGE_TEXT)
        self.label.center((screen.get_width(), screen.get_height()))
        self.label.draw(screen)

    def finished(self) -> bool:
        return not self.active

    def next_scene(self) -> 'Scene':
        return MainMenu()


class LeaderboardDisplay(Scene):
    def __init__(self):
        self.labels = []
        self.active = True
        for name, score in Leaderboard.get_scores():
            scr_str = f"{name}     {score:09d}"
            self.labels.append(Label(scr_str, Label.MEDIUM_TEXT))
        self.compound = CompoundUIElement(self.labels)

    def update(self, delta: float) -> None:
        for event in pg.event.get(pg.KEYDOWN):
            if event.key == pg.K_ESCAPE:
                self.active = False

    def draw(self, screen: pg.Surface) -> None:
        self.compound.center((screen.get_width(), screen.get_height()))
        self.compound.draw(screen)

    def finished(self) -> bool:
        return not self.active

    def next_scene(self) -> 'Scene':
        return MainMenu()
