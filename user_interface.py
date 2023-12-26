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
        x_val = (width - self.get_dim()[0])//2
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
    GIANT_TEXT = 0
    LARGE_TEXT = 1
    MEDIUM_TEXT = 2
    SMALL_TEXT = 3

    def __init__(self, message: str, text_size: int, color: (int, int, int) = (255, 255, 255)):
        """Constructor for creating a label."""
        super().__init__()
        self.message = message
        self.color = color
        self.font = AssetManager.get_instance().get_font("primary-small")
        if text_size == TextBlock.GIANT_TEXT:
            self.font = AssetManager.get_instance().get_font("primary-giant")
        elif text_size == Label.LARGE_TEXT:
            self.font = AssetManager.get_instance().get_font("primary-large")
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
    GIANT_TEXT = 0
    LARGE_TEXT = 1
    MEDIUM_TEXT = 2
    SMALL_TEXT = 3

    __HIGHLIGHT_COLOR = (255, 0, 0, 255)

    def __init__(self, message: str, text_size: int, padding: int, color: (int, int, int) = (255, 255, 255)):
        """Constructor for the button class"""
        super().__init__()
        self.message = message
        self.color = color
        self.padding = padding
        self.font = AssetManager.get_instance().get_font("primary-small")
        if text_size == Button.GIANT_TEXT:
            self.font = AssetManager.get_instance().get_font("primary-giant")
        if text_size == Button.LARGE_TEXT:
            self.font = AssetManager.get_instance().get_font("primary-large")
        elif text_size == Button.MEDIUM_TEXT:
            self.font = AssetManager.get_instance().get_font("primary-medium")
        self.highlighted = False
        self.__render_button()

    def draw(self, screen: pg.Surface):
        """Draws the element to the given surface at its position."""
        screen.blit(self.surface, tuple(self.pos))

    def get_dim(self) -> (int, int):
        """Returns the current dimensions of the rendered element."""
        return self.surface.get_width(), self.surface.get_height()

    def highlight(self, status: bool):
        """Changes the button's highlight status based on the provided value."""
        if self.highlighted != status:
            self.highlighted = status
            self.__render_button()

    def inside(self, loc: (int, int)) -> bool:
        """Returns true if the provided location is within the button."""
        x_lim = self.pos.x() + self.get_dim()[0]
        y_lim = self.pos.y() + self.get_dim()[1]
        return self.pos.x() <= loc[0] <= x_lim and self.pos.y() <= loc[1] <= y_lim

    def __render_button(self):
        """Renders the Button as a surface."""
        text_surf = self.font.render(self.message, True, self.color)
        res_dim = text_surf.get_width() + 2*self.padding, text_surf.get_height() + 2*self.padding
        self.surface = pg.Surface(res_dim, flags=pg.SRCALPHA)
        self.surface.blit(text_surf, (self.padding, self.padding))
        if self.highlighted:
            pg.draw.rect(self.surface, Button.__HIGHLIGHT_COLOR, self.surface.get_rect(), 1)
        else:
            pg.draw.rect(self.surface, self.color, self.surface.get_rect(), 1)


class TextBlock(UIElement):
    GIANT_TEXT = 0
    LARGE_TEXT = 1
    MEDIUM_TEXT = 2
    SMALL_TEXT = 3

    __LINE_PADDING = 5

    def __init__(self, message: str, text_size: int, width: int, color: (int, int, int) = (255, 255, 255)):
        """Constructor for creating a text block."""
        super().__init__()
        self.message = message
        self.color = color
        self.width = width
        self.font = AssetManager.get_instance().get_font("primary-small")
        if text_size == TextBlock.GIANT_TEXT:
            self.font = AssetManager.get_instance().get_font("primary-giant")
        if text_size == TextBlock.LARGE_TEXT:
            self.font = AssetManager.get_instance().get_font("primary-large")
        elif text_size == TextBlock.MEDIUM_TEXT:
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


class CompoundUIElement(UIElement):
    def __init__(self, elements: [UIElement, ...], padding: int = 5):
        """Constructor for creating a compound UI element."""
        super().__init__()
        self.elements = elements
        self.padding = padding
        self.__render()

    def each_element(self):
        """Iterator over each element in the compound UI element."""
        for element in self.elements:
            yield element

    def draw(self, screen: pg.Surface):
        """Draws the element to the given surface at its position."""
        self.__render()
        screen.blit(self.surface, tuple(self.pos))

    def get_dim(self) -> (int, int):
        """Returns the current dimensions of the rendered element."""
        return self.surface.get_width(), self.surface.get_height()

    def __render(self):
        width = max(list(map(lambda element: element.get_dim()[0], self.elements)))
        height = sum(list(map(lambda element: element.get_dim()[1], self.elements)))
        height += self.padding * (len(self.elements) - 1)
        self.surface = pg.Surface((width, height))
        current_y = 0.0
        for element in self.elements:
            element.place(Vector2D(0.0, current_y))
            element.center_horizontal(width)
            element.draw(self.surface)
            current_y += element.get_dim()[1] + self.padding

