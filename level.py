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


class Level(Scene):
    
    def __init__(self, difficulty: int):
        """
        Creates a level scene with the given difficulty.
        Difficulty must be either 1, 2, or 3 (easy, med, hard.)
        Difficulty will default to 3 or 1, whichever is closer.
        """
        difficulty = max(min(3, difficulty), 1)
        self.diff = difficulty
        vert_spread = 0.3
        brick_prob = 0.3
        ball_speed = 100
        if difficulty == 2:
            ball_speed = 150
            brick_prob = 0.5
        elif difficulty == 3:
            ball_speed = 250
            vert_spread = 0.5
            brick_prob = 1
        brick_padding = 1
        scr_dim = GameConfig.get_value("screen_dim")
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

    def update(self, delta: float) -> None:
        self.ball.update(delta)
        self.paddle.update(delta)
        # Brick Collision check
        colliding_brick = self.ball.get_rect().collideobjects(self.bricks, key=lambda x: x.get_rect())
        if colliding_brick is not None:
            if colliding_brick.intact:
                colliding_brick.hit()
                # Deal with reflection
                center_diff = colliding_brick.get_center() - self.ball.get_center()
                if center_diff.x() * self.ball.velocity.x() > 0 and center_diff.y() * self.ball.velocity.y() > 0:
                    if center_diff.x() * (Brick.BRICK_HEIGHT/Brick.BRICK_WIDTH) < center_diff.y():
                        self.ball.velocity.set_x(-self.ball.velocity.x())
                    else:
                        self.ball.velocity.set_y(-self.ball.velocity.y())
                elif center_diff.x() * self.ball.velocity.x() > 0:
                    self.ball.velocity.set_x(-self.ball.velocity.x())
                else:
                    self.ball.velocity.set_y(-self.ball.velocity.y())
        # Paddle Collision check
        if self.ball.get_rect().colliderect(self.paddle.get_rect()):
            self.ball.velocity.set_y(-self.ball.velocity.y())
            self.ball.pos = self.ball.pos.to_mutable().set_y(self.paddle.pos.y() - (Ball.BALL_HEIGHT+1)).to_immutable()
        
    def draw(self, screen: pg.Surface) -> None:
        for brick in self.bricks:
            brick.draw(screen)
        self.ball.draw(screen)
        self.paddle.draw(screen)

    def finished(self) -> bool:
        if self.ball.pos.y() > (self.paddle.pos.y() + Paddle.PADDLE_HEIGHT):
            return True
        return False

    def next_scene(self) -> Scene:
        return Level(self.diff)
    