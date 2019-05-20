import glfw
from OpenGL.GL import *
import numpy
import pyrr # matrix, vector math
from PIL import Image
from math import *
import shaderLoader

cameraPos   =pyrr.Vector3([0.0, 0.0,  3.0])
cameraFront =pyrr.Vector3([0.0, 0.0, -1.0])
cameraUp    =pyrr.Vector3([0.0, 1.0,  0.0])
delta_time 	= 0.0
last_frame 	= 0.0
view = pyrr.Matrix44.look_at(cameraPos, cameraPos + cameraFront, cameraUp)
yaw    = -90.0 #Yaw is initialized to -90.0 degrees since a yaw of 0.0 results in a direction vector pointing to the right (due to how Eular angles work) so we initially rotate a bit to the left.
pitch  =  0.0
lastX  =  800 / 2.0
lastY  =  600 / 2.0
fov =  45.0
firstMouse = True

def mouse_callback(window, xpos, ypos):
	global firstMouse
	global yaw
	global pitch
	global lastX
	global lastY
	global fov
	global cameraFront

	if firstMouse:
		lastX = xpos
		lastY = ypos
		firstMouse = False

	xoffset = xpos - lastX
	yoffset = lastY - ypos # Reversed since y-coordinates go from bottom to left
	lastX = xpos
	lastY = ypos

	sensitivity = 0.50	# Change this value to your liking
	xoffset *= sensitivity
	yoffset *= sensitivity

	yaw   += xoffset
	pitch += yoffset

	# Make sure that when pitch is out of bounds, screen doesn't get flipped
	if pitch > 89.0:
		pitch = 89.0
	if pitch < -89.0:
		pitch = -89.0
	front = pyrr.Vector3([0.0,0.0,0.0])
	front.x = cos(radians(yaw)) * cos(radians(pitch))
	front.y = sin(radians(pitch))
	front.z = sin(radians(yaw)) * cos(radians(pitch))
	cameraFront = pyrr.vector.normalise(front)

def key_event(window,key,scancode,action,mods):
	global cameraFront
	global cameraPos
	global cameraUp
	global view
	global delta_time
	cameraSpeed = 52.0 * delta_time
	if action == glfw.REPEAT or action == glfw.PRESS:
		if key == glfw.KEY_ESCAPE:
			glfw.set_window_should_close(window, GL_TRUE)
		elif key == glfw.KEY_W:
			cameraPos += cameraSpeed * cameraFront
		elif key == glfw.KEY_S:
			cameraPos -= cameraSpeed * cameraFront
		elif key == glfw.KEY_A:
			cameraPos -= pyrr.vector.normalise(pyrr.vector3.cross(cameraFront, cameraUp)) * cameraSpeed
		elif key == glfw.KEY_D:
			cameraPos += pyrr.vector.normalise(pyrr.vector3.cross(cameraFront, cameraUp)) * cameraSpeed

