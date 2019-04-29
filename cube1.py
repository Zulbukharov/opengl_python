import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy
import pyrr # matrix, vector math
from PIL import Image
from math import *
# fov   =  45.0

# deltaTime = 0.0
# lastFrame = 0.0
view = pyrr.matrix44.create_from_translation(pyrr.Vector3([.0, .4, -3.0]))
firstMouse = True
yaw   = -90.0
pitch =  0.0
lastX =  800.0 / 2.0
lastY =  600.0 / 2.0

def key_event(window,key,scancode,action,mods):
	if action == glfw.REPEAT or action == glfw.PRESS:
		if key == glfw.KEY_W:
			model[3][2] += .1
		elif key == glfw.KEY_S:
			model[3][2] -= .1
		elif key == glfw.KEY_A:
			model[3][0] += .1
		elif key == glfw.KEY_D:
			model[3][0] -= .1

def mouse_callback(window, xPos, yPos):
	global firstMouse
	global yaw
	global pitch
	global lastX
	global lastY
	global view
	if firstMouse:
		lastX = xPos
		lastY = yPos
		firstMouse = False
	xoffset = xPos - lastX
	yoffset = lastY - yPos
	lastX = xPos
	lastY = yPos
	sensitivity = 0.1
	xoffset *= sensitivity
	yoffset *= sensitivity

	yaw += xoffset
	pitch += yoffset

	if pitch > 89.0:
		pitch = 89.0
	if pitch < -89.0:
		pitch = -89.0

	# glm::vec3 front;
	# cos()
	front = [0, 0, 0]
	front[0] = cos(radians(yaw)) * cos(radians(pitch))
	front[1] = sin(radians(pitch))
	front[2] = sin(radians(yaw)) * cos(radians(pitch))

	view[3][0] = front[0]
	view[3][1] = front[1]
	view[3][2] = front[2]
	# norm1 = front / numpy.linalg.norm(front)
	print(front)

def main():
	if not glfw.init():
		return
	w_width = 800
	w_height = 600
	glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
	glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
	glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, 1)
	glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

	glfw.window_hint(glfw.RESIZABLE, GL_TRUE)
	window = glfw.create_window(w_width, w_height, "MY OPENGL", None, None)

	

	if not window:
		glfw.terminate()
		return

	glfw.make_context_current(window)
	# Enable key events
	glfw.set_input_mode(window,glfw.STICKY_KEYS,GL_TRUE) 
	# Enable key event callback
	glfw.set_key_callback(window, key_event)
	# Enable cursor event callback
	glfw.set_cursor_pos_callback(window, mouse_callback)

	#when window resize
	# glfw.set_window_size_callback(window, window_resize)

	#adding colors
	#     x,    y,     z,   r,    g,   b    tx   ty
	cube = [
		-0.5, -0.5,  0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
		 0.5, -0.5,  0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
		 0.5,  0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
		-0.5,  0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

		-0.5, -0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
		 0.5, -0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
		 0.5,  0.5, -0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
		-0.5,  0.5, -0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

		 0.5, -0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
		 0.5,  0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
		 0.5,  0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
		 0.5, -0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

		-0.5,  0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
		-0.5, -0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
		-0.5, -0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
		-0.5,  0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

		-0.5, -0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
		 0.5, -0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
		 0.5, -0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
		-0.5, -0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

		 0.5,  0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
		-0.5,  0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
		-0.5,  0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
		 0.5,  0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0
	]
	cube = numpy.array(cube, dtype=numpy.float32)

	indices = [
				0,  1,  2,  2,  3,  0,
				4,  5,  6,  6,  7,  4,
				8,  9, 10, 10, 11,  8,
				12, 13, 14, 14, 15, 12,
				16, 17, 18, 18, 19, 16,
				20, 21, 22, 22, 23, 20
			]

	indices = numpy.array(indices, dtype=numpy.uint32)

	vertex_shader = """
	#version 410 core
	in vec3 position; // py => shader
	in vec3 color; // py => shader
	in vec2 inTexCords;

	out vec3 newColor; // => GPU => window
	out vec2 newTexCords;
	uniform mat4 transform;

	uniform mat4 view;
	uniform mat4 projection;
	uniform mat4 model;

	void main()
	{
		gl_Position = projection * view * model * transform * vec4(position, 1.0f);
		newColor = color;
		newTexCords = inTexCords;
	}
	"""

	fragment_shader = """
	#version 410 core
	in vec3 newColor;
	in vec2 newTexCords;

	out vec4 outColor;
	uniform sampler2D sampleTex;

	void main()
	{
		outColor = texture(sampleTex, newTexCords) * vec4(newColor, 1.0f);
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
	glBufferData(GL_ARRAY_BUFFER, cube.itemsize * len(cube), cube, GL_STATIC_DRAW)

	EBO = glGenBuffers(1)
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.itemsize * len(indices), indices, GL_STATIC_DRAW)

	#get position from vertex_shader variable
	position = glGetAttribLocation(shader, "position")
	glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
	glEnableVertexAttribArray(position)

	#get color from vertex_shader program variable
	color = glGetAttribLocation(shader, "color")
	glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
	glEnableVertexAttribArray(color)

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

	image = Image.open("./res/1.jpg")
	flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)
	image_data = numpy.array(list(flipped_image.getdata()), numpy.uint8)
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 564, 555, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)
	# glTexImage2D()

	glUseProgram(shader)

	glClearColor(.2, .3, .2, 1.0)
	glEnable(GL_DEPTH_TEST)
	# glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)


	#perspective part
	# view matrix
	# global view
	# projection matrix
	projection = pyrr.matrix44.create_perspective_projection(45.0, w_width / w_height, 0.1, 100.0)
	# model position matrix
	global model
	model = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0, 0.0, 0.0]))
	print("model", model[3][2])


	view_location = glGetUniformLocation(shader, "view")
	projection_location = glGetUniformLocation(shader, "projection")
	model_location = glGetUniformLocation(shader, "model")

	glUniformMatrix4fv(view_location, 1, GL_FALSE, view)
	glUniformMatrix4fv(model_location, 1, GL_FALSE, model)
	glUniformMatrix4fv(projection_location, 1, GL_FALSE, projection)

	while not glfw.window_should_close(window):
		glfw.poll_events()
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		# rot_x = pyrr.Matrix44.from_x_rotation(.5 * glfw.get_time())
		rot_y = pyrr.Matrix44.from_y_rotation(.0)

		# currentFrame = glfw.getTime()
		# deltaTime = currentFrame - lastFrame
		# lastFrame = currentFrame
		transform_location = glGetUniformLocation(shader, "transform")
		# glUniformMatrix4fv(transform_location, 1, GL_FALSE, rot_x * rot_y)
		glUniformMatrix4fv(transform_location, 1, GL_FALSE, rot_y)
		glUniformMatrix4fv(view_location, 1, GL_FALSE, view)
		glUniformMatrix4fv(model_location, 1, GL_FALSE, model)
		glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
		glfw.swap_buffers(window)
	
	glfw.terminate()

if __name__ == "__main__":
	main()