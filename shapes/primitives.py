import logging
import math

from OpenGL.GL import GL_LINE_LOOP, GL_LINE_STRIP

from geometry.transforms import AngleUtils
from geometry.vectors import Vec2, Vec3
from shapes.base import Shape


class Rectangle(Shape):
    def __init__(self, vertices: list[float], color: Vec3 = Vec3(1.0, 1.0, 1.0), shift_pressed: bool = False):
        """Initialize a rectangle or square if shift is pressed."""
        x, y = vertices[0], vertices[1]
        width, height = vertices[2] - x, vertices[3] - y

        if shift_pressed:
            side_length = max(abs(width), abs(height))
            width = side_length if width >= 0 else -side_length
            height = side_length if height >= 0 else -side_length

        # Generate rectangle vertices inline
        full_vertices = [
            x, y,           # Bottom left
            x, y + height,  # Top left
            x + width, y + height,  # Top right
            x + width, y    # Bottom right
        ]

        super().__init__(full_vertices, color)
        shape_type = "Square" if shift_pressed else "Rectangle"
        logging.info(f"{shape_type} created with {len(full_vertices)//2} vertices.")

    def get_vertices(self) -> list[float]:
        return self.vertices

    def get_draw_mode(self) -> int:
        return GL_LINE_LOOP

    def contains_point(self, point: Vec2) -> bool:
        """Check if point is inside rectangle using bounds check."""
        x_min = min(self.vertices[0], self.vertices[4])
        x_max = max(self.vertices[0], self.vertices[4])
        y_min = min(self.vertices[1], self.vertices[5])
        y_max = max(self.vertices[1], self.vertices[5])

        return x_min <= point.x <= x_max and y_min <= point.y <= y_max

    def get_area(self) -> float:
        """Calculate rectangle area using width * height."""
        if len(self.vertices) < 8:
            return 0.0

        width = abs(self.vertices[4] - self.vertices[0])
        height = abs(self.vertices[5] - self.vertices[1])
        return width * height

    def get_perimeter(self) -> float:
        """Calculate rectangle perimeter"""
        if len(self.vertices) < 8:
            return 0.0

        width = abs(self.vertices[4] - self.vertices[0])
        height = abs(self.vertices[5] - self.vertices[1])
        return 2 * (width + height)

    
class Triangle(Shape):
    def __init__(self, vertices: list[float], color: Vec3 = Vec3(1.0, 1.0, 1.0), shift_pressed: bool = False):
        x, y = vertices[0], vertices[1]
        origin = Vec2(x, y)
        end = Vec2(vertices[2], vertices[3])
        self.shift_pressed = shift_pressed
        self.color = color

        if shift_pressed:
            size = (end - origin).length() * 2
            height = size * math.sqrt(3) / 2

            full_vertices = [
                x, y + height * 2 / 3,
                x - size / 2, y - height / 3,
                x + size / 2, y - height / 3,
            ]
            self.is_equilateral = True
        else:
            width = end.x - origin.x
            height = end.y - origin.y

            full_vertices = [
                x, y,
                x + width, y,
                x, y + height,
            ]
            self.is_equilateral = False
        super().__init__(full_vertices, color)

    def get_vertices(self) -> list[float]:
        return self.vertices

    def contains_point(self, point: Vec2) -> bool:
        """Check if point is inside triangle using barycentric coordinates"""
        vertices = self.get_vertices()
        v1 = Vec2(vertices[0], vertices[1])
        v2 = Vec2(vertices[2], vertices[3])
        v3 = Vec2(vertices[4], vertices[5])

        v0 = v3 - v1
        v1_vec = v2 - v1
        v2_vec = point - v1

        dot00 = v0 * v0
        dot01 = v0 * v1_vec
        dot02 = v0 * v2_vec
        dot11 = v1_vec * v1_vec
        dot12 = v1_vec * v2_vec

        # Calculate barycentric coordinates
        denom = dot00 * dot11 - dot01 * dot01
        if abs(denom) < 1e-10:
            return False

        inv_denom = 1.0 / denom
        u = (dot11 * dot02 - dot01 * dot12) * inv_denom
        v = (dot00 * dot12 - dot01 * dot02) * inv_denom

        return u >= 0 and v >= 0 and u + v <= 1

    def get_area(self) -> float:
        """Calculate triangle area"""
        if self.is_equilateral:
            v1 = Vec2(self.vertices[0], self.vertices[1])
            v2 = Vec2(self.vertices[2], self.vertices[3])
            side_length = (v2 - v1).length()
            return (math.sqrt(3) / 4) * side_length * side_length
        else:
            v1 = Vec2(self.vertices[0], self.vertices[1])
            v2 = Vec2(self.vertices[2], self.vertices[3])
            v3 = Vec2(self.vertices[4], self.vertices[5])
            return abs((v1.x * (v2.y - v3.y) + v2.x * (v3.y - v1.y) + v3.x * (v1.y - v2.y)) / 2.0)

    def get_perimeter(self) -> float:
        """Calculate triangle perimeter by summing all three sides."""
        v1 = Vec2(self.vertices[0], self.vertices[1])
        v2 = Vec2(self.vertices[2], self.vertices[3])
        v3 = Vec2(self.vertices[4], self.vertices[5])

        side1 = (v2 - v1).length()
        side2 = (v3 - v2).length()
        side3 = (v1 - v3).length()

        return side1 + side2 + side3


