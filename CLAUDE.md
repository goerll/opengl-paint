# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

OpenGL Paint is a simple 2D drawing application built with Python, OpenGL, and GLFW. It allows users to draw various shapes (triangles, circles, rectangles, polygons) with an interactive GUI featuring both keyboard shortcuts and an ImGui sidebar.

## Dependencies and Setup

Install dependencies using pip:
```bash
pip install -r requirements.txt
```

Required dependencies:
- `glfw>=2.6.4` - Window management and input
- `PyOpenGL>=3.1.7` - OpenGL bindings
- `PyOpenGL_accelerate>=3.1.7` - Performance optimizations
- `numpy>=1.24` - Numerical operations
- `imgui-bundle>=1.6.0` - Immediate mode GUI

## Running the Application

```bash
python main.py
```

## Architecture

The application follows a modular architecture with clear separation of concerns:

### Core Components

- **main.py** (`GraphicsApp` class): Main application loop, window management, input handling, and state management
- **renderer.py** (`Renderer` class): OpenGL rendering pipeline, shader management, and draw calls
- **shapes.py**: Shape hierarchy with geometric primitives and hit detection
- **math_utils.py**: Vector math utilities (`Vec2`, `Vec3` classes)
- **shader.py**: Shader program compilation and management

### Key Architecture Patterns

1. **Shape System**: All shapes inherit from `Shape` base class with `get_vertices()`, `contains_point()`, and `move()` methods
2. **Coordinate System**: Screen coordinates → NDC → World coordinates with camera/zoom transforms
3. **Input Handling**: GLFW callbacks with ImGui input priority handling
4. **Rendering Pipeline**: VAO/VBO dynamic vertex uploads with MVP matrix uniforms

### Application State Management

The `GraphicsApp` class maintains:
- Drawing modes (select, triangle, circle, rectangle, polygon)
- Shape collections (`self.objects`, `self.selected_shapes`)
- Camera state (position, zoom level)
- Temporary editing state (`self.vertices`, `self.editing_origin`)

## Controls

### Keyboard Shortcuts
- `S` - Select mode
- `T` - Triangle mode
- `C` - Circle mode
- `R` - Rectangle mode
- `P` - Polygon mode
- `Space` - Reset camera and zoom
- `D` - Delete selected shapes
- `ESC/Q` - Exit

### Mouse Controls
- Left click/drag - Create shapes or select and move them
- Right click/drag - Pan the view
- Mouse wheel - Zoom in/out
- Shift + click (polygon mode) - Complete polygon creation

## Shader System

The application uses custom OpenGL shaders located in:
- `shaders/vertex.glsl` - Vertex transformation with MVP matrices
- `shaders/fragment.glsl` - Color output

The renderer expects vertex positions in 2D space and uses uniform variables for:
- `projection`, `view`, `model` matrices
- `color` Vec3 uniform for shape coloring

## Development Notes

### Type Checking
The project uses strict type checking via `pyproject.toml` with some intentionally relaxed rules for OpenGL interop.

### Logging
Configured at INFO level. Debug coordinates and interactions are logged at DEBUG level.

### Coordinate Transformations
Key methods in `GraphicsApp`:
- `screen_to_normalized()` - Convert pixels to NDC
- `screen_to_world()` - Convert pixels to world coordinates with camera/zoom
- `create_projection_matrix()` - Orthographic projection with zoom
- `create_view_matrix()` - Camera translation

### Shape Hit Detection
Each shape implements `contains_point(Vec2)` using appropriate algorithms:
- Rectangle: Axis-aligned bounding box check
- Circle: Distance from center
- Triangle: Barycentric coordinates
- Polygon: Ray casting algorithm