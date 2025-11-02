from OpenGL.GL import GL_TRIANGLES, GL_LINE_LOOP, GL_LINE_STRIP

import logging
import math
from math_utils import Vec2, Vec3


class Shape:
    def __init__(self, vertices: list[float], color: Vec3 = Vec3(1.0, 1.0, 1.0)):
        self.vertices = []
        self.color = color
        self.thickness = 1

    def get_vertices(self):
        raise NotImplementedError

    def get_color(self):
        return self.color

    def get_draw_mode(self):
        return GL_LINE_LOOP

    def contains_point(self, point: Vec2) -> bool:
        raise NotImplementedError

    def move(self, delta: Vec2) -> None:
        for i in range(0, len(self.vertices), 2):
            self.vertices[i] += delta.x
            self.vertices[i + 1] += delta.y


class Rectangle(Shape):
    def __init__(self, vertices: list[float], color: Vec3 = Vec3(1.0, 1.0, 1.0)):
        super().__init__(vertices, color)

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

        logging.info(f"Rectangle created with {len(self.vertices)//2} vertices.")


    def get_vertices(self):
        return self.vertices

    def get_draw_mode(self):
        return GL_LINE_LOOP

    def contains_point(self, point: Vec2) -> bool:
        print("ENTROU")

        x_min = min(self.vertices[0], self.vertices[4])  # x
        x_max = max(self.vertices[0], self.vertices[4])  # x + width
        y_min = min(self.vertices[1], self.vertices[5])  # y
        y_max = max(self.vertices[1], self.vertices[5])  # y + height
        
        if (x_min <= point.x <= x_max):
            print("BLA")
        if (y_min <= point.y <= y_max):
            print("BLE")
        return (x_min <= point.x <= x_max and y_min <= point.y <= y_max)

    def move(self, delta: Vec2) -> None:
        logging.info("Moving rectangle")
        for i in range(0, len(self.vertices), 2):
            self.vertices[i] += delta.x
            self.vertices[i + 1] += delta.y


class Triangle(Shape):
    def __init__(self, vertices: list[float], color: Vec3 = Vec3(1.0, 0.0, 0.0)):
        super().__init__(vertices, color)
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

    def contains_point(self, point: Vec2) -> bool:
        """Check if point is inside triangle using barycentric coordinates"""
        # Get the three vertices of the equilateral triangle
        vertices = self.get_vertices()
        v1 = Vec2(vertices[0], vertices[1])
        v2 = Vec2(vertices[2], vertices[3])
        v3 = Vec2(vertices[4], vertices[5])
        
        # Calculate vectors
        v0 = v3 - v1
        v1_vec = v2 - v1
        v2_vec = point - v1
        
        # Calculate dot products
        dot00 = v0 * v0
        dot01 = v0 * v1_vec
        dot02 = v0 * v2_vec
        dot11 = v1_vec * v1_vec
        dot12 = v1_vec * v2_vec
        
        # Calculate barycentric coordinates
        denom = dot00 * dot11 - dot01 * dot01
        if abs(denom) < 1e-10:  # Degenerate triangle
            return False
        
        inv_denom = 1.0 / denom
        u = (dot11 * dot02 - dot01 * dot12) * inv_denom
        v = (dot00 * dot12 - dot01 * dot02) * inv_denom
        
        # Check if point is in triangle
        return (u >= 0) and (v >= 0) and (u + v <= 1)


class Circle(Shape):
    def __init__(self, vertices: list[float], color: Vec3 = Vec3(1.0, 1.0, 1.0)):
        super().__init__(vertices, color)
        x, y = vertices[0], vertices[1]
        origin = Vec2(x, y)
        self.position = origin
        end = Vec2(vertices[2], vertices[3])
        self.radius = (end - origin).length()
        self.color = color

        min_segments = 50
        max_segments = 100
        segments = int(self.radius * 100)
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

    def contains_point(self, point: Vec2) -> bool:
        distance = (point - self.position).length()
        return distance <= self.radius

    def move(self, delta: Vec2) -> None:
        self.position = self.position + delta

        for i in range(0, len(self.vertices), 2):
            self.vertices[i] += delta.x
            self.vertices[i + 1] += delta.y

class Polygon(Shape):
    def __init__(self, vertices: list[float], color: Vec3 = Vec3(1.0, 1.0, 1.0)):
        super().__init__(vertices, color)
        if len(vertices) >= 2:
            self.centroid_x = sum(vertices[i] for i in range(0, len(vertices), 2)) / (len(vertices) // 2)
            self.centroid_y = sum(vertices[i] for i in range(1, len(vertices), 2)) / (len(vertices) // 2)

        self.color = color
        self.vertices = vertices

    def get_vertices(self):
        return self.vertices

    def get_draw_mode(self):
        return GL_LINE_LOOP

    def contains_point(self, point: Vec2) -> bool:
        """Ray casting algorithm: shoot ray right, count edge crossings"""
        if len(self.vertices) < 6:
            return False

        x, y = point.x, point.y
        inside = False
        
        # Start with the last vertex
        p1x, p1y = self.vertices[-2], self.vertices[-1]
        
        # Check each edge
        for i in range(0, len(self.vertices), 2):
            p2x, p2y = self.vertices[i], self.vertices[i + 1]
            
            # Check if the ray crosses this edge
            if y > min(p1y, p2y) and y <= max(p1y, p2y):
                if p1y != p2y:  # Edge is not horizontal
                    # Calculate intersection point of ray with edge
                    x_intersection = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    
                    # If point is to the left of or at intersection, count it
                    if x <= x_intersection:
                        inside = not inside
                # Horizontal edges (p1y == p2y) are automatically excluded
                # by the outer condition, since y can't be both > p1y and <= p1y
            
            # Move to next edge
            p1x, p1y = p2x, p2y
        
        return inside

    def move(self, delta: Vec2) -> None:
        # Move all vertices
        for i in range(0, len(self.vertices), 2):
            self.vertices[i] += delta.x
            self.vertices[i + 1] += delta.y
        
        # Update centroid
        if hasattr(self, 'centroid_x') and hasattr(self, 'centroid_y'):
            self.centroid_x += delta.x
            self.centroid_y += delta.y

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
