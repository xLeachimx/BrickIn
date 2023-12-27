# File: game_objects.py
# Author: Michael Huelsman
# Copyright: Dr. Michael Andrew Huelsman 2023
# License: GNU GPLv3
# Created On: 15 Dec 2023
# Purpose:
#   A series of classes for representing game objects.
# Notes:

from abc import abstractmethod
from vector_2d import Vector2D, Vector2DBuilder
from random import choice, random, randint
from game_config import GameConfig
import pygame as pg


class GameObject:
    """A class for representing game objects."""
    def __init__(self, pos: Vector2D):
        self.pos = pos
        
    @abstractmethod
    def draw(self, screen: pg.Surface):
        """Abstract method for drawing the object to screen."""
        pass
    
    @abstractmethod
    def update(self):
        """Abstract method for updating the object (called once per frame)"""
        pass
    
    @abstractmethod
    def get_rect(self) -> pg.Rect:
        pass
    
    @abstractmethod
    def get_center(self) -> Vector2D:
        pass


class Ball(GameObject):
    """A class for representing the breaking ball."""
    BALL_HEIGHT = 5
    BALL_WIDTH = 5

    def __init__(self, pos: Vector2D, speed: float, screen_dim: (int, int)):
        super().__init__(pos)
        self.launched = False
        self.color = pg.Color((255, 255, 255))
        self.velocity = Vector2DBuilder(choice([-1, 1]), -1)
        self.screen_dim = screen_dim
        self.speed = speed
        self.alive = True
        
    def is_alive(self):
        return self.alive
    
    def launch(self):
        self.launched = True
        
    def get_center(self):
        return self.pos + Vector2D(Ball.BALL_WIDTH//2, Ball.BALL_HEIGHT//2)
    
    def last_horizontal_rect(self):
        self.velocity.unit()
        delta = GameConfig.get_value("frame_delta")
        temp_pos = self.pos - (self.velocity.to_immutable().extract_x() * delta * self.speed)
        return pg.Rect(*temp_pos.to_tuple(), Ball.BALL_WIDTH, Ball.BALL_HEIGHT)
    
    def last_vertical_rect(self):
        self.velocity.unit()
        delta = GameConfig.get_value("frame_delta")
        temp_pos = self.pos - (self.velocity.to_immutable().extract_y() * delta * self.speed)
        return pg.Rect(*temp_pos.to_tuple(), Ball.BALL_WIDTH, Ball.BALL_HEIGHT)

    def get_rect(self) -> pg.Rect:
        return pg.Rect(*self.pos.to_tuple(), Ball.BALL_WIDTH, Ball.BALL_HEIGHT)

    def draw(self, screen: pg.Surface):
        """Draw the Ball to the screen."""
        rect = (*self.pos.to_tuple(), Ball.BALL_WIDTH, Ball.BALL_HEIGHT)
        pg.draw.rect(screen, self.color, rect)
        
    def update(self):
        """Method for updating the ball (called once per frame)"""
        if not self.launched:
            return
        delta = GameConfig.get_value("frame_delta")
        if self.pos.y() + Ball.BALL_HEIGHT > self.screen_dim[1] and self.velocity.y() > 0:
            self.alive = False
        if self.alive:
            if self.pos.y() <= 0 and self.velocity.y() < 0:
                self.velocity.set_y(-self.velocity.y())
            if self.pos.x() < 0 and self.velocity.x() < 0 or \
                    self.pos.x() + Ball.BALL_WIDTH >= self.screen_dim[0] and self.velocity.x() > 0:
                self.velocity.set_x(-self.velocity.x())
            self.velocity.unit()
            self.pos = self.pos + (self.velocity.to_immutable() * delta * self.speed)

    def reset(self):
        self.launched = False
        self.alive = True
    
    @staticmethod
    def __small_delta():
        """Returns a small random value in [-0.1, 0.1) which has at most 3 decimal places."""
        return round((0.2 * random())-0.1, 3)


class Brick(GameObject):
    """A class for representing a breakable block."""
    BRICK_WIDTH = 30
    BRICK_HEIGHT = 15
    __COLORS = [
        "aquamarine3",
        "blueviolet",
        "chartreuse3",
        "darkgoldenrod2",
        "darkolivegreen3",
        "darkorange3",
        "deeppink2",
        "green3",
        "khaki2"
    ]
    
    def __init__(self, pos: Vector2D):
        super().__init__(pos)
        self.intact = True
        self.rectangle = pg.Rect(*pos.to_tuple(), Brick.BRICK_WIDTH, Brick.BRICK_HEIGHT)
        self.rectangle_outline = pg.Rect(*pos.to_tuple(), Brick.BRICK_WIDTH, Brick.BRICK_HEIGHT)
        self.color = pg.Color(choice(Brick.__COLORS))
        self.color = Brick.__random_color()
        
    def get_rect(self) -> pg.Rect:
        return self.rectangle
    
    def get_center(self):
        return self.pos + Vector2D(Brick.BRICK_WIDTH//2, Brick.BRICK_HEIGHT//2)
        
    def hit(self):
        self.intact = False
    
    def draw(self, screen: pg.Surface):
        """Draw the Brick to the screen."""
        if self.intact:
            pg.draw.rect(screen, self.color, self.rectangle)
            # pg.draw.rect(screen, (0, 0, 0), self.rectangle_outline, width=1)
        
    def update(self):
        """Method for updating a brick (which does nothing.)"""
        pass
    
    @staticmethod
    def __random_color():
        return pg.Color((randint(50, 250), randint(50, 250), randint(50, 250)))
    
    
class Paddle(GameObject):
    PADDLE_WIDTH = 50
    PADDLE_HEIGHT = 10
    PADDLE_SPEED = 300

    def __init__(self, pos: Vector2D, ball: Ball):
        super().__init__(pos)
        self.color = pg.Color((200, 200, 200))
        self.left_vec = Vector2D(-1, 0) * Paddle.PADDLE_SPEED
        self.right_vec = Vector2D(1, 0) * Paddle.PADDLE_SPEED
        self.ball = ball
    
    def draw(self, screen: pg.Surface):
        pg.draw.rect(screen, self.color, self.get_rect())

    def update(self):
        delta = GameConfig.get_value("frame_delta")
        # Key control
        if GameConfig.get_value("controller") == "KEYBOARD":
            pressed_keys = pg.key.get_pressed()
            if pressed_keys[pg.K_LEFT] or pressed_keys[pg.K_a]:
                self.pos = self.pos + (self.left_vec * delta)
                if not self.ball.launched:
                    self.ball.velocity.set_x(-1)
            if pressed_keys[pg.K_RIGHT] or pressed_keys[pg.K_d]:
                self.pos = self.pos + (self.right_vec * delta)
                if not self.ball.launched:
                    self.ball.velocity.set_x(1)
        elif GameConfig.get_value("controller") == "GAMEPAD":
            joystick = GameConfig.get_value("gamepad")
            x_axis = joystick.get_axis(GameConfig.get_value("X-axis"))
            x_axis = round(x_axis)
            if x_axis == -1:
                self.pos = self.pos + (self.left_vec * delta)
                if not self.ball.launched:
                    self.ball.velocity.set_x(-1)
            elif x_axis == 1:
                self.pos = self.pos + (self.right_vec * delta)
                if not self.ball.launched:
                    self.ball.velocity.set_x(1)
        # Bounds checking
        screen_dim = GameConfig.get_value("screen_dim")
        self.pos = self.pos.clamp((0, screen_dim[0]-Paddle.PADDLE_WIDTH), (0, screen_dim[1]-Paddle.PADDLE_HEIGHT))
        if not self.ball.launched:
            self.ball.pos = self.pos + Vector2D((Paddle.PADDLE_WIDTH - Ball.BALL_WIDTH)//2, -(Ball.BALL_HEIGHT + 1))

    def get_rect(self) -> pg.Rect:
        return pg.Rect(*self.pos.to_tuple(), Paddle.PADDLE_WIDTH, Paddle.PADDLE_HEIGHT)
    
    def get_center(self):
        return self.pos + Vector2D(Paddle.PADDLE_WIDTH//2, Paddle.PADDLE_HEIGHT//2)
    