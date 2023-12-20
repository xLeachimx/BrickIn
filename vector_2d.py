# File: vector_2d.py
# Author: Michael Huelsman
# Copyright: Dr. Michael Andrew Huelsman 2023
# License: GNU GPLv3
# Created On: 09 Dec 2023
# Purpose:
#   A class for handling point and vector operation in two dimensions
# Notes:

from typing import Union
from math import hypot, atan2, pi, sin, cos

base_num = Union[int, float]


class Vector2D:
    """An immutable class for handling point and vector operation in two dimensions."""
    
    def __init__(self, x: float, y: float):
        """Vector2D constructor"""
        self.__x = float(x)
        self.__y = float(y)
    
    # Accessor functions
    def x(self) -> float:
        """Returns the x-value while preventing assignment."""
        return self.__x
    
    def extract_x(self) -> 'Vector2D':
        """Returns a vector which zeros the y component."""
        return Vector2D(self.__x, 0.0)
    
    def y(self) -> float:
        """Returns the y-value while preventing assignment."""
        return self.__y
    
    def extract_y(self) -> 'Vector2D':
        """Returns a vector which zeros the x component."""
        return Vector2D(0.0, self.__y)
    
    def to_tuple(self):
        """Returns a tuple version of the vector"""
        return self.__x, self.__y
    
    def to_mutable(self) -> 'Vector2DBuilder':
        """Returns a mutable version of the Vector"""
        return Vector2DBuilder(self.__x, self.__y)
    
    def unit(self) -> 'Vector2D':
        """Returns the unit vector of this vector."""
        return self / abs(self)
    
    def cross(self, other: 'Vector2D') -> float:
        """2D cross product"""
        return self.__x * other.__y - self.__y * other.__x
    
    def angle(self) -> float:
        """Returns the angle of the vector from the positive x-axis, in radians [0, 2pi]."""
        return atan2(self.__y, self.__x) + pi
    
    def clamp(self, x_vals: (float, float), y_vals: (float, float)) -> 'Vector2D':
        """Clamps the internal values to be inbetween the given values."""
        x_val = min(max(x_vals[0], self.__x), x_vals[1])
        y_val = min(max(y_vals[0], self.__y), y_vals[1])
        return Vector2D(x_val, y_val)
    
    # Static translation methods
    @staticmethod
    def from_list(lst: list[base_num, base_num]) -> 'Vector2D':
        """Converts the first two elements of the list into a new vector."""
        if not isinstance(lst, list):
            raise TypeError("List not given.")
        if len(lst) < 2:
            raise ValueError("Insufficient elements for conversion.")
        return Vector2D(lst[0], lst[1])
    
    @staticmethod
    def from_tuple(tup: tuple[base_num, base_num]) -> 'Vector2D':
        """Converts the first two elements of the tuple into a new vector."""
        if not isinstance(tup, tuple):
            raise TypeError("Tuple not given.")
        if len(tup) < 2:
            raise ValueError("Insufficient elements for conversion.")
        return Vector2D(tup[0], tup[1])
    
    @staticmethod
    def from_angle(angle: base_num) -> 'Vector2D':
        """Converts an angle, in radians, into a new unit vector."""
        if not isinstance(angle, (float, int)):
            raise TypeError("Int or float not given.")
        return Vector2D(cos(angle), sin(angle))
    
    @staticmethod
    def from_angle_deg(angle: base_num) -> 'Vector2D':
        """Converts an angle, in degrees, into a new unit vector."""
        if not isinstance(angle, (float, int)):
            raise TypeError("Int or float not given.")
        return Vector2D(cos(angle), sin(angle))
    
    # Operator Overloading
    def __getitem__(self, item: Union[str, int]) -> float:
        """Overload the [] operator for useful convenience"""
        if isinstance(item, str):
            if item.upper() != 'X' and item.upper() != 'Y':
                raise ValueError("Unknown axis.")
            if item.upper() == 'X':
                return self.__x
            else:
                return self.__y
        elif isinstance(item, int):
            if item != 0 and item != 1:
                raise ValueError("Unknown index.")
            elif item == 0:
                return self.__x
            else:
                return self.__y
        else:
            raise TypeError("Vector2D cannot be index with the given value.")
    
    def __len__(self) -> int:
        """Simple overload for len function."""
        return 2
    
    def __iter__(self):
        """Simple iterator creation for iterating through the coordinates of the vector."""
        return iter((self.__x, self.__y))
    
    def __tuple__(self) -> (int, int):
        """Overloads the tuple() function to return an integer tuple."""
        return int(self.__x), int(self.__y)
    
    def __add__(self, other: Union['Vector2D', tuple[base_num, base_num], list[base_num, base_num]]) -> 'Vector2D':
        """Overloads the + operator to do vector addition."""
        if not isinstance(other, (Vector2D, tuple, list)):
            raise TypeError("Vector2D added with incompatible type.")
        if len(other) < 2:
            raise ValueError("Insufficient dimensions to add to Vector2D object.")
        return Vector2D(self.__x + other[0], self.__y + other[1])
    
    def __sub__(self, other: Union['Vector2D', tuple[base_num, base_num], list[base_num, base_num]]) -> 'Vector2D':
        """Overloads the - operator to do vector subtraction."""
        if not isinstance(other, (Vector2D, tuple, list)):
            raise TypeError("Vector2D subtracted with incompatible type.")
        if len(other) < 2:
            raise ValueError("Insufficient dimensions to subtract from Vector2D object.")
        return Vector2D(self.__x - other[0], self.__y - other[1])
    
    def __mul__(self, other: Union[base_num, 'Vector2D', tuple[base_num, base_num], list[base_num, base_num]]) -> Union['Vector2D', float]:
        """Overloads the * operator to perform the dot product or scale, as determined by type."""
        if isinstance(other, (float, int)):
            return Vector2D(other * self.__x, other * self.__y)
        elif isinstance(other, (Vector2D, tuple, list)) and len(other) >= 2:
            return other[0] * self.__x + other[1] * self.__y
        else:
            raise TypeError("Vector2D multiplied by incompatible type.")
    
    def __truediv__(self, other: base_num) -> 'Vector2D':
        """Overloads the / operator for scaling"""
        if not isinstance(other, (int, float)):
            raise TypeError("Vector2D divided by incompatible type.")
        return Vector2D(self.__x / other, self.__y / other)
    
    def __floordiv__(self, other: base_num) -> 'Vector2D':
        """Overloads the // operator for scaling"""
        if not isinstance(other, (int, float)):
            raise TypeError("Vector2D divided by incompatible type.")
        return Vector2D(int(self.__x / other), int(self.__y / other))
    
    def __abs__(self) -> float:
        """Overloads the abs function which returns the magnitude of the vector."""
        return hypot(self.__x, self.__y)
    
    def __neg__(self) -> 'Vector2D':
        """Overloads the unary - function which negates the X and Y values of the vector."""
        return Vector2D(-self.__x, -self.__y)
    
    def __str__(self):
        return f"<{self.__x}, {self.__y}>"

    def __repr__(self):
        return str(self)
    
    
