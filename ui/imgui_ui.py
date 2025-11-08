from imgui_bundle import imgui
from typing import Any
import logging

# UI Constants
SIDEBAR_PADDING = 10
SIDEBAR_WIDTH = 280

# Drawing modes
DRAWING_MODES = {
    "select": "Select (S)",
    "triangle": "Triangle (T)",
    "circle": "Circle (C)",
    "rectangle": "Rectangle (R)",
    "polygon": "Polygon (P)"
}


class ImGuiUI:
    def __init__(self, app: Any):
        self.app = app

    def render(self) -> None:
        """Render the ImGui interface"""
        self._build_sidebar_ui()

    def _build_sidebar_ui(self) -> None:
        """Build the main sidebar UI"""
        imgui.set_next_window_pos(imgui.ImVec2(SIDEBAR_PADDING, SIDEBAR_PADDING), imgui.Cond_.always)
        imgui.set_next_window_size(
            imgui.ImVec2(SIDEBAR_WIDTH, self.app.camera.fb_height - 2 * SIDEBAR_PADDING),
            imgui.Cond_.always
        )
        flags = (
            imgui.WindowFlags_.no_move
            | imgui.WindowFlags_.no_resize
            | imgui.WindowFlags_.no_collapse
            | imgui.WindowFlags_.no_saved_settings
            | imgui.WindowFlags_.no_bring_to_front_on_focus
        )
        imgui.begin("Tools", flags=flags)

        # Mode selection buttons
        for mode_key, mode_name in DRAWING_MODES.items():
            # Highlight active mode with different color
            if self.app.mode == mode_key:
                # Active mode - use a more prominent color (blue)
                imgui.push_style_color(imgui.Col_.button, imgui.ImVec4(0.2, 0.5, 0.8, 1.0))
                imgui.push_style_color(imgui.Col_.button_hovered, imgui.ImVec4(0.3, 0.6, 0.9, 1.0))
                imgui.push_style_color(imgui.Col_.button_active, imgui.ImVec4(0.4, 0.7, 1.0, 1.0))
            else:
                # Inactive mode - use default gray colors
                imgui.push_style_color(imgui.Col_.button, imgui.ImVec4(0.6, 0.6, 0.6, 1.0))
                imgui.push_style_color(imgui.Col_.button_hovered, imgui.ImVec4(0.7, 0.7, 0.7, 1.0))
                imgui.push_style_color(imgui.Col_.button_active, imgui.ImVec4(0.8, 0.8, 0.8, 1.0))

            if imgui.button(mode_name):
                self.app.set_mode(mode_key)

            # Pop the style colors
            imgui.pop_style_color(3)

        imgui.separator()

        # Properties section
        self._build_properties_section()

        imgui.separator()

        # Status information
        imgui.text(f"Zoom: {self.app.camera.zoom_level:.2f}")
        imgui.text(f"Objects: {len(self.app.objects)}")
        imgui.text(f"Selected: {len(self.app.get_selected_shapes())}")
        imgui.text(f"Mode: {self.app.mode}")

        imgui.end()

    def _build_properties_section(self) -> None:
        """Build the properties section showing selected shape information"""
        selected_shapes = self.app.get_selected_shapes()

        if not selected_shapes:
            imgui.text("No selection")
            return

        # Calculate total area and perimeter
        total_area = sum(shape.get_area() for shape in selected_shapes)
        total_perimeter = sum(shape.get_perimeter() for shape in selected_shapes)

        imgui.text("Properties")
        imgui.separator()

        # Display based on selection count
        if len(selected_shapes) == 1:
            # Single selection - show detailed info
            shape = selected_shapes[0]
            shape_type = type(shape).__name__
            imgui.text(f"Type: {shape_type}")
            imgui.text(f"Area: {shape.get_area():.2f}")
            imgui.text(f"Perimeter: {shape.get_perimeter():.2f}")
        else:
            # Multiple selection - show totals
            imgui.text(f"Objects: {len(selected_shapes)}")
            imgui.text(f"Total Area: {total_area:.2f}")
            imgui.text(f"Total Perimeter: {total_perimeter:.2f}")