"""
Math utilities for 2D transformations including rotation, translation, and scaling.
This module provides clean, reusable transformation functions following modern design patterns.
"""

import math
from dataclasses import dataclass
from typing import List, Tuple
from geometry.vectors import Vec2


@dataclass(frozen=True)
class Transform2D:
    """
    Immutable 2D transformation using matrix representation.
    Follows the principle of immutability for clean, predictable behavior.
    """
    matrix: Tuple[Tuple[float, float, float],
                  Tuple[float, float, float],
                  Tuple[float, float, float]]

    @classmethod
    def identity(cls) -> 'Transform2D':
        """Create identity transformation matrix"""
        return cls((
            (1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (0.0, 0.0, 1.0)
        ))

    @classmethod
    def translation(cls, dx: float, dy: float) -> 'Transform2D':
        """Create translation transformation"""
        return cls((
            (1.0, 0.0, dx),
            (0.0, 1.0, dy),
            (0.0, 0.0, 1.0)
        ))

    @classmethod
    def rotation(cls, angle_degrees: float) -> 'Transform2D':
        """Create rotation transformation around origin"""
        angle_rad = math.radians(angle_degrees)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)

        return cls((
            (cos_a, -sin_a, 0.0),
            (sin_a,  cos_a, 0.0),
            (0.0,    0.0,   1.0)
        ))

    @classmethod
    def rotation_around_point(cls, angle_degrees: float, center: Vec2) -> 'Transform2D':
        """Create rotation transformation around a specific point"""
        # T * R * T^-1 (translate to origin, rotate, translate back)
        to_origin = cls.translation(-center.x, -center.y)
        rotate = cls.rotation(angle_degrees)
        back_to_point = cls.translation(center.x, center.y)

        return back_to_point.multiply(rotate).multiply(to_origin)

    def multiply(self, other: 'Transform2D') -> 'Transform2D':
        """Multiply two transformation matrices (this * other)"""
        a = self.matrix
        b = other.matrix

        result = [[0.0] * 3 for _ in range(3)]

        for i in range(3):
            for j in range(3):
                for k in range(3):
                    result[i][j] += a[i][k] * b[k][j]

        return Transform2D((
            (result[0][0], result[0][1], result[0][2]),
            (result[1][0], result[1][1], result[1][2]),
            (result[2][0], result[2][1], result[2][2])
        ))

    def transform_point(self, point: Vec2) -> Vec2:
        """Transform a 2D point using this transformation matrix"""
        x = point.x
        y = point.y

        new_x = self.matrix[0][0] * x + self.matrix[0][1] * y + self.matrix[0][2]
        new_y = self.matrix[1][0] * x + self.matrix[1][1] * y + self.matrix[1][2]

        return Vec2(new_x, new_y)

    def transform_vertices(self, vertices: List[float]) -> List[float]:
        """Transform a list of vertices using this transformation"""
        if not vertices:
            return []

        result = []
        for i in range(0, len(vertices), 2):
            point = Vec2(vertices[i], vertices[i + 1])
            transformed = self.transform_point(point)
            result.extend([transformed.x, transformed.y])

        return result


class AngleUtils:
    """Utility class for angle normalization and conversions"""

    @staticmethod
    def normalize_degrees(angle: float) -> float:
        """
        Normalize angle to range [-180, 180] degrees.
        This is the standard range used in most graphics applications.
        """
        # Add 180 to shift range to [0, 360], use modulo, then subtract 180
        normalized = ((angle + 180) % 360) - 180
        # Special case: ensure 180 maps to 180, not -180
        if abs(normalized + 180) < 0.001 and abs(angle - 180) < 0.001:
            return 180.0
        return normalized

    @staticmethod
    def normalize_radians(angle: float) -> float:
        """Normalize angle to range [-π, π] radians"""
        # Add π to shift range to [0, 2π], use modulo, then subtract π
        normalized = ((angle + math.pi) % (2 * math.pi)) - math.pi
        return normalized

    @staticmethod
    def degrees_to_radians(degrees: float) -> float:
        """Convert degrees to radians"""
        return math.radians(degrees)

    @staticmethod
    def radians_to_degrees(radians: float) -> float:
        """Convert radians to degrees"""
        return math.degrees(radians)


def rotate_point_around_center(point: Vec2, center: Vec2, angle_degrees: float) -> Vec2:
    """
    Convenience function to rotate a point around a center.
    This is a cleaner, more readable alternative to matrix multiplication for simple cases.
    """
    transform = Transform2D.rotation_around_point(angle_degrees, center)
    return transform.transform_point(point)


def rotate_vertices_around_center(vertices: List[float], center: Vec2, angle_degrees: float) -> List[float]:
    """
    Convenience function to rotate vertices around a center.
    Handles all the vertex manipulation logic in one place.
    """
    if not vertices:
        return []

    transform = Transform2D.rotation_around_point(angle_degrees, center)
    return transform.transform_vertices(vertices)


def calculate_geometric_center(vertices: List[float]) -> Vec2:
    """
    Calculate the geometric center (centroid) of a set of vertices.
    Uses the standard centroid formula for polygons.
    """
    if not vertices:
        return Vec2(0.0, 0.0)

    if len(vertices) < 4:  # Need at least 2 vertices
        return Vec2(vertices[0] if len(vertices) > 0 else 0.0,
                   vertices[1] if len(vertices) > 1 else 0.0)

    # Calculate average of all vertices
    num_vertices = len(vertices) // 2
    sum_x = sum(vertices[i] for i in range(0, len(vertices), 2))
    sum_y = sum(vertices[i] for i in range(1, len(vertices), 2))

    return Vec2(sum_x / num_vertices, sum_y / num_vertices)