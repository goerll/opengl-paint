"""
Configuration constants for the OpenGL Paint application.
Centralized constants to improve maintainability and reduce magic numbers.
"""


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


class CameraConfig:
    """Camera and viewport configuration"""
    DEFAULT_ZOOM = 1.0
    MIN_ZOOM = 0.1
    MAX_ZOOM = 10.0
    ZOOM_SPEED = 0.1

    # Pan speed
    PAN_SPEED = 1.0


class ColorPalette:
    """Standard color palette for the application"""
    RED = (1.0, 0.0, 0.0)
    GREEN = (0.0, 1.0, 0.0)
    BLUE = (0.0, 0.0, 1.0)
    YELLOW = (1.0, 1.0, 0.0)
    CYAN = (0.0, 1.0, 1.0)
    MAGENTA = (1.0, 0.0, 1.0)
    WHITE = (1.0, 1.0, 1.0)
    BLACK = (0.0, 0.0, 0.0)
    ORANGE = (1.0, 0.5, 0.0)
    PURPLE = (0.5, 0.0, 1.0)
    PINK = (1.0, 0.75, 0.8)
    GRAY = (0.5, 0.5, 0.5)

    @classmethod
    def get_all_colors(cls):
        """Get all predefined colors as a dictionary"""
        return {
            "Red": cls.RED,
            "Green": cls.GREEN,
            "Blue": cls.BLUE,
            "Yellow": cls.YELLOW,
            "Cyan": cls.CYAN,
            "Magenta": cls.MAGENTA,
            "White": cls.WHITE,
            "Black": cls.BLACK
        }


class LoggingConfig:
    """Logging configuration"""
    DEFAULT_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Specific loggers
    INPUT_LOGGER = "input"
    RENDER_LOGGER = "renderer"
    UI_LOGGER = "ui"
    SHAPE_LOGGER = "shapes"