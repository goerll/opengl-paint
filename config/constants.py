"""Configuration constants for the OpenGL Paint application"""

class UIConfig:
    """UI-related configuration constants"""
    SIDEBAR_WIDTH = 280
    SIDEBAR_PADDING = 10
    MIN_SHAPE_SIZE = 1.0

    # Rotation range
    ROTATION_MIN = -180.0
    ROTATION_MAX = 180.0

    # Color picker flags
    COLOR_PICKER_FLAGS = [
        "no_alpha",
        "display_rgb",
        "no_side_preview",
        "no_small_preview"
    ]


class DrawingConfig:
    """Drawing and interaction configuration"""
    DEFAULT_CIRCLE_SEGMENTS = 32
    MIN_DRAG_DISTANCE = 2.0

    # Scaling limits
    MIN_SCALE_FACTOR = 0.1
    MAX_SCALE_FACTOR = 10.0

    # Selection tolerance
    SELECTION_TOLERANCE = 5.0