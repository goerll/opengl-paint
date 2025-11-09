from OpenGL.GL import GL_LINE_LOOP, GL_LINE_STRIP
import math
from geometry.vectors import Vec2, Vec3
from geometry.transforms import AngleUtils
from shapes.base import Shape
import logging


class Rectangle(Shape):
    def __init__(self, vertices: list[float], color: Vec3 = Vec3(1.0, 1.0, 1.0), shift_pressed: bool = False):
        x, y = vertices[0], vertices[1]
        width, height = vertices[2] - x, vertices[3] - y

        # If shift is pressed, constrain to square (1:1 aspect ratio)
        if shift_pressed:
            # Use the larger dimension as the side length
            side_length = max(abs(width), abs(height))
            # Maintain the sign of the original width/height
            width = side_length if width >= 0 else -side_length
            height = side_length if height >= 0 else -side_length

        # Generate the full rectangle vertices
        full_vertices = [
            x,                    y,
            x,                    y + height,
            x + width,            y + height,
            x + width,            y,
        ]

        # Initialize with the full rectangle vertices
        super().__init__(full_vertices, color)
        logging.info(f"{'Square' if shift_pressed else 'Rectangle'} created with {len(full_vertices)//2} vertices.")

    def get_vertices(self) -> list[float]:
        return self.vertices

    def get_draw_mode(self) -> int:
        return GL_LINE_LOOP

    def contains_point(self, point: Vec2) -> bool:
        x_min = min(self.vertices[0], self.vertices[4])  # x
        x_max = max(self.vertices[0], self.vertices[4])  # x + width
        y_min = min(self.vertices[1], self.vertices[5])  # y
        y_max = max(self.vertices[1], self.vertices[5])  # y + height

        return (x_min <= point.x <= x_max and y_min <= point.y <= y_max)

    def get_area(self) -> float:
        """Calculate rectangle area"""
        if len(self.vertices) < 8:
            return 0.0

        # For rectangles, vertices are stored as [x1, y1, x2, y2, x3, y3, x4, y4]
        # We can calculate width and height from any two adjacent vertices
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
            # With shift: create equilateral triangle
            size = (end - origin).length() * 2
            height = size * math.sqrt(3) / 2

            full_vertices = [
                x,                    y + height * 2 / 3,  # Top vertex
                x - size / 2,         y - height / 3,      # Bottom left
                x + size / 2,         y - height / 3,      # Bottom right
            ]
            self.is_equilateral = True
        else:
            # Without shift: create right triangle with user-controlled width and height
            width = end.x - origin.x
            height = end.y - origin.y

            full_vertices = [
                x, y,                  # Bottom left corner (origin)
                x + width, y,          # Bottom right corner
                x, y + height,         # Top left corner
            ]
            self.is_equilateral = False

        # Initialize with the full triangle vertices
        super().__init__(full_vertices, color)

    def get_vertices(self) -> list[float]:
        return self.vertices

    def contains_point(self, point: Vec2) -> bool:
        """Check if point is inside triangle using barycentric coordinates"""
        # Get the three vertices of the triangle
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

    def get_area(self) -> float:
        """Calculate triangle area"""
        if self.is_equilateral:
            # Equilateral triangle area using side length
            v1 = Vec2(self.vertices[0], self.vertices[1])  # Top vertex
            v2 = Vec2(self.vertices[2], self.vertices[3])  # Bottom left vertex
            side_length = (v2 - v1).length()
            return (math.sqrt(3) / 4) * side_length * side_length
        else:
            # Right triangle area: 0.5 * base * height
            # Using the Shoelace formula for general triangle area
            v1 = Vec2(self.vertices[0], self.vertices[1])  # Bottom left
            v2 = Vec2(self.vertices[2], self.vertices[3])  # Bottom right
            v3 = Vec2(self.vertices[4], self.vertices[5])  # Top left
            return abs((v1.x * (v2.y - v3.y) + v2.x * (v3.y - v1.y) + v3.x * (v1.y - v2.y)) / 2.0)

    def get_perimeter(self) -> float:
        """Calculate triangle perimeter"""
        # Calculate all three side lengths
        v1 = Vec2(self.vertices[0], self.vertices[1])
        v2 = Vec2(self.vertices[2], self.vertices[3])
        v3 = Vec2(self.vertices[4], self.vertices[5])

        side1 = (v2 - v1).length()
        side2 = (v3 - v2).length()
        side3 = (v1 - v3).length()

        return side1 + side2 + side3


