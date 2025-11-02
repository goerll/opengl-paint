import glfw
from OpenGL.GL import (
    glClear,
    glClearColor,
    glViewport,
    GL_COLOR_BUFFER_BIT,
)
import glm
import numpy as np
from typing import Any, cast
from renderer import Renderer
from shapes import Triangle, Circle, Rectangle, Polygon
from math_utils import Vec2, Vec3
import logging

logging.basicConfig(level=logging.INFO)

# Globals
window_width = 800
window_height = 800
white = Vec3(1.0, 1.0, 1.0)

class GraphicsApp:
    def __init__(self, width: int = 800, height: int = 800) -> None:
        # Properties
        self.width: int = width
        self.height: int = height
        self.window: None = None
        self.renderer: Renderer | None = None
        self.fb_width: int = width
        self.fb_height: int = height

        # State
        self.mode: str = "select"
        self.editing_shape: bool = False
        self.panning: bool = False
        self.dragging: bool = False
        self.objects: list[Triangle | Circle | Rectangle | Polygon] = []
        self.ui: list[Triangle | Circle | Rectangle | Polygon] = []
        self.selected_shapes: list[Triangle | Circle | Rectangle | Polygon] = []

        # Camera
        self.camera_x: float = 0.0
        self.camera_y: float = 0.0
        self.zoom_level: float = 1.0

        # Temporary "cache" variables
        self.vertices: list[float] = []
        self.editing_origin: Vec2 = Vec2(0.0, 0.0)

    def init_window(self) -> bool:
        if not glfw.init():
            logging.error("GLFW could not be initialized!")
            return False

        glfw.window_hint(glfw.SCALE_TO_MONITOR, glfw.FALSE)

        logging.info("GLFW initialized")

        # Window creation
        self.window = glfw.create_window(self.width, self.height, "OpenGL", None, None)

        if not self.window:
            logging.error("Window could not be created!")
            glfw.terminate()
            return False

        logging.info("Window created")

        # Set window
        glfw.make_context_current(self.window)
        glfw.set_window_user_pointer(self.window, self)

        win_w, win_h = glfw.get_window_size(self.window)
        fb_w, fb_h = glfw.get_framebuffer_size(self.window)
        self.width, self.height = win_w, win_h
        self.fb_width, self.fb_height = fb_w, fb_h
        glViewport(0, 0, fb_w, fb_h)

        logging.info("Window set")

        # Set callbacks
        glfw.set_mouse_button_callback(self.window, self.mouse_callback)
        glfw.set_cursor_pos_callback(self.window, self.cursor_pos_callback)
        glfw.set_scroll_callback(self.window, self.scroll_callback)
        glfw.set_key_callback(self.window, self.key_callback)
        glfw.set_framebuffer_size_callback(self.window, self.framebuffer_size_callback)

        logging.info("Callbacks set")

        return True

    @staticmethod
    def framebuffer_size_callback(window: Any, width: int, height: int) -> None:
        app: GraphicsApp = glfw.get_window_user_pointer(window)
        glViewport(0, 0, width, height)
        logging.info(f"Viewport updated to {width}x{height}")
        app.width, app.height = glfw.get_window_size(window)
        app.fb_width, app.fb_height = width, height

    def init_renderer(self) -> bool:
        self.renderer = Renderer()
        if not self.renderer.init():
            logging.error("Renderer could not be initialized!")
            return False
        return True

    def screen_to_normalized(self, xpos: float, ypos: float) -> tuple[float, float]:
        """Convert screen coordinates to NDC"""
        ndc_x = (2 * xpos / self.width) - 1
        ndc_y = 1 - (2* ypos / self.height)
        logging.debug("Screen to normalized: (%f, %f) -> (%f, %f)", xpos, ypos, ndc_x, ndc_y)
        return ndc_x, ndc_y

    def screen_to_world(self, xpos: float, ypos: float) -> tuple[float, float]:
        """Convert screen-space (pixels) into world-space coordinates"""
        ndc_x, ndc_y = self.screen_to_normalized(xpos, ypos)

        aspect_ratio = self.width/self.height if self.height != 0 else 1.0

        view_height = 2.0 / self.zoom_level
        view_width = view_height * aspect_ratio

        world_x = self.camera_x + ndc_x * (view_width / 2.0)
        world_y = self.camera_y + ndc_y * (view_height / 2.0)

        logging.debug(
            "Screen to world: screen(%.2f, %.2f) ndc(%.2f, %.2f) -> world(%.2f, %.2f)",
            xpos, ypos, ndc_x, ndc_y, world_x, world_y
        )

        return world_x, world_y

    def create_projection_matrix(self) -> glm.mat4:
        aspect_ratio = self.fb_width / self.fb_height if self.fb_height != 0 else 1.0
        view_height = 2.0 / self.zoom_level
        view_width = view_height * aspect_ratio

        left = -view_width / 2.0
        right = view_width / 2.0
        bottom = -view_height / 2.0
        top = view_height / 2.0

        return glm.ortho(left, right, bottom, top, -1.0, 1.0)

    def create_view_matrix(self) -> glm.mat4:
        return glm.translate(
            glm.mat4(1.0), glm.vec3(-self.camera_x, -self.camera_y, 0.0)
        )

    def create_model_matrix(self) -> glm.mat4:
        """Create identity model matrix"""
        return glm.mat4(1.0)

    @staticmethod
    def mouse_callback(window: Any, button: int, action: int, mods: int) -> None:
        app: GraphicsApp = glfw.get_window_user_pointer(window)

        xpos, ypos = glfw.get_cursor_pos(window)
        wx, wy = app.screen_to_world(xpos, ypos)
        click_point = Vec2(wx, wy)
        app.editing_origin = click_point
        
        if button == glfw.MOUSE_BUTTON_LEFT:
            if action == glfw.PRESS:
                app._handle_left_press(window, click_point)
            elif action == glfw.RELEASE:
                app._handle_left_release()
        
        elif button == glfw.MOUSE_BUTTON_RIGHT:
            app._handle_right_click(action, wx, wy)

    def _handle_left_press(self, window: Any, click_point: Vec2) -> None:
        match self.mode:
            case "select":
                self._handle_selection(window, click_point)
            case "triangle" | "circle" | "rectangle":
                self._start_primitive_creation(click_point)
            case "polygon":
                self._handle_polygon_creation(window, click_point)
            case _:
                logging.error(f"Invalid mode: {self.mode}")

    def _handle_left_release(self) -> None:
        """Handle left mouse release based on current mode"""
        match self.mode:
            case "select":
                self.dragging = False
            case "triangle" | "circle" | "rectangle":
                self._finish_primitive_creation()
            case "polygon":
                pass
            case _:
                logging.error(f"Invalid mode: {self.mode}")

    def _handle_right_click(self, action: int, wx: float, wy: float) -> None:
        """Handle right mouse button for panning"""
        match action:
            case glfw.PRESS:
                self.panning = True
                logging.info("Started panning at (%.2f, %.2f)", wx, wy)
            case glfw.RELEASE:
                self.panning = False
                logging.info("Stopped panning at (%.2f, %.2f)", wx, wy)
            case _:
                pass

    def _handle_selection(self, window: Any, click_point: Vec2) -> None:
        """Handle shape selection logic"""
        clicked_shape = self._find_clicked_shape(click_point)
        shift_pressed = glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS
        
        if clicked_shape:
            self._select_shape(clicked_shape, shift_pressed)
            self.dragging = True
            logging.info(f"Selected {type(clicked_shape).__name__}")
        else:
            self._clear_selection()
            self.dragging = False
            logging.info("Deselected")

    def _find_clicked_shape(self, click_point: Vec2):
        """Find the topmost shape at click point"""
        for shape in reversed(self.objects):
            if shape.contains_point(click_point):
                return shape
        return None

    def _select_shape(self, clicked_shape, shift_pressed: bool) -> None:
        """Select a shape with proper multi-selection handling"""
        clicked_shape.thickness = 2
        
        if shift_pressed:
            # Multi-select: add if not already selected
            if clicked_shape not in self.selected_shapes:
                self.selected_shapes.append(clicked_shape)
        else:
            # Single select: clear previous and select new
            if clicked_shape not in self.selected_shapes:
                self._reset_thickness_for_selected()
                self.selected_shapes = [clicked_shape]

    def _clear_selection(self) -> None:
        """Clear all selected shapes"""
        self._reset_thickness_for_selected()
        self.selected_shapes.clear()

    def _reset_thickness_for_selected(self) -> None:
        """Reset thickness for all currently selected shapes"""
        for shape in self.selected_shapes:
            shape.thickness = 1

    def _start_primitive_creation(self, click_point: Vec2) -> None:
        """Start creating a primitive shape"""
        self.editing_shape = True
        self.vertices = [click_point.x, click_point.y]
        self.add_shape([click_point.x, click_point.y] * 2)

    def _finish_primitive_creation(self) -> None:
        """Finish creating a primitive shape"""
        self.editing_shape = False
        self.vertices.clear()
        logging.info(f"Shape {self.mode} created at {self.editing_origin}. Total shapes: {len(self.objects)}")

    def _handle_polygon_creation(self, window: Any, click_point: Vec2) -> None:
        """Handle polygon vertex addition and completion"""
        shift_pressed = glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS
        
        # Add vertex
        if not self.vertices:  # First vertex
            self.editing_shape = True
            self.vertices.extend([click_point.x, click_point.y])
            self.add_shape([click_point.x, click_point.y] * 2)
        else:  # Additional vertices
            self.vertices.extend([click_point.x, click_point.y])
        
        logging.info("Added vertex (%.2f, %.2f) to polygon", click_point.x, click_point.y)
        
        # Complete polygon if shift pressed
        if shift_pressed and len(self.vertices) >= 6:  # At least 3 vertices
            self.editing_shape = False
            vertex_count = len(self.vertices) // 2
            self.vertices.clear()
            logging.info(f"Polygon created with {vertex_count} vertices (Total shapes: {len(self.objects)})")

    @staticmethod
    def cursor_pos_callback(window: Any, xpos: float, ypos: float) -> None:
        app: GraphicsApp = glfw.get_window_user_pointer(window)
        wx, wy = app.screen_to_world(xpos, ypos)

        if app.dragging and app.selected_shapes:
            current_point = Vec2(wx, wy)
            delta = current_point - app.editing_origin
            for shape in app.selected_shapes:
                shape.move(delta)
            logging.info(f"Moved shapes")
            app.editing_origin = current_point

        elif app.editing_shape:
            app.vertices.extend([wx, wy])

            app.objects.pop()
            app.add_shape(app.vertices)

            app.vertices = app.vertices[:-2]

        elif app.panning:
            delta_x = app.editing_origin.x - wx
            delta_y = app.editing_origin.y - wy

            app.camera_x += delta_x
            app.camera_y += delta_y

    @staticmethod
    def scroll_callback(window: Any, xoffset: float, yoffset: float) -> None:
        app: GraphicsApp = glfw.get_window_user_pointer(window)

        xpos, ypos = glfw.get_cursor_pos(window)

        wx, wy = app.screen_to_world(xpos, ypos)

        zoom_speed = 0.1
        if yoffset > 0:
            app.zoom_level *= 1.0 + zoom_speed
        elif yoffset < 0:
            app.zoom_level *= 1.0 - zoom_speed

        app.zoom_level = max(0.1, min(app.zoom_level, 10.0))

        new_wx, new_wy = app.screen_to_world(xpos, ypos)

        app.camera_x += wx - new_wx
        app.camera_y += wy - new_wy

        logging.info(f"Zoom level: {app.zoom_level}")


    @staticmethod
    def key_callback(window: Any, key: int, scancode: int, action: int, mods: int) -> None:
        app: GraphicsApp = glfw.get_window_user_pointer(window)
        if action == glfw.PRESS:
            match key:
                case glfw.KEY_S:
                    app.mode = "select"
                    logging.info("Mode:Select")

                case glfw.KEY_T:
                    app.mode = "triangle"
                    logging.info("Mode:Triangle")

                case glfw.KEY_C:
                    app.mode = "circle"
                    logging.info("Mode:Circle")

                case glfw.KEY_R:
                    app.mode = "rectangle"
                    logging.info("Mode:Rectangle")

                case glfw.KEY_P:
                    app.mode = "polygon"
                    logging.info("Mode:Polygon")

                case glfw.KEY_SPACE:
                    app.zoom_level = 1.0
                    app.camera_x = 0.0
                    app.camera_y = 0.0
                    logging.info("Reset camera and zoom")

                case glfw.KEY_D:
                    if app.selected_shapes:
                        for shape in app.selected_shapes:
                            app.objects.remove(shape)
                        app.selected_shapes.clear()
                        logging.info("Deleted selected shapes")

                case glfw.KEY_ESCAPE:
                    glfw.set_window_should_close(window, True)

                case _:
                    logging.debug("Untreated key input")

    def add_shape(self, vertices: list[float]) -> None:
        white: Vec3 = Vec3(1.0, 1.0, 1.0)

        match self.mode:
            case "triangle":
                self.objects.append(Triangle(vertices, white))

            case "circle":
                self.objects.append(Circle(vertices, white))

            case "rectangle":
                self.objects.append(Rectangle(vertices, white))

            case "polygon":
                self.objects.append(Polygon(vertices, white))

            case _:
                logging.error(f"Invalid shape: {self.mode}")
                return

        logging.debug(f"{self.mode.capitalize()} created at {self.editing_origin} (Total shapes: {len(self.objects)})")

    def add_polygon(self, vertices: list[float]) -> None:
        self.objects.append(Polygon(vertices, white))
        logging.info(f"Polygon created with {len(vertices)//2} vertices (Total shapes: {len(self.objects)})")

    def render(self) -> None:
        glClear(GL_COLOR_BUFFER_BIT)

        renderer = cast(Renderer, self.renderer)
        renderer.set_matrices(
            self.create_projection_matrix(),
            self.create_view_matrix(),
            self.create_model_matrix(),
        )

        for obj in self.objects:
            renderer.render_shape(obj)

        window = cast(Any, self.window)
        glfw.swap_buffers(window)

    def run(self) -> None:
        if not self.init_window():
            return

        if not self.init_renderer():
            return

        glClearColor(0.1, 0.1, 0.1, 1.0)

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
        print("  ESC - Exit")
        print(f"Starting in {self.mode} mode")
        print("=" * 20)

        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            self.render()

        glfw.terminate()


if __name__ == "__main__":
    app = GraphicsApp(window_width, window_height)
    app.run()
