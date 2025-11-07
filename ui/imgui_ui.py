from imgui_bundle import imgui
from typing import Any
import logging

# UI Constants
SIDEBAR_PADDING = 10
SIDEBAR_WIDTH = 280

# Drawing modes
DRAWING_MODES = {
    "select": "Select",
    "triangle": "Triangle",
    "circle": "Circle",
    "rectangle": "Rectangle",
    "polygon": "Polygon"
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
            if imgui.button(mode_name):
                self.app.mode = mode_key
                logging.info(f"Mode:{mode_name}")

        imgui.separator()

        # Status information
        imgui.text(f"Zoom: {self.app.camera.zoom_level:.2f}")
        imgui.text(f"Objects: {len(self.app.objects)}")
        imgui.text(f"Selected: {len(self.app.get_selected_shapes())}")
        imgui.text(f"Mode: {self.app.mode}")

        imgui.end()