class Circle(Shape):
    """
    Circle and ellipse shape with proper transformation support.
    Circles are rotationally symmetric, but we track rotation for consistency.
    """

    def __init__(self, vertices: list[float], color: Vec3 = Vec3(1.0, 1.0, 1.0), shift_pressed: bool = False):
        x, y = vertices[0], vertices[1]
        self.position = Vec2(x, y)
        end = Vec2(vertices[2], vertices[3])

        # Handle ellipse vs circle based on shift state
        self.shift_pressed = shift_pressed

        if shift_pressed:
            # With shift: constrain to perfect circle
            self.radius_x = (end - self.position).length()
            self.radius_y = self.radius_x
            self.is_circle = True
        else:
            # Without shift: create ellipse
            self.radius_x = abs(end.x - self.position.x)
            self.radius_y = abs(end.y - self.position.y)
            self.is_circle = False

        self.color = color

        # Calculate segments based on the larger radius for smoothness
        max_radius = max(self.radius_x, self.radius_y)
        min_segments = 50
        max_segments = 100
        segments = int(max_radius * 100)
        self.segments = max(min_segments, min(max_segments, segments))

        # Generate base vertices (unrotated circle/ellipse)
        base_vertices = self._generate_base_vertices()

        # Initialize the base class with the calculated vertices
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
        if self.is_circle:
            # Circle: simple distance check
            distance = (point - self.position).length()
            return distance <= self.radius_x  # radius_x == radius_y for circles
        else:
            # Ellipse: check if point satisfies ellipse equation
            dx = (point.x - self.position.x) / self.radius_x if self.radius_x > 0 else float('inf')
            dy = (point.y - self.position.y) / self.radius_y if self.radius_y > 0 else float('inf')
            return dx * dx + dy * dy <= 1.0

    def get_center(self) -> Vec2:
        """Override center calculation for circles - use position"""
        return self.position

    def set_rotation(self, angle_degrees: float) -> None:
        """
        Override rotation for circles.
        For perfect circles, rotation doesn't change the shape but we track it for consistency.
        For ellipses, rotation is meaningful and should be applied.
        """
        if self.is_circle:
            # Perfect circles are rotationally symmetric, but track the angle
            self._rotation = AngleUtils.normalize_degrees(angle_degrees)
            logging.debug(f"Circle rotation set to {self._rotation:.1f}° (no visual change for circles)")
        else:
            # Ellipses should rotate normally
            super().set_rotation(angle_degrees)

    def scale(self, scale_x: float, scale_y: float, center: Vec2 | None = None) -> None:
        """
        Override scaling for circles/ellipses to update radius properties.
        """
        if center is None:
            center = self.position

        # Update radius properties
        self.radius_x *= abs(scale_x)
        self.radius_y *= abs(scale_y)

        # Regenerate base vertices with new radii
        self._base_vertices = self._generate_base_vertices()

        # Reapply rotation if it's an ellipse
        if not self.is_circle and abs(self._rotation) > 0.001:
            self._apply_rotation()
        else:
            self.vertices = self._base_vertices.copy()

        logging.debug(f"Scaled Circle/Ellipse to radii ({self.radius_x:.1f}, {self.radius_y:.1f})")

    def move(self, delta: Vec2) -> None:
        """Move circle by delta and update position"""
        self.position = self.position + delta

        # Regenerate base vertices at new position
        self._base_vertices = self._generate_base_vertices()

        # Reapply rotation to maintain current orientation
        self._apply_rotation()
        logging.debug(f"Moved Circle to ({self.position.x:.1f}, {self.position.y:.1f})")

    def get_area(self) -> float:
        """Calculate circle or ellipse area"""
        if self.is_circle:
            # Circle area: π * r²
            return math.pi * self.radius_x * self.radius_x
        else:
            # Ellipse area: π * a * b (where a and b are semi-major and semi-minor axes)
            return math.pi * self.radius_x * self.radius_y

    def get_perimeter(self) -> float:
        """Calculate circle or ellipse perimeter/circumference"""
        if self.is_circle:
            # Circle circumference: 2 * π * r
            return 2 * math.pi * self.radius_x
        else:
            # Ellipse perimeter approximation (Ramanujan's formula)
            # More accurate than simple approximation
            a, b = self.radius_x, self.radius_y
            h = ((a - b) ** 2) / ((a + b) ** 2)
            return math.pi * (a + b) * (1 + (3 * h) / (10 + math.sqrt(4 - 3 * h)))


