import logging
from typing import Any, List

import glfw

from geometry.vectors import Vec2, Vec3
from shapes.primitives import Triangle, Circle, Rectangle, Polygon


class ShapeFactory:
    """Factory class for creating and managing shapes during user interaction."""

    def __init__(self):
        self.editing_shape: bool = False
        self.vertices: List[float] = []
        self.editing_origin: Vec2 = Vec2(0.0, 0.0)
        self._final_polygon_vertices: List[float] = []

    def start_primitive_creation(self, click_point: Vec2) -> None:
        """Start creating a primitive shape."""
        self.editing_shape = True
        self.vertices = [click_point.x, click_point.y]

    def finish_primitive_creation(self) -> None:
        """Finish creating a primitive shape."""
        self.editing_shape = False
        self.vertices.clear()
        logging.info("Shape creation finished.")

    def handle_polygon_creation(self, window: Any, click_point: Vec2) -> bool:
        """Handle polygon vertex addition and completion. Returns True if polygon was completed."""
        shift_pressed = glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS

        if len(self.vertices) % 2 != 0:
            self.vertices = self.vertices[:-2]

        if not self.vertices:
            self.editing_shape = True
            self.vertices.extend([click_point.x, click_point.y])
        else:
            self.vertices.extend([click_point.x, click_point.y])

        logging.info("Added vertex (%.2f, %.2f) to polygon", click_point.x, click_point.y)

        if shift_pressed and len(self.vertices) >= 6:
            self.editing_shape = False
            if len(self.vertices) % 2 != 0:
                self.vertices = self.vertices[:-2]

            vertex_count = len(self.vertices) // 2
            final_vertices = self.vertices.copy()
            self.vertices.clear()
            logging.info(f"Polygon created with {vertex_count} vertices")
            self._final_polygon_vertices = final_vertices
            return True

        return False

    def create_shape(self, mode: str, vertices: List[float], color: Vec3 = None, shift_pressed: bool = False) -> Triangle | Circle | Rectangle | Polygon | None:
        """Create a shape based on the mode and vertices."""
        if color is None:
            color = Vec3(1.0, 1.0, 1.0)

        match mode:
            case "triangle":
                return Triangle(vertices, color, shift_pressed=shift_pressed)
            case "circle":
                return Circle(vertices, color, shift_pressed=shift_pressed)
            case "rectangle":
                return Rectangle(vertices, color, shift_pressed=shift_pressed)
            case "polygon":
                return Polygon(vertices, color)
            case _:
                logging.error(f"Invalid shape mode: {mode}")
                return None

    def is_editing(self) -> bool:
        """Check if currently editing a shape"""
        return self.editing_shape

    def get_current_vertices(self) -> List[float]:
        """Get current vertices being edited"""
        return self.vertices.copy()

    def get_final_polygon_vertices(self) -> List[float]:
        """Get the final polygon vertices for shape creation"""
        return self._final_polygon_vertices.copy()

    def clear_editing_state(self) -> None:
        """Clear all editing state"""
        self.editing_shape = False
        self.vertices.clear()
        self._final_polygon_vertices.clear()