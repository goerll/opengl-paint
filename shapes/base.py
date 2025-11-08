from abc import ABC, abstractmethod
from OpenGL.GL import GL_LINE_LOOP
from geometry.vectors import Vec2, Vec3
import logging


class Shape(ABC):
    def __init__(self, vertices: list[float], color: Vec3 = Vec3(1.0, 1.0, 1.0)) -> None:
        self.vertices: list[float] = vertices.copy()  # Store a copy of input vertices
        self.color = color
        self.thickness = 1

    @abstractmethod
    def get_vertices(self) -> list[float]:
        """Return the vertex data for this shape"""
        pass

    def get_color(self) -> Vec3:
        """Return the color of this shape"""
        return self.color

    def get_draw_mode(self) -> int:
        """Return the OpenGL drawing mode for this shape"""
        return GL_LINE_LOOP

    @abstractmethod
    def contains_point(self, point: Vec2) -> bool:
        """Check if a point is inside this shape"""
        pass

    @abstractmethod
    def get_area(self) -> float:
        """Calculate the area of this shape"""
        pass

    @abstractmethod
    def get_perimeter(self) -> float:
        """Calculate the perimeter of this shape"""
        pass

    def move(self, delta: Vec2) -> None:
        """Move this shape by the given delta"""
        for i in range(0, len(self.vertices), 2):
            self.vertices[i] += delta.x
            self.vertices[i + 1] += delta.y