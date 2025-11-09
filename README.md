# OpenGL Paint

A 2D drawing application built with Python, OpenGL, and GLFW that allows users to create and manipulate various geometric shapes through both keyboard shortcuts and an ImGui interface.

# Assignment Items Completed
- Draw graphical objects
   - [x] Non-convex polygons
   - [x] Circles
   - [x] Rectangles
   - [x] (Optional) other shapes such as stars, elipses and regular polygons

- Select graphical objects
   - [x] Implement point-based object selection algorithm
   - [x] Multiple object selection
   - [ ] (Optional) Draw bounding boxes and selection handlers for selected objects

- Interactively manipulate graphical objects
   - [] Remove objects (use key d)
   - [ ] Change size
   - [x] Rotation
   - [x] Translation
   - [x] (Optional) Uniform scaling (without deforming the object) and non-uniform scaling (shifting while creating object)
   - [ ] (Optional) Selection of rotation point (center, bounding box corner, arbitrary point)

- Modify properties and perform queries
   - [x] Query: area, perimeter (sidebar)
   - [x] Attributes: color (pre-configured palette, keyboard input, or color picker component)
   - [ ] (Optional) Solid color fill
   - [ ] (Optional) Change outline line type

- Use visualization resources
   - [x] Zoom in/out
   - [x] Pan
   - [ ] (Optional) Zoom window

## Features

- **Shape Creation**: Triangle, Circle, Rectangle, Polygon drawing tools
- **Shape Selection**: Click to select, drag to move, Shift+click for multi-selection
- **Camera Controls**: Pan, zoom, and reset view functionality
- **Real-time Rendering**: OpenGL-based rendering with custom shaders
- **Interactive UI**: ImGui sidebar with tool selection and status information

## Project Structure

```
opengl-paint/
├── main.py                 # Application entry point
├── shader.py               # OpenGL shader program management
├── core/                   # Core application systems
│   ├── app.py             # Main application class and game loop
│   ├── camera.py          # Camera and viewport management
│   └── input_manager.py   # Input handling and callbacks
├── geometry/              # Mathematical utilities
│   └── vectors.py         # Vec2 and Vec3 classes for vector math
├── graphics/              # Rendering system
│   └── renderer.py        # OpenGL rendering pipeline
├── shapes/                # Shape hierarchy and implementations
│   ├── base.py           # Abstract Shape base class
│   └── primitives.py     # Concrete shape implementations
├── systems/               # Game logic systems
│   ├── selection_system.py  # Shape selection logic
│   └── shape_factory.py     # Shape creation and editing
├── ui/                    # User interface
│   └── imgui_ui.py       # ImGui sidebar interface
└── shaders/              # OpenGL shader files
    ├── vertex.glsl       # Vertex shader
    └── fragment.glsl     # Fragment shader
```

## Architecture Overview

### Core Systems

**GraphicsApp (`core/app.py`)**
- Main application loop and state management
- Window initialization and OpenGL context setup
- Coordinate system transformations
- Temporary shape rendering during creation

**Camera (`core/camera.py`)**
- Orthographic projection with zoom and pan
- Screen-to-world coordinate conversion
- Viewport management for window resizing

**InputManager (`core/input_manager.py`)**
- GLFW callback handling for mouse and keyboard
- ImGui input priority management
- Mode-specific input processing

### Shape System

**Shape Base Class (`shapes/base.py`)**
- Abstract interface for all shapes
- Common functionality: movement, color, rendering mode
- Hit detection abstraction

**Shape Implementations (`shapes/primitives.py`)**
- **Rectangle**: 4-corner rectangle from diagonal points
- **Triangle**: Equilateral triangle from base points
- **Circle**: Circle defined by center and radius
- **Polygon**: Multi-vertex polygon with ray-casting hit detection

**ShapeFactory (`systems/shape_factory.py`)**
- Shape creation from vertex data
- Drawing state management for interactive creation
- Vertex manipulation during shape editing

**SelectionSystem (`systems/selection_system.py`)**
- Single and multi-selection logic
- Hit testing with z-ordering (topmost shape priority)
- Encapsulated selection state management

### Rendering Pipeline

**Renderer (`graphics/renderer.py`)**
- OpenGL VAO/VBO management
- Dynamic vertex buffer updates
- Shader program and uniform management
- MVP matrix transformations

**ShaderProgram (`shader.py`)**
- OpenGL shader compilation and linking
- Error handling with logging
- Resource cleanup management

## Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `glfw>=2.6.4` - Window management and input handling
- `PyOpenGL>=3.1.7` - OpenGL bindings
- `PyOpenGL_accelerate>=3.1.7` - Performance optimizations
- `numpy>=1.24` - Numerical operations
- `imgui-bundle>=1.6.0` - Immediate mode GUI
- `glm` - Matrix mathematics

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

## Controls

### Keyboard Shortcuts
- `S` - Selection mode
- `T` - Triangle mode
- `C` - Circle mode
- `R` - Rectangle mode
- `P` - Polygon mode
- `Space` - Reset camera view
- `D` - Delete selected shapes
- `ESC` or `Q` - Exit application

### Mouse Controls
- **Left Click/Drag**:
  - Selection mode: Click to select shapes, drag to move
  - Drawing modes: Click and drag to create shapes
  - Polygon mode: Click to add vertices, Shift+click to complete
- **Right Click/Drag** - Pan the camera view
- **Mouse Wheel** - Zoom in/out at cursor position

## Coordinate System

The application uses a multi-layer coordinate system:
1. **Screen Coordinates**: Pixel positions (0,0 to width,height)
2. **Normalized Device Coordinates**: (-1,-1) to (1,1) OpenGL space
3. **World Coordinates**: Camera-transformed space with pan/zoom

Transformations are handled automatically by the Camera class for consistent shape placement regardless of view state.

## Shader System

Custom OpenGL shaders handle rendering:
- **Vertex Shader** (`shaders/vertex.glsl`): MVP matrix transformations
- **Fragment Shader** (`shaders/fragment.glsl`): Color output

Vertex positions are provided as 2D coordinates, with shape colors passed as Vec3 uniforms.

## Development Notes

### Type Checking
The project uses strict type checking via `pyproject.toml`. Type hints are comprehensive across all modules.

### Logging
Configured at INFO level. Debug coordinate and interaction data available at DEBUG level.

### Memory Management
- OpenGL resources (VAOs, VBOs, shaders) are properly cleaned up
- Shape vertex data uses copies to prevent reference issues
- Selection state encapsulated to prevent external modification

## License

[Add your license information here]