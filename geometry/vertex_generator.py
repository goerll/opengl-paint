"""
Vertex generation utilities for creating common shape vertex patterns.
Standardizes shape creation and eliminates code duplication across shape classes.
"""

import math
from typing import List, Tuple
from geometry.vectors import Vec2
from config.constants import DrawingConfig


class VertexGenerator:
    """Utility class for generating vertex patterns for common shapes"""

    @staticmethod
    def generate_rectangle(min_bound: Vec2, max_bound: Vec2) -> List[float]:
        """
        Generate vertices for a rectangle from bounds.

        Args:
            min_bound: Minimum corner of the rectangle
            max_bound: Maximum corner of the rectangle

        Returns:
            List of vertex coordinates [x1, y1, x2, y2, ...]
        """
        return [
            min_bound.x, min_bound.y,  # Bottom left
            min_bound.x, max_bound.y,  # Top left
            max_bound.x, max_bound.y,  # Top right
            max_bound.x, min_bound.y   # Bottom right
        ]

    @staticmethod
    def generate_circle(center: Vec2, radius: float, segments: int = None) -> List[float]:
        """
        Generate vertices for a circle.

        Args:
            center: Center point of the circle
            radius: Radius of the circle
            segments: Number of segments (defaults to config value)

        Returns:
            List of vertex coordinates [x1, y1, x2, y2, ...]
        """
        if segments is None:
            segments = DrawingConfig.DEFAULT_CIRCLE_SEGMENTS

        vertices = []
        angle_step = 2 * math.pi / segments

        for i in range(segments):
            angle = i * angle_step
            x = center.x + radius * math.cos(angle)
            y = center.y + radius * math.sin(angle)
            vertices.extend([x, y])

        return vertices

    @staticmethod
    def generate_ellipse(center: Vec2, radius_x: float, radius_y: float, segments: int = None) -> List[float]:
        """
        Generate vertices for an ellipse.

        Args:
            center: Center point of the ellipse
            radius_x: Horizontal radius
            radius_y: Vertical radius
            segments: Number of segments (defaults to config value)

        Returns:
            List of vertex coordinates [x1, y1, x2, y2, ...]
        """
        if segments is None:
            segments = DrawingConfig.DEFAULT_CIRCLE_SEGMENTS

        vertices = []
        angle_step = 2 * math.pi / segments

        for i in range(segments):
            angle = i * angle_step
            x = center.x + radius_x * math.cos(angle)
            y = center.y + radius_y * math.sin(angle)
            vertices.extend([x, y])

        return vertices

    @staticmethod
    def generate_regular_polygon(center: Vec2, radius: float, sides: int, rotation: float = 0.0) -> List[float]:
        """
        Generate vertices for a regular polygon.

        Args:
            center: Center point of the polygon
            radius: Distance from center to vertices
            sides: Number of sides
            rotation: Rotation angle in radians

        Returns:
            List of vertex coordinates [x1, y1, x2, y2, ...]
        """
        if sides < 3:
            raise ValueError("Polygon must have at least 3 sides")

        vertices = []
        angle_step = 2 * math.pi / sides
        start_angle = rotation - math.pi / 2  # Start from top

        for i in range(sides):
            angle = start_angle + i * angle_step
            x = center.x + radius * math.cos(angle)
            y = center.y + radius * math.sin(angle)
            vertices.extend([x, y])

        return vertices

    @staticmethod
    def generate_triangle_from_points(p1: Vec2, p2: Vec2, p3: Vec2) -> List[float]:
        """
        Generate vertices for a triangle from three points.

        Args:
            p1: First vertex
            p2: Second vertex
            p3: Third vertex

        Returns:
            List of vertex coordinates [x1, y1, x2, y2, x3, y3]
        """
        return [p1.x, p1.y, p2.x, p2.y, p3.x, p3.y]

    @staticmethod
    def generate_isosceles_triangle(base_center: Vec2, base_width: float, height: float) -> List[float]:
        """
        Generate vertices for an isosceles triangle.

        Args:
            base_center: Center point of the base
            base_width: Width of the base
            height: Height from base to apex

        Returns:
            List of vertex coordinates [x1, y1, x2, y2, x3, y3]
        """
        left = Vec2(base_center.x - base_width / 2, base_center.y)
        right = Vec2(base_center.x + base_width / 2, base_center.y)
        apex = Vec2(base_center.x, base_center.y + height)

        return VertexGenerator.generate_triangle_from_points(left, right, apex)

    @staticmethod
    def generate_right_triangle(right_angle: Vec2, base_length: float, height: float) -> List[float]:
        """
        Generate vertices for a right triangle.

        Args:
            right_angle: Position of the right angle vertex
            base_length: Length of the base (horizontal)
            height: Height of the triangle (vertical)

        Returns:
            List of vertex coordinates [x1, y1, x2, y2, x3, y3]
        """
        p1 = right_angle
        p2 = Vec2(right_angle.x + base_length, right_angle.y)
        p3 = Vec2(right_angle.x, right_angle.y + height)

        return VertexGenerator.generate_triangle_from_points(p1, p2, p3)

    @staticmethod
    def generate_line(start: Vec2, end: Vec2) -> List[float]:
        """
        Generate vertices for a line segment.

        Args:
            start: Starting point
            end: Ending point

        Returns:
            List of vertex coordinates [x1, y1, x2, y2]
        """
        return [start.x, start.y, end.x, end.y]

    @staticmethod
    def generate_dashed_line(start: Vec2, end: Vec2, dash_length: float, gap_length: float) -> List[float]:
        """
        Generate vertices for a dashed line.

        Args:
            start: Starting point
            end: Ending point
            dash_length: Length of each dash
            gap_length: Length of each gap

        Returns:
            List of vertex coordinates for multiple line segments
        """
        vertices = []
        direction = (end - start)
        total_length = direction.length()

        if total_length == 0:
            return vertices

        direction = direction.normalized()
        current_pos = start
        pattern_length = dash_length + gap_length

        while current_pos.distance_to(end) > dash_length:
            # Add dash
            dash_end = current_pos + direction * dash_length
            vertices.extend(VertexGenerator.generate_line(current_pos, dash_end))

            # Skip gap
            current_pos = dash_end + direction * gap_length

            # Don't overshoot the end
            if current_pos.distance_to(start) >= total_length:
                break

        # Add final dash if needed
        if current_pos.distance_to(end) > DrawingConfig.MIN_DRAG_DISTANCE:
            vertices.extend(VertexGenerator.generate_line(current_pos, end))

        return vertices

    @staticmethod
    def generate_arc(center: Vec2, radius: float, start_angle: float, end_angle: float, segments: int = None) -> List[float]:
        """
        Generate vertices for an arc.

        Args:
            center: Center point of the arc
            radius: Radius of the arc
            start_angle: Starting angle in radians
            end_angle: Ending angle in radians
            segments: Number of segments (defaults to config value)

        Returns:
            List of vertex coordinates [x1, y1, x2, y2, ...]
        """
        if segments is None:
            # Calculate segments based on arc length
            arc_length = abs(end_angle - start_angle)
            segments = max(3, int(arc_length / (2 * math.pi) * DrawingConfig.DEFAULT_CIRCLE_SEGMENTS))

        vertices = []
        angle_step = (end_angle - start_angle) / segments

        for i in range(segments + 1):
            angle = start_angle + i * angle_step
            x = center.x + radius * math.cos(angle)
            y = center.y + radius * math.sin(angle)
            vertices.extend([x, y])

        return vertices

    @staticmethod
    def calculate_bounds_from_vertices(vertices: List[float]) -> Tuple[Vec2, Vec2]:
        """
        Calculate bounding box from a list of vertices.

        Args:
            vertices: List of vertex coordinates [x1, y1, x2, y2, ...]

        Returns:
            Tuple of (min_point, max_point) representing the bounding box
        """
        if not vertices:
            return Vec2(0, 0), Vec2(0, 0)

        min_x = min(vertices[i] for i in range(0, len(vertices), 2))
        max_x = max(vertices[i] for i in range(0, len(vertices), 2))
        min_y = min(vertices[i] for i in range(1, len(vertices), 2))
        max_y = max(vertices[i] for i in range(1, len(vertices), 2))

        return Vec2(min_x, min_y), Vec2(max_x, max_y)

    @staticmethod
    def translate_vertices(vertices: List[float], offset: Vec2) -> List[float]:
        """
        Translate all vertices by an offset.

        Args:
            vertices: List of vertex coordinates
            offset: Translation offset

        Returns:
            Translated vertices
        """
        translated = []
        for i in range(0, len(vertices), 2):
            translated.append(vertices[i] + offset.x)
            translated.append(vertices[i + 1] + offset.y)
        return translated

    @staticmethod
    def scale_vertices(vertices: List[float], scale: float, center: Vec2) -> List[float]:
        """
        Scale vertices around a center point.

        Args:
            vertices: List of vertex coordinates
            scale: Scale factor
            center: Center point for scaling

        Returns:
            Scaled vertices
        """
        scaled = []
        for i in range(0, len(vertices), 2):
            x = vertices[i] - center.x
            y = vertices[i + 1] - center.y
            scaled.append(x * scale + center.x)
            scaled.append(y * scale + center.y)
        return scaled