class Vector2DBuilder:
    """A mutable class for handling point and vector operation in two dimensions."""
    
    def __init__(self, x: float, y: float):
        """Vector2DBuilder constructor"""
        self.__x = float(x)
        self.__y = float(y)
    
    # Accessor functions
    def x(self):
        """Returns the x-value while preventing assignment."""
        return self.__x
    
    def extract_x(self) -> 'Vector2DBuilder':
        """Returns a vector which zeros the y component."""
        self.__y = 0.0
        return self
    
    def y(self):
        """Returns the y-value while preventing assignment."""
        return self.__y
    
    def extract_y(self) -> 'Vector2DBuilder':
        """Returns a vector which zeros the x component."""
        self.__x = 0.0
        return self
    
    def to_tuple(self):
        """Returns a tuple version of the vector"""
        return self.__x, self.__y
    
    def set(self, x, y) -> 'Vector2DBuilder':
        """Sets the Vector2DBuilder's x and y values to the given values."""
        self.__x = x
        self.__y = y
        return self
    
    def set_x(self, x) -> 'Vector2DBuilder':
        """Sets the Vector2DBuilder's x value to the given value."""
        self.__x = x
        return self
    
    def set_y(self, y) -> 'Vector2DBuilder':
        """Sets the Vector2DBuilder's y value to the given value."""
        self.__y = y
        return self
    
    def unit(self) -> 'Vector2DBuilder':
        """Returns the unit vector of this vector."""
        return self / abs(self)
    
    def cross(self, other: 'Vector2DBuilder') -> float:
        """2D cross product"""
        return self.__x * other.__y - self.__y * other.__x
    
    def angle(self) -> float:
        """Returns the angle of the vector from the positive x-axis, in radians [0, 2pi]."""
        return atan2(self.__y, self.__x) + pi
    
    def to_immutable(self) -> Vector2D:
        """Returns an immutable version of the Vector2DBuilder"""
        return Vector2D(self.__x, self.__y)
    
    def clamp(self, x_vals: (float, float), y_vals: (float, float)) -> 'Vector2DBuilder':
        """Clamps the internal values to be inbetween the given values."""
        self.__x = min(max(x_vals[0], self.__x), x_vals[1])
        self.__y = min(max(y_vals[0], self.__y), y_vals[1])
        return self
    
    # Static translation methods
    @staticmethod
    def from_list(lst: list[base_num, base_num]) -> 'Vector2DBuilder':
        """Converts the first two elements of the list into a new vector."""
        if not isinstance(lst, list):
            raise TypeError("List not given.")
        if len(lst) < 2:
            raise ValueError("Insufficient elements for conversion.")
        return Vector2DBuilder(lst[0], lst[1])
    
    @staticmethod
    def from_tuple(tup: tuple[base_num, base_num]) -> 'Vector2DBuilder':
        """Converts the first two elements of the tuple into a new vector."""
        if not isinstance(tup, tuple):
            raise TypeError("Tuple not given.")
        if len(tup) < 2:
            raise ValueError("Insufficient elements for conversion.")
        return Vector2DBuilder(tup[0], tup[1])
    
    @staticmethod
    def from_angle(angle: base_num) -> 'Vector2DBuilder':
        """Converts an angle, in radians, into a new unit vector."""
        if not isinstance(angle, (float, int)):
            raise TypeError("Int or float not given.")
        return Vector2DBuilder(cos(angle), sin(angle))
    
    @staticmethod
    def from_angle_deg(angle: base_num) -> 'Vector2DBuilder':
        """Converts an angle, in degrees, into a new unit vector."""
        if not isinstance(angle, (float, int)):
            raise TypeError("Int or float not given.")
        return Vector2DBuilder(cos(angle), sin(angle))
    
    # Operator Overloading
    def __getitem__(self, item: Union[str, int]) -> float:
        """Overload the [] operator for useful convenience"""
        if isinstance(item, str):
            if item.upper() != 'X' and item.upper() != 'Y':
                raise ValueError("Unknown axis.")
            if item.upper() == 'X':
                return self.__x
            else:
                return self.__y
        elif isinstance(item, int):
            if item != 0 and item != 1:
                raise ValueError("Unknown index.")
            elif item == 0:
                return self.__x
            else:
                return self.__y
        else:
            raise TypeError("Vector2DBuilder cannot be index with the given value.")
    
    def __len__(self) -> int:
        """Simple overload for len function."""
        return 2
    
    def __iter__(self):
        """Simple iterator creation for iterating through the coordinates of the vector."""
        return iter((self.__x, self.__y))
    
    def __int__(self) -> (int, int):
        """Overloads the int() function to return an integer tuple."""
        self.__x = int(self.__x)
        self.__y = int(self.__y)
        return self.__x, self.__y
    
    def __add__(self, other: Union['Vector2DBuilder', tuple[base_num, base_num], list[base_num, base_num]]) -> 'Vector2DBuilder':
        """Overloads the + operator to do vector addition."""
        if not isinstance(other, (Vector2DBuilder, tuple, list)):
            raise TypeError("Vector2DBuilder added with incompatible type.")
        if len(other) < 2:
            raise ValueError("Insufficient dimensions to add to Vector2DBuilder object.")
        self.__x += other[0]
        self.__y += other[1]
        return self
    
    def __sub__(self, other: Union['Vector2DBuilder', tuple[base_num, base_num], list[base_num, base_num]]) -> 'Vector2DBuilder':
        """Overloads the - operator to do vector subtraction."""
        if not isinstance(other, (Vector2DBuilder, tuple, list)):
            raise TypeError("Vector2DBuilder subtracted with incompatible type.")
        if len(other) < 2:
            raise ValueError("Insufficient dimensions to subtract from Vector2DBuilder object.")
        self.__x -= other[0]
        self.__y -= other[1]
        return self
    
    def __mul__(self, other: Union[base_num, 'Vector2DBuilder', tuple[base_num, base_num], list[base_num, base_num]]) -> Union['Vector2DBuilder', float]:
        """Overloads the * operator to perform the dot product or scale, as determined by type."""
        if isinstance(other, (float, int)):
            self.__x = self.__x * other
            self.__y = self.__y * other
            return self
        elif isinstance(other, (Vector2DBuilder, tuple, list)) and len(other) >= 2:
            return other[0] * self.__x + other[1] * self.__y
        else:
            raise TypeError("Vector2DBuilder multiplied by incompatible type.")
    
    def __truediv__(self, other: base_num) -> 'Vector2DBuilder':
        """Overloads the / operator for scaling"""
        if not isinstance(other, (int, float)):
            raise TypeError("Vector2DBuilder divided by incompatible type.")
        self.__x = self.__x/other
        self.__y = self.__y/other
        return self
    
    def __floordiv__(self, other: base_num) -> 'Vector2DBuilder':
        """Overloads the // operator for scaling"""
        if not isinstance(other, (int, float)):
            raise TypeError("Vector2DBuilder divided by incompatible type.")
        self.__x = int(self.__x/other)
        self.__y = int(self.__y/other)
        return self
    
    def __abs__(self) -> float:
        """Overloads the abs function which returns the magnitude of the vector."""
        return hypot(self.__x, self.__y)
    
    def __neg__(self) -> 'Vector2DBuilder':
        """Overloads the unary - function which negates the X and Y values of the vector."""
        self.__x = -self.__x
        self.__y = -self.__y
        return self

    def __str__(self):
        return f"<{self.__x}, {self.__y}>"

    def __repr__(self):
        return str(self)
    