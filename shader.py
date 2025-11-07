from OpenGL.GL import (
    GL_VERTEX_SHADER,
    GL_FRAGMENT_SHADER,
    GL_LINK_STATUS,
    GL_COMPILE_STATUS,
    glGetShaderInfoLog,
    glGetProgramiv,
    glCreateProgram,
    glCreateShader,
    glAttachShader,
    glLinkProgram,
    glGetProgramInfoLog,
    glDeleteShader,
    glShaderSource,
    glCompileShader,
    glGetShaderiv,
)
import logging


class ShaderProgram:
    def __init__(self) -> None:
        self.program: int | None = None

    def load(self, vertex_path: str, fragment_path: str) -> bool:
        """Load and compile vertex and fragment shaders"""
        vertex_source = self.read_file(vertex_path)
        fragment_source = self.read_file(fragment_path)

        if not vertex_source or not fragment_source:
            return False

        vertex_shader = self.compile_shader(vertex_source, GL_VERTEX_SHADER)
        fragment_shader = self.compile_shader(fragment_source, GL_FRAGMENT_SHADER)

        if not vertex_shader or not fragment_shader:
            return False

        self.program = glCreateProgram()
        glAttachShader(self.program, vertex_shader)
        glAttachShader(self.program, fragment_shader)
        glLinkProgram(self.program)

        # Check linking
        if not glGetProgramiv(self.program, GL_LINK_STATUS):
            logging.error(f"Shader linking failed: {glGetProgramInfoLog(self.program)}")
            return False

        # Clean up shaders
        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)

        return True

    def read_file(self, path: str) -> str | None:
        """Read shader source code from file"""
        try:
            with open(path, "r") as file:
                return file.read()
        except FileNotFoundError:
            logging.error(f"Shader file not found: {path}")
            return None

    def compile_shader(self, source: str, shader_type: int) -> int | None:
        """Compile OpenGL shader from source code"""
        shader = glCreateShader(shader_type)
        glShaderSource(shader, source)
        glCompileShader(shader)

        if not glGetShaderiv(shader, GL_COMPILE_STATUS):
            logging.error(f"Shader compilation failed: {glGetShaderInfoLog(shader)}")
            return None

        return shader
