import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy

def main():
	if not glfw.init():
		return
	glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
	glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
	glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, 1)
	glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
	window = glfw.create_window(800, 600, "MY OPENGL", None, None)

	if not window:
		glfw.terminate()
		return

	glfw.make_context_current(window)

	triangle = [
		-.5, -.5, 0.0,
		.5, -.5, 0.0,
		0.0, 0.5, 0.0
	]
	triangle = numpy.array(triangle, dtype=numpy.float32)

	vertex_shader = """
	#version 410 core
	in vec4 position;

	void main()
	{
		gl_Position = position;
	}
	"""

	fragment_shader = """
	#version 410 core
	out vec4 frag_color;
	void main()
	{
		frag_color = vec4(1.0f, 0.0f, 0.0f, 1.0f);
	}
	"""
	VAO = glGenVertexArrays(1)
	glBindVertexArray(VAO)

	shader = OpenGL.GL.shaders.compileProgram(
		OpenGL.GL.shaders.compileShader(
			vertex_shader, GL_VERTEX_SHADER
		),
		OpenGL.GL.shaders.compileShader(
			fragment_shader, GL_FRAGMENT_SHADER
		)
	)

	VBO = glGenBuffers(1) # vertex buffer object for GPU
	glBindBuffer(GL_ARRAY_BUFFER, VBO)
	#upload data to array buffer
	glBufferData(GL_ARRAY_BUFFER, 36, triangle, GL_STATIC_DRAW)

	#get position from vertex_shader variable
	position = glGetAttribLocation(shader, "position")
	glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 0, None)
	glEnableVertexAttribArray(position)

	glUseProgram(shader)

	glClearColor(.2, .3, .2, 1.0)
	while not glfw.window_should_close(window):
		glfw.poll_events()
		glClear(GL_COLOR_BUFFER_BIT)
		glDrawArrays(GL_TRIANGLES, 0, 3)
		glfw.swap_buffers(window)
	
	glfw.terminate()

if __name__ == "__main__":
	main()