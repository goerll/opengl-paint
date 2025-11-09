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
   - [x] (Optional) other shapes such as stars, elipses and regular polygons (elipses are drawn in circle mode without <kbd>SHIFT</shift>)

- Select graphical objects
   - [x] Implement point-based object selection algorithm
   - [x] Multiple object selection (<SHIFT> while selecting)
   - [ ] (Optional) Draw bounding boxes and selection handlers for selected objects

- Interactively manipulate graphical objects
   - [x] Remove objects (<kbd>d</kbd> while selecting)
   - [ ] Change size
   - [x] Rotation (sidebar)
   - [x] Translation (dragging in select mode)
   - [x] (Optional) Uniform scaling (without deforming the object) and non-uniform scaling (<kbd>SHIFT</kbd> while creating object)
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

## Features

- **Shape Creation**: Triangle, Circle, Rectangle, Polygon drawing tools
- **Shape Selection**: Click to select, drag to move, Shift+click for multi-selection
- **Camera Controls**: Pan, zoom, and reset view functionality
- **Real-time Rendering**: OpenGL-based rendering with custom shaders
- **Interactive UI**: ImGui sidebar with tool selection and status information

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




