"""Math utilities for 2D transformations including rotation, translation, and scaling"""

import math
from dataclasses import dataclass
from typing import List, Tuple
from geometry.vectors import Vec2


class AngleUtils:
    """Utility class for angle normalization and conversions"""

    @staticmethod
    def normalize_degrees(angle: float) -> float:
        """Normalize angle to range [-180, 180] degrees"""
        normalized = ((angle + 180) % 360) - 180
        if abs(normalized + 180) < 0.001 and abs(angle - 180) < 0.001:
            return 180.0
        return normalized


def rotate_vertices_around_center(vertices: List[float], center: Vec2, angle_degrees: float) -> List[float]:
    """Rotate vertices around a center point by specified angle in degrees"""
    if not vertices:
        return []

    result = []
    angle_rad = math.radians(angle_degrees)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)

    for i in range(0, len(vertices), 2):
        x, y = vertices[i], vertices[i + 1]
        # Translate to origin
        x -= center.x
        y -= center.y
        # Rotate
        new_x = x * cos_a - y * sin_a
        new_y = x * sin_a + y * cos_a
        # Translate back
        new_x += center.x
        new_y += center.y
        result.extend([new_x, new_y])

    return result


def calculate_geometric_center(vertices: List[float]) -> Vec2:
    """Calculate the geometric center (centroid) of a set of vertices"""
    if not vertices:
        return Vec2(0.0, 0.0)

    if len(vertices) < 4:
        return Vec2(vertices[0] if len(vertices) > 0 else 0.0,
                   vertices[1] if len(vertices) > 1 else 0.0)

    num_vertices = len(vertices) // 2
    sum_x = sum(vertices[i] for i in range(0, len(vertices), 2))
    sum_y = sum(vertices[i] for i in range(1, len(vertices), 2))

    return Vec2(sum_x / num_vertices, sum_y / num_vertices)