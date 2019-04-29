import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy
import pyrr # matrix, vector math

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

	#adding colors
	#    x,    y,  z,   r,   g,   b
	cube = [
		-.5, -.5, 0.5, 1.0, 0.0, 0.0,
		0.5, -.5, 0.5, 0.0, 1.0, 0.0,
		0.5, 0.5, 0.5, 0.0, 0.0, 1.0,
		-.5, 0.5, 0.5, 1.0, 1.0, 1.0,
		-.5, -.5, -.5, 1.0, 0.0, 0.0,
		0.5, -.5, -.5, 0.0, 1.0, 0.0,
		0.5, 0.5, -.5, 0.0, 0.0, 1.0,
		-.5, 0.5, -.5, 1.0, 1.0, 1.0
	]
	cube = numpy.array(cube, dtype=numpy.float32)

	indices = [
		0, 1, 2, 2, 3, 0,
		4, 5, 6, 6, 7, 4,
		4, 5, 1, 1, 0, 4,
		6, 7, 3, 3, 2, 6,
		5, 6, 2, 2, 1, 5,
		7, 4, 0, 0, 3, 7
	]

	indices = numpy.array(indices, dtype=numpy.uint32)

	vertex_shader = """
	#version 410 core
	in vec3 position; // py => shader
	in vec3 color; // py => shader
	out vec3 newColor; // => GPU => window
	uniform mat4 transform;

	void main()
	{
		gl_Position = transform * vec4(position, 1.0f);
		newColor = color;
	}
	"""

	fragment_shader = """
	#version 410 core
	in vec3 newColor;
	out vec4 outColor;

	void main()
	{
		outColor = vec4(newColor, 1.0f);
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
	#                 buf type   byte  point     type
	glBufferData(GL_ARRAY_BUFFER, 192, cube, GL_STATIC_DRAW)

	EBO = glGenBuffers(1)
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, 144, indices, GL_STATIC_DRAW)

	#get position from vertex_shader variable
	position = glGetAttribLocation(shader, "position")
	glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
	glEnableVertexAttribArray(position)

	#get color from vertex_shader program variable
	color = glGetAttribLocation(shader, "color")
	glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
	glEnableVertexAttribArray(color)

	glUseProgram(shader)

	glClearColor(.2, .3, .2, 1.0)
	glEnable(GL_DEPTH_TEST)
	# glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
	while not glfw.window_should_close(window):
		glfw.poll_events()
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		rot_x = pyrr.Matrix44.from_x_rotation(.5 * glfw.get_time())
		rot_y = pyrr.Matrix44.from_y_rotation(.8 * glfw.get_time())

		transform_location = glGetUniformLocation(shader, "transform")
		glUniformMatrix4fv(transform_location, 1, GL_FALSE, rot_x * rot_y)
		glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, None)
		glfw.swap_buffers(window)
	
	glfw.terminate()

if __name__ == "__main__":
	main()