"""
ImGui helper functions to reduce code duplication and improve UI consistency.
Provides common UI patterns and styled components.
"""

from imgui_bundle import imgui
from typing import Optional, Callable, Any
from geometry.vectors import Vec3
import logging


class ImGuiHelpers:
    """Collection of helper methods for common ImGui operations"""

    @staticmethod
    def styled_button(label: str, color: Vec3, width: Optional[float] = None) -> bool:
        """
        Create a button with custom styling based on a color.

        Args:
            label: Button label text
            color: RGB color for the button
            width: Optional button width

        Returns:
            True if button was clicked
        """
        # Set button colors based on the provided color
        imgui.push_style_color(imgui.Col_.button, imgui.ImVec4(color.r, color.g, color.b, 1.0))
        imgui.push_style_color(imgui.Col_.button_hovered, imgui.ImVec4(color.r * 0.8, color.g * 0.8, color.b * 0.8, 1.0))
        imgui.push_style_color(imgui.Col_.button_active, imgui.ImVec4(color.r * 0.6, color.g * 0.6, color.b * 0.6, 1.0))

        if width is not None:
            imgui.push_item_width(width)

        clicked = imgui.button(label)

        if width is not None:
            imgui.pop_item_width()

        imgui.pop_style_color(3)
        return clicked

    @staticmethod
    def mode_button(label: str, is_active: bool, width: Optional[float] = None) -> bool:
        """
        Create a mode selection button with active/inactive styling.

        Args:
            label: Button label text
            is_active: Whether this mode is currently active
            width: Optional button width

        Returns:
            True if button was clicked
        """
        if is_active:
            # Active mode - use blue color scheme
            imgui.push_style_color(imgui.Col_.button, imgui.ImVec4(0.2, 0.5, 0.8, 1.0))
            imgui.push_style_color(imgui.Col_.button_hovered, imgui.ImVec4(0.3, 0.6, 0.9, 1.0))
            imgui.push_style_color(imgui.Col_.button_active, imgui.ImVec4(0.4, 0.7, 1.0, 1.0))
        else:
            # Inactive mode - use gray color scheme
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
    def color_palette_button(label: str, color: Vec3, size: float = 0.0) -> bool:
        """
        Create a small color palette button.

        Args:
            label: Button label (typically empty for color buttons)
            color: RGB color for the button
            size: Optional button size (0 = auto)

        Returns:
            True if button was clicked
        """
        # Set button colors to match the actual color
        imgui.push_style_color(imgui.Col_.button, imgui.ImVec4(color.r, color.g, color.b, 1.0))
        imgui.push_style_color(imgui.Col_.button_hovered, imgui.ImVec4(color.r * 0.8, color.g * 0.8, color.b * 0.8, 1.0))
        imgui.push_style_color(imgui.Col_.button_active, imgui.ImVec4(color.r * 0.6, color.g * 0.6, color.b * 0.6, 1.0))

        if size > 0:
            clicked = imgui.button(label, imgui.ImVec2(size, size))
        else:
            clicked = imgui.button(label)

        imgui.pop_style_color(3)
        return clicked

    @staticmethod
    def section_header(title: str) -> None:
        """
        Create a consistent section header with separator.

        Args:
            title: Section title text
        """
        imgui.separator()
        imgui.text(title)

    @staticmethod
    def info_row(label: str, value: str) -> None:
        """
        Create a consistent info row with label and value.

        Args:
            label: Info label
            value: Info value
        """
        imgui.text(f"{label}: {value}")

    @staticmethod
    def disabled_text(text: str) -> None:
        """
        Display text in a disabled/grayscale style.

        Args:
            text: Text to display
        """
        imgui.push_style_color(imgui.Col_.text, imgui.ImVec4(0.6, 0.6, 0.6, 1.0))
        imgui.text(text)
        imgui.pop_style_color(1)

    @staticmethod
    def center_next_item(width: float) -> None:
        """
        Center the next ImGui item horizontally.

        Args:
            width: Total available width
        """
        item_width = imgui.calc_item_width()
        offset = (width - item_width) * 0.5
        imgui.set_cursor_pos_x(offset)

    @staticmethod
    def help_marker(text: str) -> None:
        """
        Add a help marker (?) with tooltip text.

        Args:
            text: Help text to show in tooltip
        """
        imgui.same_line()
        imgui.text_disabled("(?)")
        if imgui.is_item_hovered():
            imgui.begin_tooltip()
            imgui.push_text_wrap_pos(imgui.get_font_size() * 35.0)
            imgui.text_unformatted(text)
            imgui.pop_text_wrap_pos()
            imgui.end_tooltip()

    @staticmethod
    def spinner(label: str, radius: float, thickness: int, color: imgui.ImVec4) -> None:
        """
        Display a simple spinning loading indicator.

        Args:
            label: Spinner label
            radius: Spinner radius
            thickness: Line thickness
            color: Spinner color
        """
        # This is a placeholder for a spinner implementation
        # In a real implementation, you would draw a rotating circle
        imgui.text(f"{label}...")