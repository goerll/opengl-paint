from imgui_bundle import imgui
from typing import Any
import logging
from geometry.vectors import Vec3
from config.constants import UIConfig, ColorPalette
from ui.imgui_helpers import ImGuiHelpers

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
        imgui.set_next_window_pos(imgui.ImVec2(UIConfig.SIDEBAR_PADDING, UIConfig.SIDEBAR_PADDING), imgui.Cond_.always)
        imgui.set_next_window_size(
            imgui.ImVec2(UIConfig.SIDEBAR_WIDTH, self.app.camera.fb_height - 2 * UIConfig.SIDEBAR_PADDING),
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
            if ImGuiHelpers.mode_button(mode_name, self.app.mode == mode_key):
                self.app.set_mode(mode_key)

        imgui.separator()

        # Properties section
        self._build_properties_section()

        imgui.separator()

        # Status information
        imgui.text(f"Zoom: {self.app.camera.zoom_level:.2f}")
        imgui.text(f"Objects: {len(self.app.objects)}")
        imgui.text(f"Selected: {len(self.app.get_selected_shapes())}")

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
            ImGuiHelpers.info_row("Type", shape_type)
            ImGuiHelpers.info_row("Area", f"{shape.get_area():.2f}")
            ImGuiHelpers.info_row("Perimeter", f"{shape.get_perimeter():.2f}")
        else:
            # Multiple selection - show totals
            ImGuiHelpers.info_row("Objects", str(len(selected_shapes)))
            ImGuiHelpers.info_row("Total Area", f"{total_area:.2f}")
            ImGuiHelpers.info_row("Total Perimeter", f"{total_perimeter:.2f}")


        # Rotation controls


        # Color picker
        if selected_shapes:
            ImGuiHelpers.section_header("Color")

            # Get the current color from the first selected shape
            current_color = selected_shapes[0].get_color()
            # Convert Vec3 to ImVec4 (add alpha = 1.0)
            color_imvec = imgui.ImVec4(current_color.r, current_color.g, current_color.b, 1.0)

            # Create color picker with additional flags for better interaction
            color_flags = 0
            for flag in UIConfig.COLOR_PICKER_FLAGS:
                color_flags |= getattr(imgui.ColorEditFlags_, flag)

            changed, new_color = imgui.color_picker4("Color", color_imvec, color_flags)

            if changed:
                # Convert ImVec4 back to Vec3 (ImVec4 uses x,y,z,w attributes)
                new_color_vec3 = Vec3(new_color.x, new_color.y, new_color.z)
                # Apply color to all selected shapes
                for shape in selected_shapes:
                    shape.color = new_color_vec3
                logging.info(f"Changed color of {len(selected_shapes)} shape(s) to RGB({new_color.x:.2f}, {new_color.y:.2f}, {new_color.z:.2f})")
        

        if selected_shapes:
            ImGuiHelpers.section_header("Rotation")
            # Get current rotation from first selected shape
            current_rotation = selected_shapes[0].get_rotation()

            # Rotation slider (180 to -180 degrees for intuitive UX)
            changed, new_rotation = imgui.slider_float(
                "Rotation", current_rotation, UIConfig.ROTATION_MAX, UIConfig.ROTATION_MIN, "%.1f°"
            )

            if changed:
                # Apply rotation to all selected shapes
                for shape in selected_shapes:
                    shape.set_rotation(new_rotation)
                logging.info(f"Rotated {len(selected_shapes)} shape(s) to {new_rotation:.1f}°")