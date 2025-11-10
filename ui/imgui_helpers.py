"""ImGui helper functions to reduce code duplication and improve UI consistency"""

import logging
from typing import Optional, Callable, Any

from imgui_bundle import imgui

from geometry.vectors import Vec3


class ImGuiHelpers:
    """Collection of helper methods for common ImGui operations."""

    @staticmethod
    def mode_button(label: str, is_active: bool, width: Optional[float] = None) -> bool:
        """Create a mode selection button with active/inactive styling"""
        if is_active:
            imgui.push_style_color(imgui.Col_.button, imgui.ImVec4(0.2, 0.5, 0.8, 1.0))
            imgui.push_style_color(imgui.Col_.button_hovered, imgui.ImVec4(0.3, 0.6, 0.9, 1.0))
            imgui.push_style_color(imgui.Col_.button_active, imgui.ImVec4(0.4, 0.7, 1.0, 1.0))
        else:
            imgui.push_style_color(imgui.Col_.button, imgui.ImVec4(0.6, 0.6, 0.6, 1.0))
            imgui.push_style_color(imgui.Col_.button_hovered, imgui.ImVec4(0.7, 0.7, 0.7, 1.0))
            imgui.push_style_color(imgui.Col_.button_active, imgui.ImVec4(0.8, 0.8, 0.8, 1.0))

        if width is not None:
            imgui.push_item_width(width)

        clicked = imgui.button(label)

        if width is not None:
            imgui.pop_item_width()

        imgui.pop_style_color(3)
        return clicked

    @staticmethod
    def section_header(title: str) -> None:
        """Create a consistent section header with separator"""
        imgui.separator()
        imgui.text(title)

    @staticmethod
    def info_row(label: str, value: str) -> None:
        """Create a consistent info row with label and value."""
        imgui.text(f"{label}: {value}")