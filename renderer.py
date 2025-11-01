from OpenGL.GL import (
    GL_TRIANGLES,
    GL_LINE_LOOP,
    GL_ARRAY_BUFFER,
    GL_DYNAMIC_DRAW,
    GL_FLOAT,
    GL_FALSE,
    glUniform3f,
    glGetUniformLocation,
    glGenVertexArrays,
    glGenBuffers,
    glBindVertexArray,
    glBindBuffer,
    glBufferData,
    glVertexAttribPointer,
    glEnableVertexAttribArray,
    glUseProgram,
    glDrawArrays,
    glUniformMatrix4fv,
)

import glm
import numpy as np
from shader import ShaderProgram
from shapes import Shape


class Renderer:
    def __init__(self):
        self.shader_program = None
        self.vao = None
        self.vbo = None

    def init(self):
        # Initialize shader program
        self.shader_program = ShaderProgram()
        if not self.shader_program.load("shaders/vertex.glsl", "shaders/fragment.glsl"):
            return False

        # Create VAO and VBO
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)

        return True

    def set_matrices(self, projection, view, model):
        """Set MVP matrices for the shader"""
        glUseProgram(self.shader_program.program)

        # Get uniform locations
        proj_location = glGetUniformLocation(self.shader_program.program, "projection")
        view_location = glGetUniformLocation(self.shader_program.program, "view")
        model_location = glGetUniformLocation(self.shader_program.program, "model")

        # Set matrix uniforms
        glUniformMatrix4fv(proj_location, 1, GL_FALSE, glm.value_ptr(projection))
        glUniformMatrix4fv(view_location, 1, GL_FALSE, glm.value_ptr(view))
        glUniformMatrix4fv(model_location, 1, GL_FALSE, glm.value_ptr(model))

    def render_shape(self, shape: Shape):
        vertices = shape.get_vertices()

        glUseProgram(self.shader_program.program)
        glBindVertexArray(self.vao)

        # Upload vertex data
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        vertices_array = np.array(vertices, dtype=np.float32)
        glBufferData(
            GL_ARRAY_BUFFER, vertices_array.nbytes, vertices_array, GL_DYNAMIC_DRAW
        )

        # Configure vertex attributes
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)

        # Set color uniform
        color_location = glGetUniformLocation(self.shader_program.program, "color")
        color = shape.get_color()
        glUniform3f(color_location, color.r, color.g, color.b)

        # Draw
        if shape.get_draw_mode() == GL_TRIANGLES:
            glDrawArrays(GL_TRIANGLES, 0, len(vertices) // 2)
        elif shape.get_draw_mode() == GL_LINE_LOOP:
            glDrawArrays(GL_LINE_LOOP, 0, len(vertices) // 2)

        glBindVertexArray(0)
