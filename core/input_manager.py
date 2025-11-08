import glfw
from typing import Any, Callable
from geometry.vectors import Vec2
import logging


class InputManager:
    def __init__(self):
        self.window: Any = None
        self.app: Any = None  # Reference to main app
        self.imgui_impl: Any = None

        # Input state
        self.panning: bool = False
        self.dragging: bool = False
        self.editing_origin: Vec2 = Vec2(0.0, 0.0)

    def initialize(self, window: Any, app: Any, imgui_impl: Any) -> None:
        """Initialize input manager with window and app references"""
        self.window = window
        self.app = app
        self.imgui_impl = imgui_impl

        # Set GLFW callbacks
        glfw.set_mouse_button_callback(self.window, self.mouse_callback)
        glfw.set_cursor_pos_callback(self.window, self.cursor_pos_callback)
        glfw.set_scroll_callback(self.window, self.scroll_callback)
        glfw.set_key_callback(self.window, self.key_callback)
        glfw.set_framebuffer_size_callback(self.window, self.framebuffer_size_callback)

    @staticmethod
    def framebuffer_size_callback(window: Any, width: int, height: int) -> None:
        """Handle framebuffer resize"""
        from OpenGL.GL import glViewport

        app = glfw.get_window_user_pointer(window)
        if hasattr(app, 'camera'):
            app.camera.update_viewport(
                *glfw.get_window_size(window),
                width, height
            )
            # Update OpenGL viewport to match framebuffer size
            glViewport(0, 0, width, height)

    def mouse_callback(self, window: Any, button: int, action: int, mods: int) -> None:
        """Handle mouse button events"""
        from imgui_bundle import imgui

        # Check if ImGui wants to capture the mouse input first
        io = imgui.get_io()
        xpos, ypos = glfw.get_cursor_pos(window)
        io.add_mouse_pos_event(xpos, ypos)
        io.add_mouse_button_event(button, action == glfw.PRESS)
        self.imgui_impl.mouse_button_callback(window, button, action, mods)

        # Only process viewport input if ImGui doesn't want it
        if io.want_capture_mouse:
            return

        # Convert to world coordinates and set editing origin only for viewport clicks
        wx, wy = self.app.camera.screen_to_world(xpos, ypos)
        click_point = Vec2(wx, wy)
        self.editing_origin = click_point

        if button == glfw.MOUSE_BUTTON_LEFT:
            if action == glfw.PRESS:
                self._handle_left_press(click_point)
            elif action == glfw.RELEASE:
                self._handle_left_release()

        elif button == glfw.MOUSE_BUTTON_RIGHT:
            self._handle_right_click(action)

    def _handle_left_press(self, click_point: Vec2) -> None:
        """Handle left mouse press"""
        if self.app.mode == "select":
            self.app.selection_system.handle_selection(self.window, click_point, self.app.objects)
            self.dragging = True if self.app.get_selected_shapes() else False
        elif self.app.mode in ["triangle", "circle", "rectangle"]:
            self.app.shape_factory.start_primitive_creation(click_point)
        elif self.app.mode == "polygon":
            polygon_completed = self.app.shape_factory.handle_polygon_creation(self.window, click_point)
            if polygon_completed:
                # Create the persistent polygon
                final_vertices = self.app.shape_factory.get_final_polygon_vertices()
                self.app.add_shape(final_vertices)
                self.app.temp_shape = None  # Clear preview after polygon completion
        else:
            logging.error(f"Invalid mode: {self.app.mode}")

    def _handle_left_release(self) -> None:
        """Handle left mouse release"""
        if self.app.mode == "select":
            self.dragging = False
        elif self.app.mode in ["triangle", "circle", "rectangle"]:
            # Create the persistent shape with start point + current mouse position
            current_vertices = self.app.shape_factory.get_current_vertices()
            if len(current_vertices) >= 2:  # Have at least start point
                # Get current mouse position for the end point
                wx, wy = self.app.camera.screen_to_world(*glfw.get_cursor_pos(self.window))
                final_vertices = [current_vertices[0], current_vertices[1], wx, wy]
                self.app.add_shape(final_vertices)
            self.app.shape_factory.finish_primitive_creation()
            self.app.temp_shape = None  # Clear preview after shape creation
        # Polygon mode handled separately

    def _handle_right_click(self, action: int) -> None:
        """Handle right mouse button for panning"""
        if action == glfw.PRESS:
            wx, wy = self.app.camera.screen_to_world(*glfw.get_cursor_pos(self.window))
            self.panning = True
            logging.info("Started panning at (%.2f, %.2f)", wx, wy)
        elif action == glfw.RELEASE:
            wx, wy = self.app.camera.screen_to_world(*glfw.get_cursor_pos(self.window))
            self.panning = False
            logging.info("Stopped panning at (%.2f, %.2f)", wx, wy)

    def cursor_pos_callback(self, window: Any, xpos: float, ypos: float) -> None:
        """Handle cursor movement"""
        from imgui_bundle import imgui

        # Check if ImGui wants to capture the mouse input first
        if imgui.get_io().want_capture_mouse:
            return

        wx, wy = self.app.camera.screen_to_world(xpos, ypos)
        current_point = Vec2(wx, wy)

        if self.dragging and self.app.get_selected_shapes():
            delta = current_point - self.editing_origin
            for shape in self.app.get_selected_shapes():
                shape.move(delta)
            logging.info("Moved shapes")
            self.editing_origin = current_point

        elif self.app.shape_factory.editing_shape:
            # Update temp_shape preview directly instead of modifying vertices array
            self._update_shape_preview(wx, wy)

        elif self.panning:
            delta_x = self.editing_origin.x - wx
            delta_y = self.editing_origin.y - wy
            self.app.camera.pan(delta_x, delta_y)

    def scroll_callback(self, window: Any, xoffset: float, yoffset: float) -> None:
        """Handle mouse scroll for zooming"""
        from imgui_bundle import imgui

        # Check if ImGui wants to capture the mouse input first
        if imgui.get_io().want_capture_mouse:
            return

        xpos, ypos = glfw.get_cursor_pos(window)
        self.app.camera.zoom_at_point(xpos, ypos, yoffset)

    def key_callback(self, window: Any, key: int, scancode: int, action: int, mods: int) -> None:
        """Handle keyboard input"""
        from imgui_bundle import imgui

        if imgui.get_io().want_capture_keyboard:
            return

        if action == glfw.PRESS:
            match key:
                case glfw.KEY_S:
                    self.app.set_mode("select")

                case glfw.KEY_T:
                    self.app.set_mode("triangle")

                case glfw.KEY_C:
                    self.app.set_mode("circle")

                case glfw.KEY_R:
                    self.app.set_mode("rectangle")

                case glfw.KEY_P:
                    self.app.set_mode("polygon")

                case glfw.KEY_SPACE:
                    self.app.camera.reset()
                    logging.info("Reset camera and zoom")

                case glfw.KEY_D:
                    if self.app.get_selected_shapes():
                        for shape in self.app.get_selected_shapes():
                            self.app.objects.remove(shape)
                        self.app.selection_system.clear_selection()
                        logging.info("Deleted selected shapes")

                case glfw.KEY_ESCAPE | glfw.KEY_Q:
                    glfw.set_window_should_close(window, True)

                case _:
                    logging.debug("Untreated key input")

    def _update_shape_preview(self, wx: float, wy: float) -> None:
        """Update the temporary shape preview without modifying the vertices array"""
        if self.app.mode in ["triangle", "circle", "rectangle"]:
            # For primitive shapes, create preview with start point + current mouse position
            current_vertices = self.app.shape_factory.get_current_vertices()
            if len(current_vertices) >= 2:  # Have at least start point
                # Create preview with start point and current mouse position
                preview_vertices = [current_vertices[0], current_vertices[1], wx, wy]
                self.app.temp_shape = self.app.shape_factory.create_shape(self.app.mode, preview_vertices)

        elif self.app.mode == "polygon":
            # For polygons, create preview with existing vertices + current mouse position as preview point
            current_vertices = self.app.shape_factory.get_current_vertices()
            if len(current_vertices) >= 2:  # Have at least one vertex
                # Add current mouse position as temporary preview point
                preview_vertices = current_vertices.copy()
                preview_vertices.extend([wx, wy])
                self.app.temp_shape = self.app.shape_factory.create_shape(self.app.mode, preview_vertices)