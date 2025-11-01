from OpenGL.GL import GL_TRIANGLES, GL_LINE_LOOP

import math
from math_utils import Vec2, Vec3


class Shape:
    def __init__(self, position, color=Vec3(1.0, 1.0, 1.0)):
        self.position = position
        self.color = color

    def get_vertices(self):
        raise NotImplementedError

    def get_color(self):
        return self.color

    def get_draw_mode(self):
        return GL_LINE_LOOP


class Rectangle(Shape):
    def __init__(self, position, size, color=Vec3(1.0, 1.0, 1.0)):
        super().__init__(position, color)
        self.size = size

    def get_vertices(self):
        x, y = self.position.x, self.position.y

        vertices = [
            x,
            y,
            x,
            y + self.size.y,
            x + self.size.x,
            y + self.size.y,
            x + self.size.x,
            y,
        ]

        return vertices

    def get_draw_mode(self):
        return GL_LINE_LOOP


class Triangle(Shape):
    def __init__(self, position, size, color=Vec3(1.0, 0.0, 0.0)):
        super().__init__(position, color)
        self.size = size

    def get_vertices(self):
        # Equilateral triangle vertices
        x, y = self.position.x, self.position.y
        height = self.size * math.sqrt(3) / 2

        vertices = [
            x,
            y + height * 2 / 3,  # Top vertex
            x - self.size / 2,
            y - height / 3,  # Bottom left
            x + self.size / 2,
            y - height / 3,  # Bottom right
        ]

        return vertices


class Circle(Shape):
    def __init__(self, position, radius, segments=20, color=Vec3(1.0, 1.0, 1.0)):
        super().__init__(position, color)
        min_segments = 50
        max_segments = 100
        segments = int(radius * 100)
        self.radius = radius
        self.segments = max(min_segments, min(max_segments, segments))

    def get_vertices(self):
        vertices = []
        x, y = self.position.x, self.position.y

        for i in range(self.segments):
            angle = 2.0 * math.pi * i / self.segments
            vertex_x = x + self.radius * math.cos(angle)
            vertex_y = y + self.radius * math.sin(angle)
            vertices.extend([vertex_x, vertex_y])

        return vertices

    def get_draw_mode(self):
        return GL_LINE_LOOP


class Polygon(Shape):
    def __init__(self, points: list[Vec2], color: Vec3 = Vec3(1.0, 1.0, 1.0)):
        # Calculate centroid as position
        if len(points) >= 2:
            centroid_x = sum(point.x for point in points) / len(points)
            centroid_y = sum(point.y for point in points) / len(points)
            super().__init__(Vec2(centroid_x, centroid_y), color)
        else:
            super().__init__(Vec2(0, 0), color)
        self.points = points

    def get_vertices(self):
        return self.points

    def get_draw_mode(self):
        return GL_LINE_LOOP
