import glfw
from typing import Any, List
from geometry.vectors import Vec2
from shapes.base import Shape
import logging


class SelectionSystem:
    def __init__(self) -> None:
        self.selected_shapes: List[Shape] = []

    def get_selected_shapes(self) -> List[Shape]:
        """Get the list of selected shapes"""
        return self.selected_shapes.copy()  # Return a copy to prevent external modification

    def handle_selection(self, window: Any, click_point: Vec2, objects: List[Shape]) -> None:
        """Handle shape selection logic"""
        clicked_shape = self._find_clicked_shape(click_point, objects)
        shift_pressed = glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS

        if clicked_shape:
            self._select_shape(clicked_shape, shift_pressed)
            logging.info(f"Selected {type(clicked_shape).__name__}")
        else:
            self._clear_selection()
            logging.info("Deselected")

    def _find_clicked_shape(self, click_point: Vec2, objects: List[Shape]) -> Shape | None:
        """Find the topmost shape at click point"""
        for shape in reversed(objects):
            if shape.contains_point(click_point):
                return shape
        return None

    def _select_shape(self, clicked_shape: Shape, shift_pressed: bool) -> None:
        """Select a shape with proper multi-selection handling"""
        clicked_shape.thickness = 2

        if shift_pressed:
            # Multi-select: add if not already selected
            if clicked_shape not in self.selected_shapes:
                self.selected_shapes.append(clicked_shape)
        else:
            # Single select: clear previous and select new
            if clicked_shape not in self.selected_shapes:
                self._reset_thickness_for_selected()
                self.selected_shapes = [clicked_shape]

    def _clear_selection(self) -> None:
        """Clear all selected shapes"""
        self._reset_thickness_for_selected()
        self.selected_shapes.clear()

    def _reset_thickness_for_selected(self) -> None:
        """Reset thickness for all currently selected shapes"""
        for shape in self.selected_shapes:
            shape.thickness = 1

    def is_empty(self) -> bool:
        """Check if any shapes are selected"""
        return len(self.selected_shapes) == 0

    def get_count(self) -> int:
        """Get number of selected shapes"""
        return len(self.selected_shapes)