class Circle(Shape):
    """Circle and ellipse shape"""

    def __init__(self, vertices: list[float], color: Vec3 = Vec3(1.0, 1.0, 1.0), shift_pressed: bool = False):
        x, y = vertices[0], vertices[1]
        self.position = Vec2(x, y)
        end = Vec2(vertices[2], vertices[3])

        self.shift_pressed = shift_pressed

        if shift_pressed:
            self.radius_x = (end - self.position).length()
            self.radius_y = self.radius_x
            self.is_circle = True
        else:
            self.radius_x = abs(end.x - self.position.x)
            self.radius_y = abs(end.y - self.position.y)
            self.is_circle = False

        self.color = color

        max_radius = max(self.radius_x, self.radius_y)
        min_segments = 50
        max_segments = 100
        segments = int(max_radius * 100)
        self.segments = max(min_segments, min(max_segments, segments))

        base_vertices = self._generate_base_vertices()
        super().__init__(base_vertices, color)

    def _generate_base_vertices(self) -> list[float]:
        """Generate the base vertices for this circle/ellipse"""
        vertices = []

        for i in range(self.segments):
            angle = 2.0 * math.pi * i / self.segments
            vertex_x = self.position.x + self.radius_x * math.cos(angle)
            vertex_y = self.position.y + self.radius_y * math.sin(angle)
            vertices.extend([vertex_x, vertex_y])

        return vertices

    def get_vertices(self) -> list[float]:
        return self.vertices

    def get_draw_mode(self) -> int:
        return GL_LINE_LOOP

    def contains_point(self, point: Vec2) -> bool:
        """Check if point is inside circle or ellipse."""
        if self.is_circle:
            distance = (point - self.position).length()
            return distance <= self.radius_x
        else:
            dx = (point.x - self.position.x) / self.radius_x if self.radius_x > 0 else float('inf')
            dy = (point.y - self.position.y) / self.radius_y if self.radius_y > 0 else float('inf')
            return dx * dx + dy * dy <= 1.0

    def get_center(self) -> Vec2:
        """Override center calculation for circles - use position"""
        return self.position

    def set_rotation(self, angle_degrees: float) -> None:
        """Override rotation for circles (rotationally symmetric) vs ellipses."""
        if self.is_circle:
            self._rotation = AngleUtils.normalize_degrees(angle_degrees)
            logging.debug(f"Circle rotation set to {self._rotation:.1f}° (no visual change for circles)")
        else:
            super().set_rotation(angle_degrees)

    def scale(self, scale_x: float, scale_y: float, center: Vec2 | None = None) -> None:
        """Override scaling for circles/ellipses to update radius properties"""
        if center is None:
            center = self.position

        self.radius_x *= abs(scale_x)
        self.radius_y *= abs(scale_y)

        self._base_vertices = self._generate_base_vertices()

        if not self.is_circle and abs(self._rotation) > 0.001:
            self._apply_rotation()
        else:
            self.vertices = self._base_vertices.copy()

        logging.debug(f"Scaled Circle/Ellipse to radii ({self.radius_x:.1f}, {self.radius_y:.1f})")

    def move(self, delta: Vec2) -> None:
        """Move circle by delta and update position"""
        self.position = self.position + delta

        self._base_vertices = self._generate_base_vertices()

        self._apply_rotation()
        logging.debug(f"Moved Circle to ({self.position.x:.1f}, {self.position.y:.1f})")

    def get_area(self) -> float:
        """Calculate circle or ellipse area"""
        if self.is_circle:
            return math.pi * self.radius_x * self.radius_x
        else:
            return math.pi * self.radius_x * self.radius_y

    def get_perimeter(self) -> float:
        """Calculate circle or ellipse perimeter/circumference (uses Ramanujan's formula for ellipses)"""
        if self.is_circle:
            return 2 * math.pi * self.radius_x
        else:
            a, b = self.radius_x, self.radius_y
            h = ((a - b) ** 2) / ((a + b) ** 2)
            return math.pi * (a + b) * (1 + (3 * h) / (10 + math.sqrt(4 - 3 * h)))