class Polygon(Shape):
    def __init__(self, vertices: list[float], color: Vec3 = Vec3(1.0, 1.0, 1.0)):
        super().__init__(vertices, color)
        if len(vertices) >= 2:
            self.centroid_x = sum(vertices[i] for i in range(0, len(vertices), 2)) / (len(vertices) // 2)
            self.centroid_y = sum(vertices[i] for i in range(1, len(vertices), 2)) / (len(vertices) // 2)

        self.color = color
        self.vertices = vertices

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
        """Move polygon by delta and update centroid"""
        # Let base class handle vertex movement
        super().move(delta)

        # Update centroid
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
        if len(self.vertices) < 6:  # Need at least 3 vertices
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
        if len(self.vertices) < 4:  # Need at least 2 vertices
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


class Line(Shape):
    """
    Line shape with support for rotation around its midpoint.
    Lines rotate around their midpoint for natural behavior.
    """

    def __init__(self, points: list[float], color: Vec3 = Vec3(1.0, 1.0, 1.0)):
        # Calculate centroid for potential use
        if len(points) >= 4:  # Need at least 2 points
            self.centroid_x = sum(points[i] for i in range(0, len(points), 2)) / (len(points) // 2)
            self.centroid_y = sum(points[i] for i in range(1, len(points), 2)) / (len(points) // 2)
        else:
            self.centroid_x = 0.0
            self.centroid_y = 0.0

        # Initialize with Shape base class
        super().__init__(points, color)
        self.points = points.copy()

    def get_vertices(self) -> list[float]:
        return self.vertices  # Use the transformed vertices from base class

    def get_draw_mode(self) -> int:
        return GL_LINE_STRIP

    def contains_point(self, point: Vec2) -> bool:
        # Line selection not implemented
        return False

    def get_area(self) -> float:
        """Lines have no area"""
        return 0.0

    def get_perimeter(self) -> float:
        """Calculate line length as perimeter"""
        if len(self.vertices) < 4:  # Need at least 2 points
            return 0.0

        length = 0.0
        n = len(self.vertices) // 2

        for i in range(n - 1):
            x_i = self.vertices[2 * i]
            y_i = self.vertices[2 * i + 1]
            x_j = self.vertices[2 * (i + 1)]
            y_j = self.vertices[2 * (i + 1) + 1]

            segment_length = math.sqrt((x_j - x_i)**2 + (y_j - y_i)**2)
            length += segment_length

        return length

    def move(self, delta: Vec2) -> None:
        """Move line by delta and update centroid"""
        super().move(delta)
        if hasattr(self, 'centroid_x') and hasattr(self, 'centroid_y'):
            self.centroid_x += delta.x
            self.centroid_y += delta.y
        self.points = self.vertices.copy()  # Keep points in sync

    def get_center(self) -> Vec2:
        """Override center calculation for lines - use centroid"""
        if hasattr(self, 'centroid_x') and hasattr(self, 'centroid_y'):
            return Vec2(self.centroid_x, self.centroid_y)
        return super().get_center()