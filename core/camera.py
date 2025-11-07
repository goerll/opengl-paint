import glm
import logging
from geometry.vectors import Vec2


class Camera:
    def __init__(self, width: int = 800, height: int = 800):
        self.width: int = width
        self.height: int = height
        self.fb_width: int = width
        self.fb_height: int = height

        # Camera properties
        self.x: float = 0.0
        self.y: float = 0.0
        self.zoom_level: float = 1.0

    def update_viewport(self, width: int, height: int, fb_width: int, fb_height: int) -> None:
        """Update camera viewport dimensions"""
        self.width = width
        self.height = height
        self.fb_width = fb_width
        self.fb_height = fb_height
        logging.info(f"Camera viewport updated to {fb_width}x{fb_height}")

    def screen_to_normalized(self, xpos: float, ypos: float) -> tuple[float, float]:
        """Convert screen coordinates to NDC"""
        # Account for framebuffer scaling
        scale_x = self.fb_width / self.width if self.width != 0 else 1.0
        scale_y = self.fb_height / self.height if self.height != 0 else 1.0

        # Scale mouse position to framebuffer coordinates
        fb_x = xpos * scale_x
        fb_y = ypos * scale_y

        ndc_x = (2 * fb_x / self.fb_width) - 1
        ndc_y = 1 - (2 * fb_y / self.fb_height)
        logging.debug("Screen to normalized: (%f, %f) -> (%f, %f)", xpos, ypos, ndc_x, ndc_y)
        return ndc_x, ndc_y

    def screen_to_world(self, xpos: float, ypos: float) -> tuple[float, float]:
        """Convert screen-space (pixels) into world-space coordinates"""
        ndc_x, ndc_y = self.screen_to_normalized(xpos, ypos)

        # Use framebuffer aspect ratio for consistency with projection matrix
        aspect_ratio = self.fb_width / self.fb_height if self.fb_height != 0 else 1.0

        view_height = 2.0 / self.zoom_level
        view_width = view_height * aspect_ratio

        world_x = self.x + ndc_x * (view_width / 2.0)
        world_y = self.y + ndc_y * (view_height / 2.0)

        logging.debug(
            "Screen to world: screen(%.2f, %.2f) ndc(%.2f, %.2f) -> world(%.2f, %.2f)",
            xpos, ypos, ndc_x, ndc_y, world_x, world_y
        )

        return world_x, world_y

    def create_projection_matrix(self) -> glm.mat4:
        """Create orthographic projection matrix"""
        aspect_ratio = self.fb_width / self.fb_height if self.fb_height != 0 else 1.0
        view_height = 2.0 / self.zoom_level
        view_width = view_height * aspect_ratio

        left = -view_width / 2.0
        right = view_width / 2.0
        bottom = -view_height / 2.0
        top = view_height / 2.0

        return glm.ortho(left, right, bottom, top, -1.0, 1.0)

    def create_view_matrix(self) -> glm.mat4:
        """Create view matrix for camera position"""
        return glm.translate(  # type: ignore[attr-defined]
            glm.mat4(1.0), glm.vec3(-self.x, -self.y, 0.0)
        )

    def create_model_matrix(self) -> glm.mat4:
        """Create identity model matrix"""
        return glm.mat4(1.0)

    def zoom_at_point(self, xpos: float, ypos: float, zoom_delta: float) -> None:
        """Zoom camera at specific screen point"""
        # Get world position before zoom
        wx, wy = self.screen_to_world(xpos, ypos)

        # Apply zoom
        zoom_speed = 0.1
        if zoom_delta > 0:
            self.zoom_level *= 1.0 + zoom_speed
        elif zoom_delta < 0:
            self.zoom_level *= 1.0 - zoom_speed

        self.zoom_level = max(0.1, min(self.zoom_level, 10.0))

        # Adjust camera to keep the same world point under cursor
        new_wx, new_wy = self.screen_to_world(xpos, ypos)
        self.x += wx - new_wx
        self.y += wy - new_wy

        logging.info(f"Zoom level: {self.zoom_level}")

    def pan(self, delta_x: float, delta_y: float) -> None:
        """Pan camera by given delta"""
        self.x += delta_x
        self.y += delta_y

    def reset(self) -> None:
        """Reset camera to default position and zoom"""
        self.x = 0.0
        self.y = 0.0
        self.zoom_level = 1.0
        logging.info("Camera reset to default position")