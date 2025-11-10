import glfw
from OpenGL.GL import (
    glClear,
    glClearColor,
    glViewport,
    GL_COLOR_BUFFER_BIT,
)
import logging
from typing import Any, cast

from imgui_bundle import imgui
from imgui_bundle.python_backends.glfw_backend import GlfwRenderer

from core.camera import Camera
from core.input_manager import InputManager
from graphics.renderer import Renderer
from systems.selection_system import SelectionSystem
from systems.shape_factory import ShapeFactory
from ui.imgui_ui import ImGuiUI


class DrawingModes:
    """Constants for different drawing modes."""
    SELECT = "select"
    TRIANGLE = "triangle"
    CIRCLE = "circle"
    RECTANGLE = "rectangle"
    POLYGON = "polygon"


class GraphicsApp:
    """Main application class for the OpenGL Paint application."""

    def __init__(self, width: int = 800, height: int = 800) -> None:
        """Initialize the graphics application."""
        self.width: int = width
        self.height: int = height
        self.window: Any = None

        self.camera = Camera(width, height)
        self.input_manager = InputManager()
        self.renderer: Renderer | None = None
        self.ui: ImGuiUI | None = None

        self.mode: str = DrawingModes.SELECT
        self.objects: list[Any] = []
        self.temp_shape: Any | None = None

        self.selection_system = SelectionSystem()
        self.shape_factory = ShapeFactory()
        self.imgui_impl: Any | None = None

    def get_selected_shapes(self) -> list[Any]:
        """Get selected shapes from selection system"""
        return self.selection_system.get_selected_shapes()

    def set_mode(self, new_mode: str) -> None:
        """Set a new drawing mode and clear any related state"""
        self.mode = new_mode
        self.shape_factory.clear_editing_state()
        self.selection_system.clear_selection()
        logging.info(f"Mode changed to: {new_mode}")

    def init_window(self) -> bool:
        """Initialize GLFW window and OpenGL context"""
        if not glfw.init():
            logging.error("GLFW could not be initialized!")
            return False

        glfw.window_hint(glfw.SCALE_TO_MONITOR, glfw.FALSE)
        logging.info("GLFW initialized")

        self.window = glfw.create_window(self.width, self.height, "OpenGL", None, None)

        if not self.window:
            logging.error("Window could not be created!")
            glfw.terminate()
            return False

        logging.info("Window created")
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        glfw.set_window_user_pointer(self.window, self)

        win_w, win_h = glfw.get_window_size(self.window)
        fb_w, fb_h = glfw.get_framebuffer_size(self.window)
        self.width, self.height = win_w, win_h
        self.camera.update_viewport(win_w, win_h, fb_w, fb_h)
        glViewport(0, 0, fb_w, fb_h)

        logging.info("Window set")

        imgui.create_context()
        self.imgui_impl = GlfwRenderer(self.window)
        self.ui = ImGuiUI(self)
        self.input_manager.initialize(self.window, self, self.imgui_impl)

        logging.info("Callbacks set")
        return True

    def init_renderer(self) -> bool:
        """Initialize the renderer"""
        self.renderer = Renderer()
        if not self.renderer.init():
            logging.error("Renderer could not be initialized!")
            return False
        return True

    def add_shape(self, vertices: list[float]) -> None:
        """Add a shape based on current mode"""
        shape = self.shape_factory.create_shape(self.mode, vertices)
        if shape:
            self.objects.append(shape)
            logging.debug(f"{self.mode.capitalize()} created. Total shapes: {len(self.objects)}")

    def render(self) -> None:
        """Render the scene"""
        glClear(GL_COLOR_BUFFER_BIT)

        renderer = cast(Renderer, self.renderer)
        renderer.set_matrices(
            self.camera.create_projection_matrix(),
            self.camera.create_view_matrix(),
            self.camera.create_model_matrix(),
        )

        for obj in self.objects:
            renderer.render_shape(obj)

        if self.temp_shape:
            renderer.render_shape(self.temp_shape)

    def run(self) -> None:
        """Main application loop"""
        if not self.init_window():
            return

        if not self.init_renderer():
            return

        glClearColor(0.1, 0.1, 0.1, 1.0)

        self._print_controls()

        while not glfw.window_should_close(self.window):
            glfw.poll_events()

            imgui.new_frame()

            self.imgui_impl.process_inputs()

            if not self.shape_factory.is_editing():
                self.temp_shape = None

            self.ui.render()
            self.render()
            imgui.render()
            self.imgui_impl.render(imgui.get_draw_data())

            glfw.swap_buffers(self.window)

        self._cleanup()

    def _print_controls(self) -> None:
        """Print control instructions"""
        print("=== OpenGL Paint ===")
        print("Controls:")
        print("  S - Select mode")
        print("  T - Triangle mode")
        print("  C - Circle mode")
        print("  R - Rectangle mode")
        print("  P - Polygon mode")
        print("  Mouse wheel - Zoom in/out")
        print("  Space - Reset camera and zoom")
        print("  Click and drag to draw shapes")
        print("  Hold Shift while drawing:")
        print("    - Rectangle: Constrain to square (1:1 ratio)")
        print("    - Circle: Constrain to perfect circle")
        print("    - Triangle: Constrain to equilateral triangle")
        print("  D - Delete selected shapes")
        print("  ESC - Exit")
        print(f"Starting in {self.mode} mode")
        print("=" * 20)

    def _cleanup(self) -> None:
        """Clean up resources."""
        try:
            self.imgui_impl.shutdown()
        except Exception:
            pass
        try:
            imgui.destroy_context()
        except Exception:
            pass
        glfw.terminate()