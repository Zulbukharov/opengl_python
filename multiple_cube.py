import glfw
from OpenGL.GL import *
import numpy
import pyrr # matrix, vector math
from PIL import Image
from math import *
import shaderLoader

cube_positions = []
cameraPos   =pyrr.Vector3([0.0, 0.5,  2.0])
cameraFront =pyrr.Vector3([0.0, 0.0, -1.0])
cameraUp    =pyrr.Vector3([0.0, 1.0,  0.0])
delta_time 	= 0.0
last_frame 	= 0.0
view = pyrr.Matrix44.look_at(cameraPos, cameraPos + cameraFront, cameraUp)
yaw    = -90.0 #Yaw is initialized to -90.0 degrees since a yaw of 0.0 results in a direction vector pointing to the right (due to how Eular angles work) so we initially rotate a bit to the left.
pitch  =  0.0
lastX  =  1920 / 2.0
lastY  =  1080 / 2.0
fov =  45.0
firstMouse = True
keys = [False] * 1024

def scroll_callback(window, xoffset, yoffset):
	global fov
	if fov >= 1.0 and fov <= 45.0:
		fov -= yoffset
	if fov <= 1.0:
		fov = 1.0
	if fov >= 45.0:
		fov = 45.0

def do_movement():
	global cameraFront, cameraPos, cameraUp, view, delta_time, keys, cube_positions
	cameraSpeed = 2.5 * delta_time
	###
	# To determine if two spheres are colliding, we take the sum of the 
	# radiuses and compare it with the length from the centers of 
	# the spheres. If the length is smaller than the sum of the radiuses, 
	# we have a collision.
	###
	old_camera_pos = pyrr.Vector3([cameraPos.x, cameraPos.y, cameraPos.z])
	# print(old_camera_pos)
	if keys[glfw.KEY_W]:
		cameraPos += cameraSpeed * cameraFront
		# print("press")
		# print(cameraPos)
	if keys[glfw.KEY_S]:
		cameraPos -= cameraSpeed * cameraFront
	if keys[glfw.KEY_A]:
		cameraPos -= pyrr.vector.normalise(pyrr.vector3.cross(cameraFront, cameraUp)) * cameraSpeed
	if keys[glfw.KEY_D]:
		cameraPos += pyrr.vector.normalise(pyrr.vector3.cross(cameraFront, cameraUp)) * cameraSpeed
	for i in range (len(cube_positions)):
		vecd = cameraPos - cube_positions[i]
		dist = sqrt(pow(vecd.x, 2) + pow(vecd.y, 2) + pow(vecd.z, 2))	
		if dist < 1: # s1.radius + s2.radius
			# print("old")
			# print(cameraPos)
			# print("new")
			# del(cameraPos)
			cameraPos = old_camera_pos[:]
			# print(cameraPos)
			return

def mouse_callback(window, xpos, ypos):
	global firstMouse, yaw, pitch, lastX, lastY, fov, cameraFront

	if firstMouse:
		lastX = xpos
		lastY = ypos
		firstMouse = False

	xoffset = xpos - lastX
	yoffset = lastY - ypos # Reversed since y-coordinates go from bottom to left
	lastX = xpos
	lastY = ypos

	sensitivity = 0.25	# Change this value to your liking
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
	if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
		glfw.set_window_should_close(window, True)
	if key >= 0 and key < 1024:
		if action == glfw.PRESS:
			keys[key] = True
		elif action == glfw.RELEASE:
			keys[key] = False

