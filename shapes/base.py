from abc import ABC, abstractmethod
from OpenGL.GL import GL_LINE_LOOP
from geometry.vectors import Vec2, Vec3
from geometry.transforms import AngleUtils, calculate_geometric_center, rotate_vertices_around_center
import logging


class Shape(ABC):
    """
    Abstract base class for all drawable shapes with support for transformations.
    Follows clean architecture principles with clear separation of concerns.
    """

    def __init__(self, vertices: list[float], color: Vec3 = Vec3(1.0, 1.0, 1.0)) -> None:
        """
        Initialize a shape with vertices and color.

        Args:
            vertices: List of vertex coordinates [x1, y1, x2, y2, ...]
            color: RGB color vector
        """
        self._base_vertices: list[float] = vertices.copy()  # Original, untransformed vertices
        self.vertices: list[float] = vertices.copy()  # Current transformed vertices
        self.color = color
        self.thickness = 1
        self._rotation: float = 0.0  # Rotation angle in degrees, normalized to [-180, 180]

    @property
    def rotation(self) -> float:
        """Get the current rotation angle in degrees"""
        return self._rotation

    @property
    def base_vertices(self) -> list[float]:
        """Get the original, untransformed vertices"""
        return self._base_vertices.copy()

    @abstractmethod
    def get_vertices(self) -> list[float]:
        """Return the vertex data for this shape"""
        pass

    def get_color(self) -> Vec3:
        """Return the color of this shape"""
        return self.color

    def get_rotation(self) -> float:
        """Return the current rotation angle in degrees"""
        return self._rotation

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

    def set_rotation(self, angle_degrees: float) -> None:
        """
        Set the rotation angle for this shape.

        Args:
            angle_degrees: Rotation angle in degrees (will be normalized to [-180, 180])
        """
        normalized_angle = AngleUtils.normalize_degrees(angle_degrees)
        self._rotation = normalized_angle
        self._apply_rotation()
        logging.debug(f"Set rotation to {normalized_angle:.1f}° for {type(self).__name__}")

    def get_center(self) -> Vec2:
        """
        Get the geometric center of this shape.
        Can be overridden by subclasses for custom center calculations.
        """
        return calculate_geometric_center(self._base_vertices)

    def move(self, delta: Vec2) -> None:
        """
        Move this shape by the given delta vector.

        Args:
            delta: Movement vector
        """
        # Update both base and current vertices
        for i in range(0, len(self._base_vertices), 2):
            self._base_vertices[i] += delta.x
            self._base_vertices[i + 1] += delta.y

        # Reapply rotation to maintain current orientation
        self._apply_rotation()
        logging.debug(f"Moved {type(self).__name__} by ({delta.x:.1f}, {delta.y:.1f})")

    def _apply_rotation(self) -> None:
        """
        Apply the current rotation to the base vertices.
        This is an internal method that maintains the transformation pipeline.
        """
        if abs(self._rotation) < 0.001:
            # No rotation needed, use base vertices directly
            self.vertices = self._base_vertices.copy()
            return

        # Calculate rotation center
        center = self.get_center()

        # Apply rotation transformation
        self.vertices = rotate_vertices_around_center(self._base_vertices, center, self._rotation)

    def scale(self, scale_x: float, scale_y: float, center: Vec2 | None = None) -> None:
        """
        Scale the shape by the given factors around a center point.

        Args:
            scale_x: Scaling factor for X axis
            scale_y: Scaling factor for Y axis
            center: Center point for scaling (defaults to shape center)
        """
        if center is None:
            center = self.get_center()

        # Apply scaling to base vertices using direct math
        new_base_vertices = []
        for i in range(0, len(self._base_vertices), 2):
            x = self._base_vertices[i] - center.x
            y = self._base_vertices[i + 1] - center.y

            # Apply scaling
            scaled_x = x * scale_x + center.x
            scaled_y = y * scale_y + center.y

            new_base_vertices.extend([scaled_x, scaled_y])

        self._base_vertices = new_base_vertices

        # Reapply rotation to maintain current orientation
        self._apply_rotation()

        logging.debug(f"Scaled {type(self).__name__} by ({scale_x:.2f}, {scale_y:.2f}) around ({center.x:.1f}, {center.y:.1f})")

    def scale_from_point(self, scale_x: float, scale_y: float, reference_point: Vec2) -> None:
        """
        Scale the shape relative to a reference point (like mouse position).

        Args:
            scale_x: Scaling factor for X axis
            scale_y: Scaling factor for Y axis
            reference_point: Point relative to which scaling is calculated
        """
        # Calculate center relative to reference point
        center = self.get_center()
        delta = center - reference_point

        # Scale the delta and calculate new center
        new_center = reference_point + Vec2(delta.x * scale_x, delta.y * scale_y)

        # Apply scaling around original center
        self.scale(scale_x, scale_y, center)

        # Move to new center position
        move_delta = new_center - center
        self.move(move_delta)

    def get_bounds(self) -> tuple[Vec2, Vec2]:
        """
        Get the axis-aligned bounding box of the shape.

        Returns:
            Tuple of (min_point, max_point) representing the bounding box
        """
        if not self.vertices:
            return Vec2(0, 0), Vec2(0, 0)

        min_x = min(self.vertices[i] for i in range(0, len(self.vertices), 2))
        max_x = max(self.vertices[i] for i in range(0, len(self.vertices), 2))
        min_y = min(self.vertices[i] for i in range(1, len(self.vertices), 2))
        max_y = max(self.vertices[i] for i in range(1, len(self.vertices), 2))

        return Vec2(min_x, min_y), Vec2(max_x, max_y)