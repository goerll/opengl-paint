from OpenGL.GL import GL_TRIANGLES, GL_LINE_LOOP, GL_LINE_STRIP

import math
from math_utils import Vec2, Vec3


class Shape:
    def __init__(self, vertices: list[float], color: Vec3 = Vec3(1.0, 1.0, 1.0)):
        self.vertices = vertices
        self.color = color

    def get_vertices(self):
        raise NotImplementedError

    def get_color(self):
        return self.color

    def get_draw_mode(self):
        return GL_LINE_LOOP

    def contains_point(self, point: Vec2) -> bool:
        raise NotImplementedError


class Rectangle(Shape):
    def __init__(self, vertices: list[float], color: Vec3 = Vec3(1.0, 1.0, 1.0)):
        self.color = color

        x, y = vertices[0], vertices[1]
        width, height = vertices[2] - x, vertices[3] - y

        self.vertices = [
            x,
            y,
            x,
            y + height,
            x + width,
            y + height,
            x + width,
            y,
        ]


    def get_vertices(self):
        return self.vertices

    def get_draw_mode(self):
        return GL_LINE_LOOP

    def contains_point(self, point: Vec2) -> bool:
        return (
            self.vertices[0] <= point.x <= self.vertices[2]
            and self.vertices[1] <= point.y <= self.vertices[3]
        )


class Triangle(Shape):
    def __init__(self, vertices: list[float], color: Vec3 = Vec3(1.0, 0.0, 0.0)):
        x, y = vertices[0], vertices[1]
        origin = Vec2(x, y)
        end = Vec2(vertices[2], vertices[3])
        size = (end - origin).length() * 2
        height = size * math.sqrt(3) / 2
        self.color = color

        self.vertices = [
            x,
            y + height * 2 / 3,  # Top vertex
            x - size / 2,
            y - height / 3,  # Bottom left
            x + size / 2,
            y - height / 3,  # Bottom right
        ]

    def get_vertices(self):
        return self.vertices


class Circle(Shape):
    def __init__(self, vertices: list[float], color: Vec3 = Vec3(1.0, 1.0, 1.0)):
        x, y = vertices[0], vertices[1]
        origin = Vec2(x, y)
        end = Vec2(vertices[2], vertices[3])
        radius = (end - origin).length()
        self.color = color

        min_segments = 50
        max_segments = 100
        segments = int(radius * 100)
        self.radius = radius
        self.segments = max(min_segments, min(max_segments, segments))

        self.vertices = []

        for i in range(self.segments):
            angle = 2.0 * math.pi * i / self.segments
            vertex_x = x + self.radius * math.cos(angle)
            vertex_y = y + self.radius * math.sin(angle)
            self.vertices.extend([vertex_x, vertex_y])


    def get_vertices(self):
        return self.vertices

    def get_draw_mode(self):
        return GL_LINE_LOOP


class Polygon(Shape):
    def __init__(self, points: list[float], color: Vec3 = Vec3(1.0, 1.0, 1.0)):
        if len(points) >= 2:
            self.centroid_x = sum(points[i] for i in range(0, len(points), 2)) / (len(points) // 2)
            self.centroid_y = sum(points[i] for i in range(1, len(points), 2)) / (len(points) // 2)

        self.color = color
        self.points = points

    def get_vertices(self):
        return self.points

    def get_draw_mode(self):
        return GL_LINE_LOOP

class Line(Shape):
    def __init__(self, points: list[float], color: Vec3 = Vec3(1.0, 1.0, 1.0)):
        if len(points) >= 2:
            self.centroid_x = sum(points[i] for i in range(0, len(points), 2)) / (len(points) // 2)
            self.centroid_y = sum(points[i] for i in range(1, len(points), 2)) / (len(points) // 2)

        self.color = Vec3(1.0, 1.0, 1.0)
        self.points = points

    def get_vertices(self):
        return self.points

    def get_draw_mode(self):
        return GL_LINE_STRIP
