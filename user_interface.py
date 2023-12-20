# File: user_interface.py
# Author: Michael Huelsman
# Copyright: Dr. Michael Andrew Huelsman 2023
# License: GNU GPLv3
# Created On: 19 Dec 2023
# Purpose:
#   Simple User Interface Classes
# Notes:

import pygame as pg
from asset_manager import AssetManager
from vector_2d import Vector2D
from abc import abstractmethod


class UIElement:
    def __init__(self):
        self.pos = Vector2D(0.0, 0.0)

    def place(self, at: Vector2D):
        """Places the element with its anchor at the given location."""
        self.pos = at

    def move(self, by: Vector2D):
        """Moves the element by the given amount"""
        self.pos = self.pos + by

    def center(self, dim: (int, int)):
        """Changes the Label's position such that it is centered within the given dimensions"""
        x_val = (dim[0] - self.get_dim()[0])//2
        y_val = (dim[1] - self.get_dim()[1])//2
        self.pos = Vector2D(x_val, y_val)

    def center_horizontal(self, width: int):
        """Changes the Label's position such that it is centered within the given x-dimension"""
        x_val = (width - self.get_dim[0])//2
        y_val = self.pos.y()
        self.pos = Vector2D(x_val, y_val)

    def center_vertical(self, height: int):
        """Changes the Label's position so it is centered within the given y-dimension"""
        y_val = (height - self.get_dim()[1])//2
        x_val = self.pos.x()
        self.pos = Vector2D(x_val, y_val)

    @abstractmethod
    def draw(self, screen: pg.Surface):
        """Draws the element to the given surface at its position."""
        pass

    @abstractmethod
    def get_dim(self) -> (int, int):
        """Returns the current dimensions of the rendered element."""
        pass


class Label(UIElement):
    LARGE_TEXT = 0
    MEDIUM_TEXT = 1
    SMALL_TEXT = 2

    def __init__(self, message: str, text_size: int, color: (int, int, int) = (255, 255, 255)):
        """Constructor for creating a label."""
        super().__init__()
        self.message = message
        self.color = color
        self.font = AssetManager.get_instance().get_font("primary-small")
        if text_size == Label.LARGE_TEXT:
            self.font = AssetManager.get_instance().get_font("primary-medium")
        elif text_size == Label.MEDIUM_TEXT:
            self.font = AssetManager.get_instance().get_font("primary-medium")
        self.surface = self.font.render(self.message, True, self.color)

    def set_text(self, message: str):
        """Sets the Label text to the given message."""
        self.message = message
        self.surface = self.font.render(self.message, True, self.color)

    def set_color(self, color: (int, int, int)):
        """Sets the color of the Label's text to the given RGB value."""
        self.color = color
        self.surface = self.font.render(self.message, True, self.color)

    def get_dim(self) -> (int, int):
        """Returns the current dimensions of the rendered text."""
        return self.surface.get_width(), self.surface.get_height()

    def draw(self, screen: pg.Surface):
        """Draws the text to the given surface at its position."""
        screen.blit(self.surface, self.pos.to_tuple())


class Button(UIElement):
    LARGE_TEXT = 0
    MEDIUM_TEXT = 1
    SMALL_TEXT = 2

    __HIGHLIGHTED_WIDTH = 4
    __UNHIGHLIGHTED_WIDTH = 1

    def __init__(self, message: str, text_size: int, padding: int, color: (int, int, int) = (255, 255, 255)):
        """Constructor for the button class"""
        super().__init__()
        self.message = message
        self.color = color
        self.padding = padding
        self.font = AssetManager.get_instance().get_font("primary-small")
        if text_size == Label.LARGE_TEXT:
            self.font = AssetManager.get_instance().get_font("primary-large")
        elif text_size == Label.MEDIUM_TEXT:
            self.font = AssetManager.get_instance().get_font("primary-medium")
        self.highlighted = False
        self.__render_button()

    def draw(self, screen: pg.Surface):
        """Draws the element to the given surface at its position."""
        screen.blit(self.surface, tuple(self.pos))

    def get_dim(self) -> (int, int):
        """Returns the current dimensions of the rendered element."""
        return self.surface.get_width(), self.surface.get_height()

    def __render_button(self):
        """Renders the Button as a surface."""
        text_surf = self.font.render(self.message, True, self.color)
        res_dim = text_surf.get_width() + 2*self.padding, text_surf.get_height() + 2*self.padding
        self.surface = pg.Surface(res_dim, flags=pg.SRCALPHA)
        self.surface.blit(text_surf, (self.padding, self.padding))
        if self.highlighted:
            pg.draw.rect(self.surface, self.color, self.surface.get_rect(), Button.__HIGHLIGHTED_WIDTH)
        else:
            pg.draw.rect(self.surface, self.color, self.surface.get_rect(), Button.__UNHIGHLIGHTED_WIDTH)


class TextBlock(UIElement):
    LARGE_TEXT = 0
    MEDIUM_TEXT = 1
    SMALL_TEXT = 2

    __LINE_PADDING = 5

    def __init__(self, message: str, text_size: int, width: int, color: (int, int, int) = (255, 255, 255)):
        """Constructor for creating a text block."""
        super().__init__()
        self.message = message
        self.color = color
        self.width = width
        self.font = AssetManager.get_instance().get_font("primary-small")
        if text_size == Label.LARGE_TEXT:
            self.font = AssetManager.get_instance().get_font("primary-medium")
        elif text_size == Label.MEDIUM_TEXT:
            self.font = AssetManager.get_instance().get_font("primary-medium")
        self.__render()

    def set_text(self, message: str):
        """Sets the text to the given message."""
        self.message = message
        self.__render()

    def set_color(self, color: (int, int, int)):
        """Sets the color of the text to the given RGB value."""
        self.color = color
        self.__render()

    def draw(self, screen: pg.Surface):
        """Draws the element to the given surface at its position."""
        screen.blit(self.surface, tuple(self.pos))

    def get_dim(self) -> (int, int):
        """Returns the current dimensions of the rendered element."""
        return self.surface.get_width(), self.surface.get_height()

    def __render(self):
        # Line wrapping
        provided_lines = self.message.split("\n")
        wrapped_text = []
        temp = ""
        for line in provided_lines:
            temp = ""
            words = line.lstrip().split(" ")
            for word in words:
                if self.font.size(word + temp + " ")[0] < self.width:
                    temp = temp + " " + word
                else:
                    wrapped_text.append(temp)
                    temp = word
            if len(temp) != 0:
                wrapped_text.append(temp)
        # Render Text
        rendered_text = []
        res_height = 0
        for line in wrapped_text:
            rendered_text.append(self.font.render(line, True, self.color))
            res_height += rendered_text[-1].get_height()
        # Single Surface
        padding_total = TextBlock.__LINE_PADDING * (len(rendered_text)-1)
        self.surface = pg.Surface((self.width, res_height + padding_total))
        current_y = 0
        for text in rendered_text:
            self.surface.blit(text, (0, current_y))
            current_y += text.get_height() + TextBlock.__LINE_PADDING
