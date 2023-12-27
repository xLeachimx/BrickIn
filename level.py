# File: level.py
# Author: Michael Huelsman
# Copyright: Dr. Michael Andrew Huelsman 2023
# License: GNU GPLv3
# Created On: 14 Dec 2023
# Purpose:
#   A scene class for creating and running a level of BrickIn
# Notes:
from typing import Any
import pygame as pg
from scene import Scene
from game_objects import Ball, Brick, Paddle
from vector_2d import Vector2D
from game_config import GameConfig
from random import random
from asset_manager import AssetManager
import menus as menu
from user_interface import Label


class Level(Scene):
    EASY = 1
    MEDIUM = 2
    HARD = 3

    def __init__(self, difficulty: int, score: int = 0):
        """
        Creates a level scene with the given difficulty.
        Difficulty must be either 1, 2, or 3 (easy, med, hard.)
        Difficulty will default to 3 or 1, whichever is closer.
        """
        difficulty = max(min(3, difficulty), 1)
        self.diff = difficulty
        self.win = False
        self.score = score
        self.lives = 3
        self.paused = False
        vert_spread = 0.3
        brick_prob = 0.3
        ball_speed = 75
        if difficulty == 2:
            ball_speed = 150
            brick_prob = 0.5
        elif difficulty == 3:
            ball_speed = 200
            vert_spread = 0.5
            brick_prob = 1
        brick_padding = 1
        scr_dim = GameConfig.get_value("screen_dim")
        self.font = AssetManager.get_instance().get_font("primary-small")
        self.ball = Ball(Vector2D(scr_dim[0]//2, scr_dim[1] - 100), ball_speed, scr_dim)
        self.bricks = []
        horz_bricks = (scr_dim[0] // (Brick.BRICK_WIDTH+3)) - 1
        horz_start = (scr_dim[0] - (horz_bricks * (Brick.BRICK_WIDTH+brick_padding)))//2
        vert_bricks = int(vert_spread * scr_dim[1])
        vert_bricks = vert_bricks // (Brick.BRICK_HEIGHT+3)
        vert_start = int(scr_dim[1] * 0.1)
        for i in range(horz_bricks):
            for j in range(vert_bricks):
                if random() < brick_prob:
                    x = horz_start + i*(Brick.BRICK_WIDTH + brick_padding)
                    y = vert_start + j*(Brick.BRICK_HEIGHT + brick_padding)
                    self.bricks.append(Brick(Vector2D(x, y)))
        paddle_pos = Vector2D((scr_dim[0]-Paddle.PADDLE_WIDTH)//2, scr_dim[1] - 3*Paddle.PADDLE_HEIGHT)
        self.paddle = Paddle(paddle_pos, self.ball)
        # Pause label
        self.pause_label = Label("PAUSED", Label.GIANT_TEXT, (250, 0, 250))

    def update(self, delta: float) -> None:
        if GameConfig.get_value("controller") == "KEYBOARD":
            for event in pg.event.get(pg.KEYDOWN):
                if event.key == pg.K_SPACE:
                    self.ball.launch()
                elif event.key == pg.K_ESCAPE:
                    self.paused = not self.paused
        elif GameConfig.get_value("controller") == "GAMEPAD":
            for event in pg.event.get(pg.JOYBUTTONDOWN):
                if event.button == GameConfig.get_value("A"):
                    self.ball.launch()
                elif event.button == GameConfig.get_value("START"):
                    self.paused = not self.paused
        if not self.paused:
            self.ball.update()
            self.paddle.update()
            # Brick Collision check
            bounce_x = False
            bounce_y = False
            colliding_bricks = self.ball.get_rect().collideobjectsall(self.bricks, key=lambda x: x.get_rect())
            for colliding_brick in colliding_bricks:
                if colliding_brick is not None:
                    if colliding_brick.intact:
                        self.score += 100
                        colliding_brick.hit()
                        # Deal with reflection
                        if not self.ball.last_vertical_rect().colliderect(colliding_brick.get_rect()):
                            bounce_y = True
                        elif not self.ball.last_horizontal_rect().colliderect(colliding_brick.get_rect()):
                            bounce_x = True
            if bounce_x:
                self.ball.velocity.set_x(-self.ball.velocity.x())
            if bounce_y:
                self.ball.velocity.set_y(-self.ball.velocity.y())
            # Paddle Collision check
            if self.ball.get_rect().colliderect(self.paddle.get_rect()):
                self.ball.velocity.set_y(-self.ball.velocity.y())
                self.ball.pos = self.ball.pos.to_mutable().set_y(self.paddle.pos.y() - (Ball.BALL_HEIGHT+1)).to_immutable()
            # Fall below paddle check
            if self.ball.pos.y() + Ball.BALL_HEIGHT > (self.paddle.pos.y() + Paddle.PADDLE_HEIGHT):
                self.lives -= 1
                self.ball.reset()
        
    def draw(self, screen: pg.Surface) -> None:
        for brick in self.bricks:
            brick.draw(screen)
        self.ball.draw(screen)
        self.paddle.draw(screen)
        score_str = f"{self.score:09d}"
        score = self.font.render(score_str, True, (255, 255, 255))
        # Display Score
        screen.blit(score, (screen.get_width() - score.get_width(), 0))
        padding = screen.get_height()//100
        lives_str = self.font.render("Lives:", True, (255, 255, 255))
        ball_size = lives_str.get_height()//4
        ball_x = padding + ball_size//2
        ball_y = padding + lives_str.get_height()
        screen.blit(lives_str, (padding, padding))
        for i in range(self.lives):
            pg.draw.rect(screen, (255, 255, 255), (ball_x, ball_y, ball_size, ball_size))
            ball_x += (3*ball_size)//2
        if self.paused:
            self.pause_label.center((screen.get_width(), screen.get_height()))
            self.pause_label.draw(screen)

    def finished(self) -> bool:
        if self.lives <= 0:
            self.win = False
            return True
        self.win = True
        for brick in self.bricks:
            if brick.intact:
                self.win = False
                return False
        return True

    def next_scene(self) -> Scene:
        if self.win:
            return Level(self.diff, self.score)
        return menu.LeaderboardAdd(self.score)
    