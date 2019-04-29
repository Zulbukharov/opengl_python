import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy
from PIL import Image

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
	#    x,    y,  z,   r,   g,   b,  tx,  ty
	quad = [
		-.5, -.5, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0,
		0.5, -.5, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0,
		0.5, 0.5, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0,
		-.5, 0.5, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0,
	]
	quad = numpy.array(quad, dtype=numpy.float32)

	indices = [
		0, 1, 2,
		2, 3, 0
	]

	indices = numpy.array(indices, dtype=numpy.uint32)

	vertex_shader = """
	#version 410 core
	in vec3 position;
	in vec3 color;
	in vec2 inTexCords;

	out vec2 outTexCords;
	out vec3 newColor;

	void main()
	{
		gl_Position = vec4(position, 1.0f);
		newColor = color;
		outTexCords = inTexCords;
	}
	"""

	fragment_shader = """
	#version 410 core
	in vec3 newColor;
	in vec2 outTexCords;

	uniform sampler2D sampleTex;
	out vec4 outColor;

	void main()
	{
		outColor = texture(sampleTex, outTexCords);
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
	glBufferData(GL_ARRAY_BUFFER, quad.itemsize * len(quad), quad, GL_STATIC_DRAW)

	EBO = glGenBuffers(1)
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.itemsize * len(indices), indices, GL_STATIC_DRAW)

	#get position from vertex_shader variable
	position = glGetAttribLocation(shader, "position")
	glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
	glEnableVertexAttribArray(position)

	#get color from vertex_shader program variable
	# color = glGetAttribLocation(shader, "color")
	# glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
	# glEnableVertexAttribArray(color)

	texture_cords = glGetAttribLocation(shader, "inTexCords")
	glVertexAttribPointer(texture_cords, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(24))
	glEnableVertexAttribArray(texture_cords)

	#load texture
	texture = glGenTextures(1)
	glBindTexture(GL_TEXTURE_2D, texture)
	# texture wrapping parametr
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

	#texture filtering parametr
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

	image = Image.open("./1.jpg")
	flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)
	image_data = numpy.array(list(flipped_image.getdata()), numpy.uint8)
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 564, 555, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)
	# glTexImage2D()

	glUseProgram(shader)

	glClearColor(.2, .3, .2, 1.0)
	while not glfw.window_should_close(window):
		glfw.poll_events()
		glClear(GL_COLOR_BUFFER_BIT)
		glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
		glfw.swap_buffers(window)
	
	glfw.terminate()

if __name__ == "__main__":
	main()