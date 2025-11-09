"""
Input filtering utilities to centralize ImGui input capture logic.
Eliminates duplication of input filtering code across the application.
"""

from imgui_bundle import imgui
from typing import Optional
from config.constants import UIConfig


class InputFilter:
    """Centralized input filtering for ImGui capture states"""

    @staticmethod
    def should_block_mouse_input(xpos: Optional[float] = None, ypos: Optional[float] = None) -> bool:
        """
        Check if mouse input should be blocked based on ImGui state and position.

        Args:
            xpos: Optional mouse X position (for sidebar blocking)
            ypos: Optional mouse Y position (for sidebar blocking)

        Returns:
            True if mouse input should be blocked
        """
        # Check if ImGui wants to capture mouse input
        if imgui.get_io().want_capture_mouse:
            return True

        # Block viewport input if we're in the sidebar area but ImGui doesn't explicitly want capture
        # (e.g., clicking on empty sidebar space)
        if xpos is not None and xpos < UIConfig.SIDEBAR_WIDTH:
            return True

        return False

    @staticmethod
    def should_block_keyboard_input() -> bool:
        """
        Check if keyboard input should be blocked based on ImGui state.

        Returns:
            True if keyboard input should be blocked
        """
        return imgui.get_io().want_capture_keyboard

    @staticmethod
    def should_block_any_input(xpos: Optional[float] = None, ypos: Optional[float] = None) -> bool:
        """
        Check if any input (mouse or keyboard) should be blocked.

        Args:
            xpos: Optional mouse X position
            ypos: Optional mouse Y position

        Returns:
            True if any input should be blocked
        """
        return (InputFilter.should_block_mouse_input(xpos, ypos) or
                InputFilter.should_block_keyboard_input())

    @staticmethod
    def should_allow_viewport_interaction(xpos: float, ypos: float) -> bool:
        """
        Check if viewport interaction should be allowed.

        Args:
            xpos: Mouse X position
            ypos: Mouse Y position

        Returns:
            True if viewport interaction should be allowed
        """
        return not InputFilter.should_block_mouse_input(xpos, ypos)

    @staticmethod
    def log_input_state(xpos: Optional[float] = None, ypos: Optional[float] = None) -> None:
        """
        Log the current input filtering state (useful for debugging).

        Args:
            xpos: Optional mouse X position
            ypos: Optional mouse Y position
        """
        import logging

        logger = logging.getLogger("input_filter")
        logger.debug(f"Input state - Mouse captured: {imgui.get_io().want_capture_mouse}, "
                    f"Keyboard captured: {imgui.get_io().want_capture_keyboard}, "
                    f"Mouse pos: ({xpos}, {ypos})")

    @staticmethod
    def is_in_sidebar(xpos: float) -> bool:
        """
        Check if the mouse position is within the sidebar area.

        Args:
            xpos: Mouse X position

        Returns:
            True if mouse is in sidebar area
        """
        return xpos < UIConfig.SIDEBAR_WIDTH

    @staticmethod
    def filter_mouse_callback(callback_fn):
        """
        Decorator to filter mouse callbacks based on ImGui state.

        Args:
            callback_fn: The callback function to wrap

        Returns:
            Wrapped callback function that checks input filtering
        """
        def wrapped_callback(*args, **kwargs):
            # Extract position from callback args if available
            xpos = None
            if len(args) >= 3:
                xpos = args[1]  # Typical GLFW callback signature: (window, xpos, ypos, ...)

            if InputFilter.should_block_mouse_input(xpos):
                return  # Block the callback

            return callback_fn(*args, **kwargs)

        return wrapped_callback

    @staticmethod
    def filter_keyboard_callback(callback_fn):
        """
        Decorator to filter keyboard callbacks based on ImGui state.

        Args:
            callback_fn: The callback function to wrap

        Returns:
            Wrapped callback function that checks input filtering
        """
        def wrapped_callback(*args, **kwargs):
            if InputFilter.should_block_keyboard_input():
                return  # Block the callback

            return callback_fn(*args, **kwargs)

        return wrapped_callback