def main():
	global delta_time
	global last_frame
	# global cameraFront
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
	glfw.set_input_mode(window, glfw.STICKY_KEYS,GL_TRUE) 
	# Enable key event callback
	glfw.set_key_callback(window, key_event)

	glfw.set_cursor_pos_callback(window, mouse_callback)

	#when window resize
	# glfw.set_window_size_callback(window, window_resize)

	#adding colors
	#     x,    y,     z,   r,    g,   b    tx   ty
	cube = [
		-0.5, -0.5, -0.5,  0.0, 0.0,
		 0.5, -0.5, -0.5,  1.0, 0.0,
		 0.5,  0.5, -0.5,  1.0, 1.0,
		 0.5,  0.5, -0.5,  1.0, 1.0,
		-0.5,  0.5, -0.5,  0.0, 1.0,
		-0.5, -0.5, -0.5,  0.0, 0.0,

		-0.5, -0.5,  0.5,  0.0, 0.0,
		 0.5, -0.5,  0.5,  1.0, 0.0,
		 0.5,  0.5,  0.5,  1.0, 1.0,
		 0.5,  0.5,  0.5,  1.0, 1.0,
		-0.5,  0.5,  0.5,  0.0, 1.0,
		-0.5, -0.5,  0.5,  0.0, 0.0,

		-0.5,  0.5,  0.5,  1.0, 0.0,
		-0.5,  0.5, -0.5,  1.0, 1.0,
		-0.5, -0.5, -0.5,  0.0, 1.0,
		-0.5, -0.5, -0.5,  0.0, 1.0,
		-0.5, -0.5,  0.5,  0.0, 0.0,
		-0.5,  0.5,  0.5,  1.0, 0.0,

		 0.5,  0.5,  0.5,  1.0, 0.0,
		 0.5,  0.5, -0.5,  1.0, 1.0,
		 0.5, -0.5, -0.5,  0.0, 1.0,
		 0.5, -0.5, -0.5,  0.0, 1.0,
		 0.5, -0.5,  0.5,  0.0, 0.0,
		 0.5,  0.5,  0.5,  1.0, 0.0,

		-0.5, -0.5, -0.5,  0.0, 1.0,
		 0.5, -0.5, -0.5,  1.0, 1.0,
		 0.5, -0.5,  0.5,  1.0, 0.0,
		 0.5, -0.5,  0.5,  1.0, 0.0,
		-0.5, -0.5,  0.5,  0.0, 0.0,
		-0.5, -0.5, -0.5,  0.0, 1.0,

		-0.5,  0.5, -0.5,  0.0, 1.0,
		 0.5,  0.5, -0.5,  1.0, 1.0,
		 0.5,  0.5,  0.5,  1.0, 0.0,
		 0.5,  0.5,  0.5,  1.0, 0.0,
		-0.5,  0.5,  0.5,  0.0, 0.0,
		-0.5,  0.5, -0.5,  0.0, 1.0
	]
	        # Positions          # Texture Coords
	# cube = [   0.5,  0.5, 0.0,   1.0, 1.0, # Top Right
	# 	 0.5, -0.5, 0.0,   1.0, 0.0, # Bottom Right
	# 	-0.5, -0.5, 0.0,   0.0, 0.0, # Bottom Let
	# 	-0.5,  0.5, 0.0,   0.0, 1.0]  # Top Left 
	cube = numpy.array(cube, dtype=numpy.float32)

	# indices = [
	# 			0,  1,  2,  2,  3,  0,
	# 			4,  5,  6,  6,  7,  4,
	# 			8,  9, 10, 10, 11,  8,
	# 			12, 13, 14, 14, 15, 12,
	# 			16, 17, 18, 18, 19, 16,
	# 			20, 21, 22, 22, 23, 20
	# 		]
	# indices = [
	# 	0, 1, 3,
	# 	1, 2, 3
	# ]

	cube_positions = [
		( 0.0,  0.0,  0.0),
		( 2.0,5.0, -15.0),
		(-1.5, -2.2, -2.5),
		(-3.8, -2.0, -12.3),
		( 2.4, -0.4, -3.5),
		(-1.7,3.0, -7.5),
		( 1.3, -2.0, -2.5),
		( 1.5,2.0, -2.5),
		( 1.5,0.2, -1.5),
		(-1.3,1.0, -1.5),
	]
	# indices = numpy.array(indices, dtype=numpy.uint32)

	VAO = glGenVertexArrays(1)
	glBindVertexArray(VAO)

	shader = shaderLoader.compile_shader("./shaders/vertex_shader1.vs", "./shaders/fragment_shader1.fs")

	VBO = glGenBuffers(1) # vertex buffer object for GPU
	glBindBuffer(GL_ARRAY_BUFFER, VBO)
	#upload data to array buffer
	#                 buf type   byte  point     type
	glBufferData(GL_ARRAY_BUFFER, cube.itemsize * len(cube), cube, GL_STATIC_DRAW)

	# EBO = glGenBuffers(1)
	# glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
	# glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.itemsize * len(indices), indices, GL_STATIC_DRAW)

	#get position from vertex_shader variable
	position = glGetAttribLocation(shader, "position")
	glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(0))
	glEnableVertexAttribArray(position)

	#get color from vertex_shader program variable
	# color = glGetAttribLocation(shader, "color")
	# glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
	# glEnableVertexAttribArray(color)

	texture_cords = glGetAttribLocation(shader, "inTexCords")
	glVertexAttribPointer(texture_cords, 2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(12))
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

	image = Image.open("./res/block.jpg")
	flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)
	image_data = numpy.array(list(flipped_image.getdata()), numpy.uint8)
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)

	glUseProgram(shader)

	glClearColor(.2, .3, .2, 1.0)
	glEnable(GL_DEPTH_TEST)
	# glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

	#perspective part
	# view matrix
	# view = pyrr.matrix44.create_from_translation(pyrr.Vector3([.0, .0, -3.0]))
	# global view
	# projection matrix
	projection = pyrr.matrix44.create_perspective_projection(45.0, w_width / w_height, 0.1, 100.0)
	print("[PROJECTION MATRIX]")
	print(projection)


	view_location = glGetUniformLocation(shader, "view")
	projection_location = glGetUniformLocation(shader, "projection")
	model_location = glGetUniformLocation(shader, "model")

	# glUniformMatrix4fv(view_location, 1, GL_FALSE, view)
	glUniformMatrix4fv(projection_location, 1, GL_FALSE, projection)

	# rot_x = pyrr.matrix44.create_from_x_rotation(sin(glfw.get_time()) * 2)
	while not glfw.window_should_close(window):
		glfw.poll_events()
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		current_frame = glfw.get_time()
		delta_time = current_frame - last_frame
		last_frame = current_frame

		# pyrr.matrix44.create_look_at(eye, target, up, dtype=None)
		# radius = 10.0
		# camX = sin(glfw.get_time()) * radius
		# camZ = cos(glfw.get_time()) * radius
		# view = pyrr.matrix44.create_look_at(pyrr.Vector3([camX, 0.0, camZ]), pyrr.Vector3([0.0, 0.0, 0.0]), pyrr.Vector3([0.0, 1.0, 0.0]))
		global view
		print(type(cameraFront))
		view = pyrr.Matrix44.look_at(cameraPos, cameraPos + cameraFront, cameraUp)
		glUniformMatrix4fv(view_location, 1, GL_FALSE, view)

		for i in range(len(cube_positions)):
			model = pyrr.matrix44.create_from_translation(cube_positions[i])
			angle = 20.0 * i
			if i % 3 == 0:
				angle = glfw.get_time() * 25.5
			if i % 4 == 0:
				angle = sin(glfw.get_time()) * 50
			rot = pyrr.matrix44.create_from_axis_rotation(pyrr.Vector3([1.0, 0.3, 0.5]), radians(angle))
			model = pyrr.matrix44.multiply(rot, model)
			glUniformMatrix4fv(model_location, 1, GL_FALSE, model)
			glDrawArrays(GL_TRIANGLES, 0, 36)
		glfw.swap_buffers(window)
	
	glfw.terminate()

if __name__ == "__main__":
	main()