def main():
	global delta_time
	global last_frame
	global cameraPos
	# global cameraFront
	if not glfw.init():
		return
	w_width = 1920
	w_height = 1080
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
	glfw.set_input_mode(window, glfw.STICKY_KEYS, GL_TRUE) 
	# Enable key event callback
	# if glfw. MotionSupported():
	# glfw.set_input_mode(window, glfw.GLFW_RAW_MOUSE_MOTION, glfw.TRUE)
	glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
	glfw.set_key_callback(window, key_event)

	glfw.set_cursor_pos_callback(window, mouse_callback)

	glfw.set_scroll_callback(window, scroll_callback)

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
		-0.5,  0.5, -0.5,  0.0, 1.0,
		#ground
		-10,   -1.1, 20,   0.0, 0.0,
		 10,   -1.1, 20,   0.0, 1.0,
		-10,   -1.1, -300, 1.0, 1.0,
		 10,   -1.1, -300, 1.0, 0.0
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


	global cube_positions
	cube_positions = [
		pyrr.Vector3([ 0.0,  0.0,  0.0]),
		pyrr.Vector3([ 2.0,5.0, -15.0]),
		pyrr.Vector3([-1.5, -2.2, -2.5]),
		pyrr.Vector3([-3.8, -2.0, -12.3]),
		pyrr.Vector3([ 2.4, -0.4, -3.5]),
		pyrr.Vector3([-1.7,3.0, -7.5]),
		pyrr.Vector3([ 1.3, -2.0, -2.5]),
		pyrr.Vector3([ 1.5,2.0, -2.5]),
		pyrr.Vector3([ 1.5,0.2, -1.5]),
		pyrr.Vector3([-1.3,1.0, -1.5]),
	]

	# ground_vertices = [
	# 	-10, -1.1, 20,
	# 	10, -1.1, 20,
	# 	-10, -1.1, -300,
	# 	10, -1.1, -300,
	# ]
	# indices = numpy.arraypyrr.Vector3([indices, dtype=numpy.uint32)

	VAO = glGenVertexArrays(1)
	glBindVertexArray(VAO)

	shader = shaderLoader.compile_shader("./shaders/vertex_shader1.vs", "./shaders/fragment_shader1.fs")

	VBO = glGenBuffers(1) # vertex buffer object for GPU
	glBindBuffer(GL_ARRAY_BUFFER, VBO)
	#upload data to array buffer
	#                 buf type   byte  point     type
	glBufferData(GL_ARRAY_BUFFER, cube.itemsize * len(cube), cube, GL_STATIC_DRAW)

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

	# glClearColor(.2, .3, .2, 1.0)
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
		w = 0
		glfw.poll_events()
		do_movement()
		
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
		# cameraPos.y = 0.5
		
		view = pyrr.Matrix44.look_at(cameraPos, cameraPos + cameraFront, cameraUp)
		glUniformMatrix4fv(view_location, 1, GL_FALSE, view)
		# model = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0, 0.0, 0.0]))
		# glUniformMatrix4fv(model_location, 1, GL_FALSE, model)
		# for i in range(len(cube_positions)):
		# 	if int(cameraPos.x) == int(cube_positions[i][0]) and \
		# 		int(cameraPos.y) == int(cube_positions[i][1]) and \
		# 		int(cameraPos.z) == int(cube_positions[i][2]):
		# 		w = 1
		# if w:
		# 	w = 0
		# 	continue
		# glDrawArrays(GL_TRIANGLES, 36, 39)

		# cube_positions_len = len(cube_positions) - 20w
		# print(cameraPos.z)
		# for i in range(len(cube_positions)):
		# 	if int(cube_positions[i][2]) >= int(cameraPos.z):
		# 		return
# 		rangeIntersect: function(min0, max0, min1, max1) {
# 		return Math.max(min0, max0) >= Math.min(min1, max1) && 
# 			   Math.min(min0, max0) <= Math.max(min1, max1);
# 	},

# 	rectIntersect: function(r0, r1) {
# 		return utils.rangeIntersect(r0.x, r0.x + r0.width, r1.x, r1.x + r1.width) &&
# 			   utils.rangeIntersect(r0.y, r0.y + r0.height, r1.y, r1.y + r1.height);
# }	
		rot_x = pyrr.matrix44.create_from_x_rotation(sin(glfw.get_time()) * 2)
		for i in range(len(cube_positions)):
			model = pyrr.matrix44.create_from_translation(cube_positions[i])
			# print(model)
			angle = 0
			# # angle = i
			# if i % 3 == 0:
				# angle = glfw.get_time() * 180
				# angle = sin(radians(angle)) * cos(radians(angle))
			# # if i % 4 == 0:
			# 	# angle = sin(glfw.get_time()) * 50
			# if i == 8:
			# 	# angle = 0
			# 	angle = sin(glfw.get_time()) * 50
			# if i % 3 == 0:
				# rot = 
				# model = pyrr.matrix44.multiply(rot_x, model)
				# if w == 0:
					# print(model)
			if i == 0:
# radius = 100
# for angle in range(0, 361):
#     theta = math.radians(angle)
#     x = radius*math.cos(theta)
#     y = radius*math.sin(theta)
#     print(x, y)
				# rot = pyrr.matrix44.create_from_axis_rotation(cameraFront, 1)
				# rot = pyrr.matrix44.create_from_translation(cameraFront + camera)
				# pyrr.matrix44.create_from_x_rotation()
				radius = 4
				theta = radians(glfw.get_time() * 100)
				rot_y = pyrr.matrix44.create_from_y_rotation(glfw.get_time() * 0.5)
				# X := originX + cos(angle)*radius;
				# Y := originY + sin(angle)*radius;
				cube_positions[0][0] = cameraPos.x + cos(theta) * radius
				cube_positions[0][1] = cameraPos.y
				cube_positions[0][2] = cameraPos.z + sin(theta) * radius
				model = pyrr.matrix44.multiply(rot_y, model)
				# model = pyrr.matrix44.create_from_translation(cube_positions[0])

				# model = pyrr.matrix44.multiply(cube_positions[i]), model)
				# model = pyrr.Matrix44.look_at(cube_positions[i], cube_positions[i] + cameraFront, cameraUp)
				# model = pyrr.matrix44.inverse(model)
			# rot = pyrr.matrix44.create_from_axis_rotation(pyrr.Vector3([]), angle)
			glUniformMatrix4fv(model_location, 1, GL_FALSE, model)
			glDrawArrays(GL_TRIANGLES, 0, 36)
			# w = 1
			
		# glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
		glfw.swap_buffers(window)
	
	glfw.terminate()

if __name__ == "__main__":
	main()