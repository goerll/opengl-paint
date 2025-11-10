"""Input filtering utilities to centralize ImGui input capture logic."""

from imgui_bundle import imgui
from typing import Optional, Callable, Any
from config.constants import UIConfig


class InputFilter:
    """Centralized input filtering for ImGui capture states"""

    @staticmethod
    def should_block_mouse_input(xpos: Optional[float] = None, ypos: Optional[float] = None) -> bool:
        """Check if mouse input should be blocked based on ImGui state and position"""
        if imgui.get_io().want_capture_mouse:
            return True

        if xpos is not None and xpos < UIConfig.SIDEBAR_WIDTH:
            return True

        return False

    @staticmethod
    def should_block_keyboard_input() -> bool:
        """Check if keyboard input should be blocked based on ImGui state"""
        return imgui.get_io().want_capture_keyboard

    @staticmethod
    def should_block_any_input(xpos: Optional[float] = None, ypos: Optional[float] = None) -> bool:
        """Check if any input (mouse or keyboard) should be blocked"""
        return (InputFilter.should_block_mouse_input(xpos, ypos) or
                InputFilter.should_block_keyboard_input())

    @staticmethod
    def should_allow_viewport_interaction(xpos: float, ypos: float) -> bool:
        """Check if viewport interaction should be allowed"""
        return not InputFilter.should_block_mouse_input(xpos, ypos)

    @staticmethod
    def log_input_state(xpos: Optional[float] = None, ypos: Optional[float] = None) -> None:
        """Log the current input filtering state (useful for debugging)"""
        import logging

        logger = logging.getLogger("input_filter")
        logger.debug(f"Input state - Mouse captured: {imgui.get_io().want_capture_mouse}, "
                    f"Keyboard captured: {imgui.get_io().want_capture_keyboard}, "
                    f"Mouse pos: ({xpos}, {ypos})")

    @staticmethod
    def is_in_sidebar(xpos: float) -> bool:
        """Check if the mouse position is within the sidebar area"""
        return xpos < UIConfig.SIDEBAR_WIDTH

    @staticmethod
    def filter_mouse_callback(callback_fn: Callable[..., Any]):
        """Decorator to filter mouse callbacks based on ImGui state"""
        def wrapped_callback(*args: Any, **kwargs: Any) -> Any:
            xpos = None
            if len(args) >= 3:
                xpos = args[1]

            if InputFilter.should_block_mouse_input(xpos):
                return

            return callback_fn(*args, **kwargs)

        return wrapped_callback

    @staticmethod
    def filter_keyboard_callback(callback_fn: Callable[..., Any]):
        """Decorator to filter keyboard callbacks based on ImGui state"""
        def wrapped_callback(*args: Any, **kwargs: Any) -> Any:
            if InputFilter.should_block_keyboard_input():
                return

            return callback_fn(*args, **kwargs)

        return wrapped_callback