# OpenGL Paint

A 2D drawing application built with Python, OpenGL, and GLFW that allows users to create and manipulate various geometric shapes through both keyboard shortcuts and an ImGui interface.

# Controls

| Key | Alt | Function |
| - | - | - |
| <kbd>S</kbd> | - | Switch to select mode |
| <kbd>T</kbd> | - | Switch to triangle drawing mode |
| <kbd>C</kbd> | - | Switch to circle drawing mode |
| <kbd>R</kbd> | - | Switch to rectangle drawing mode |
| <kbd>P</kbd> | - | Switch to polygon drawing mode |
| <kbd>D</kbd> | - | Delete selected shapes |
| <kbd>SPACE</kbd> | - | Reset camera and zoom |
| <kbd>ESC</kbd> / <kbd>Q</kbd> | - | Exit application |
| - | <kbd>🖱️ LMB</kbd> | Click to select shapes (in select mode), click and drag to draw shapes (in drawing modes), drag to move selected shapes (in select mode) |
| - | <kbd>🖱️ RMB</kbd> | Hold and drag to pan the camera |
| - | <kbd>🖱️ Wheel</kbd> | Zoom in/out at mouse cursor position |
| <kbd>SHIFT</kbd> | <kbd>🖱️ LMB</kbd> | Multi-select shapes (in select mode) |
| <kbd>SHIFT</kbd> | <kbd>🖱️ Drag</kbd> | Constrain shapes while drawing (square for rectangle, perfect circle for circle, equilateral for triangle) |


# Assignment Items Completed
- Draw graphical objects
   - [x] Non-convex polygons
   - [x] Circles
   - [x] Rectangles
   - [x] (Optional) other shapes such as stars, elipses and regular polygons (elipses are drawn in circle mode without <kbd>SHIFT</kbd>)

- Select graphical objects
   - [x] Implement point-based object selection algorithm (used for polygons, in /shapes/primitives.py)
   - [x] Multiple object selection (<kbd>SHIFT</kbd> while selecting)
   - [ ] (Optional) Draw bounding boxes and selection handlers for selected objects

- Interactively manipulate graphical objects
   - [x] Remove objects (<kbd>d</kbd> while selecting)
   - [ ] Change size
   - [x] Rotation (sidebar)
   - [x] Translation (clicking and dragging in select mode)
   - [x] (Optional) Uniform scaling (without deforming the object) and non-uniform scaling (<kbd>SHIFT</kbd> while creating object for uniform scaling)
   - [ ] (Optional) Selection of rotation point (center, bounding box corner, arbitrary point)

- Modify properties and perform queries
   - [x] Query: area, perimeter (sidebar)
   - [x] Attributes: color (sidebar)
   - [ ] (Optional) Solid color fill
   - [ ] (Optional) Change outline line type

- Use visualization resources
   - [x] Zoom in/out
   - [x] Pan
   - [ ] (Optional) Zoom window

## Structure

The project follows a modular architecture with clear separation of concerns:

```
opengl-paint/
├── main.py                 # Application entry point
├── shader.py               # Shader program management
├── shaders/                # GLSL shader files
│   ├── vertex.glsl         # Vertex shader
│   └── fragment.glsl       # Fragment shader
├── core/                   # Core application components
│   ├── app.py              # Main GraphicsApp class (application loop, state management)
│   ├── camera.py           # Camera system (viewport, zoom, pan, coordinate transformations)
│   ├── input_manager.py    # Input handling (keyboard, mouse, callbacks)
│   └── input_filter.py     # Input filtering for ImGui integration
├── shapes/                 # Shape definitions
│   ├── base.py             # Abstract Shape base class (transformations, rendering interface)
│   └── primitives.py       # Concrete shape implementations (Triangle, Circle, Rectangle, Polygon)
├── systems/                # Feature systems
│   ├── selection_system.py # Shape selection and multi-selection logic
│   └── shape_factory.py    # Shape creation and editing (primitive creation, polygon building)
├── geometry/               # Geometric utilities
│   ├── vectors.py          # Vector math (Vec2, Vec3)
│   ├── transforms.py       # Transformation utilities (rotation, scaling, center calculation)
│   └── vertex_generator.py # Vertex generation for shapes (circles, polygons)
├── graphics/               # Rendering system
│   └── renderer.py         # OpenGL rendering (VAO/VBO management, draw calls)
├── ui/                     # User interface
│   ├── imgui_ui.py         # ImGui sidebar UI (tool selection, properties panel)
│   └── imgui_helpers.py    # ImGui helper utilities
└── config/                 # Configuration
    └── constants.py        # Application constants (UI config, drawing config, camera config)
```

### Key Components

- **`core/app.py`**: Main application class that orchestrates all systems, manages the render loop, and handles application state (drawing modes, object list, temporary shapes).

- **`core/camera.py`**: Handles viewport transformations, zoom, pan, and coordinate system conversions between screen space and world space.

- **`core/input_manager.py`**: Centralized input handling for keyboard shortcuts, mouse interactions (click, drag, scroll), and delegates to appropriate systems based on current mode.

- **`shapes/base.py`**: Abstract base class defining the interface for all shapes, including transformation operations (rotation, translation) and rendering preparation.

- **`shapes/primitives.py`**: Concrete implementations of geometric shapes with shape-specific logic (e.g., circle generation, polygon validation).

- **`systems/selection_system.py`**: Manages shape selection using point-in-shape algorithms, supports single and multi-selection with Shift modifier.

- **`systems/shape_factory.py`**: Handles interactive shape creation, including drag-to-draw for primitives and click-to-add-vertices for polygons.

- **`graphics/renderer.py`**: OpenGL rendering abstraction, manages vertex buffers, shader programs, and draw calls for all shapes.

- **`ui/imgui_ui.py`**: ImGui-based sidebar interface providing tool selection, shape properties editing (color, rotation), and status information.

## Dependencies

```bash
pip install -r requirements.txt
```

## Installation and Usage

1. **Clone and setup:**
   ```bash
   git clone <repository-url>
   cd opengl-paint
   pip install -r requirements.txt
   ```

2. **Run application:**
   ```bash
   python main.py
   ```