class Polygon(Shape):
    def __init__(self, vertices: list[float], color: Vec3 = Vec3(1.0, 1.0, 1.0)):
        """Initialize a polygon with vertices and calculate centroid."""
        super().__init__(vertices, color)
        if len(vertices) >= 2:
            self.centroid_x = sum(vertices[i] for i in range(0, len(vertices), 2)) / (len(vertices) // 2)
            self.centroid_y = sum(vertices[i] for i in range(1, len(vertices), 2)) / (len(vertices) // 2)

    def get_vertices(self) -> list[float]:
        return self.vertices

    def get_draw_mode(self) -> int:
        return GL_LINE_LOOP

    def contains_point(self, point: Vec2) -> bool:
        """Ray casting algorithm: shoot ray right, count edge crossings"""
        if len(self.vertices) < 6:
            return False

        x, y = point.x, point.y
        inside = False

        p1x, p1y = self.vertices[-2], self.vertices[-1]

        for i in range(0, len(self.vertices), 2):
            p2x, p2y = self.vertices[i], self.vertices[i + 1]

            if y > min(p1y, p2y) and y <= max(p1y, p2y):
                if p1y != p2y:
                    x_intersection = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x

                    if x <= x_intersection:
                        inside = not inside
            p1x, p1y = p2x, p2y

        return inside

    def move(self, delta: Vec2) -> None:
        """Move polygon by delta and update centroid."""
        super().move(delta)

        if hasattr(self, 'centroid_x') and hasattr(self, 'centroid_y'):
            self.centroid_x += delta.x
            self.centroid_y += delta.y

    def get_center(self) -> Vec2:
        """Override center calculation for polygons - use centroid"""
        if hasattr(self, 'centroid_x') and hasattr(self, 'centroid_y'):
            return Vec2(self.centroid_x, self.centroid_y)
        return super().get_center()

    def get_area(self) -> float:
        """Calculate polygon area using Shoelace formula"""
        if len(self.vertices) < 6:
            return 0.0

        area = 0.0
        n = len(self.vertices) // 2

        for i in range(n):
            j = (i + 1) % n
            x_i = self.vertices[2 * i]
            y_i = self.vertices[2 * i + 1]
            x_j = self.vertices[2 * j]
            y_j = self.vertices[2 * j + 1]
            area += x_i * y_j - x_j * y_i

        return abs(area) / 2.0

    def get_perimeter(self) -> float:
        """Calculate polygon perimeter by summing edge lengths"""
        if len(self.vertices) < 4:
            return 0.0

        perimeter = 0.0
        n = len(self.vertices) // 2

        for i in range(n):
            j = (i + 1) % n
            x_i = self.vertices[2 * i]
            y_i = self.vertices[2 * i + 1]
            x_j = self.vertices[2 * j]
            y_j = self.vertices[2 * j + 1]

            edge_length = math.sqrt((x_j - x_i)**2 + (y_j - y_i)**2)
            perimeter += edge_length

        return perimeter
