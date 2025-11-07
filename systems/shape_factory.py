import glfw
from typing import Any, List
from geometry.vectors import Vec2, Vec3
from shapes.primitives import Triangle, Circle, Rectangle, Polygon
import logging


class ShapeFactory:
    def __init__(self):
        self.editing_shape: bool = False
        self.vertices: List[float] = []
        self.editing_origin: Vec2 = Vec2(0.0, 0.0)
        self._final_polygon_vertices: List[float] = []

    def start_primitive_creation(self, click_point: Vec2) -> None:
        """Start creating a primitive shape"""
        self.editing_shape = True
        self.vertices = [click_point.x, click_point.y]
        # Initial shape will be created by the main app

    def finish_primitive_creation(self) -> None:
        """Finish creating a primitive shape"""
        self.editing_shape = False
        self.vertices.clear()
        logging.info(f"Shape creation finished.")

    def handle_polygon_creation(self, window: Any, click_point: Vec2) -> bool:
        """Handle polygon vertex addition and completion. Returns True if polygon was completed."""
        shift_pressed = glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS

        # Remove preview point if it exists (odd number of coordinates)
        if len(self.vertices) % 2 != 0:
            self.vertices = self.vertices[:-2]

        # Add the new vertex
        if not self.vertices:  # First vertex
            self.editing_shape = True
            self.vertices.extend([click_point.x, click_point.y])
        else:  # Additional vertices
            self.vertices.extend([click_point.x, click_point.y])

        logging.info("Added vertex (%.2f, %.2f) to polygon", click_point.x, click_point.y)

        # Complete polygon if shift pressed
        if shift_pressed and len(self.vertices) >= 6:  # At least 3 vertices
            self.editing_shape = False
            # Remove any preview point before finalizing
            if len(self.vertices) % 2 != 0:
                self.vertices = self.vertices[:-2]

            vertex_count = len(self.vertices) // 2
            # Store vertices before clearing for shape creation
            final_vertices = self.vertices.copy()
            self.vertices.clear()
            logging.info(f"Polygon created with {vertex_count} vertices")
            # Store the final vertices for the caller to create the shape
            self._final_polygon_vertices = final_vertices
            return True

        return False

    def update_shape_drawing(self, wx: float, wy: float) -> None:
        """Update the current shape being drawn"""
        if len(self.vertices) >= 2:
            # For primitive shapes (triangle, circle, rectangle), update the last vertex
            if len(self.vertices) <= 4:
                if len(self.vertices) == 2:
                    # Only first point exists, add second point as preview
                    self.vertices.extend([wx, wy])
                elif len(self.vertices) == 4:
                    # Update the second point
                    self.vertices[2] = wx
                    self.vertices[3] = wy
            # For polygons, add a preview point to show where next vertex would be
            elif len(self.vertices) > 4:
                # Remove old preview point if exists (check if we have odd number of coordinates)
                if len(self.vertices) % 2 != 0:
                    self.vertices = self.vertices[:-2]
                # Add new preview point
                self.vertices.extend([wx, wy])

    def create_shape(self, mode: str, vertices: List[float], color: Vec3 = None) -> Triangle | Circle | Rectangle | Polygon | None:
        """Create a shape based on the mode and vertices"""
        if color is None:
            color = Vec3(1.0, 1.0, 1.0)

        match mode:
            case "triangle":
                return Triangle(vertices, color)
            case "circle":
                return Circle(vertices, color)
            case "rectangle":
                return Rectangle(vertices, color)
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