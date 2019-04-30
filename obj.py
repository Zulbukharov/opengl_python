import glfw
from OpenGL.GL import *
import numpy
import pyrr # matrix, vector math
from PIL import Image
from math import *
import shaderLoader
from objLoader import *

def key_event(window,key,scancode,action,mods):
	if action == glfw.REPEAT or action == glfw.PRESS:
		if key == glfw.KEY_ESCAPE:
			glfw.set_window_should_close(window, GL_TRUE)
		if key == glfw.KEY_W:
			model[3][2] += .5
		elif key == glfw.KEY_S:
			model[3][2] -= .5
		elif key == glfw.KEY_A:
			model[3][0] += .5
		elif key == glfw.KEY_D:
			model[3][0] -= .5
		elif key == glfw.KEY_R:
			model[3][1] += .5
		elif key == glfw.KEY_F:
			model[3][1] -= .5

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

	#when window resize
	# glfw.set_window_size_callback(window, window_resize)
	obj = ObjLoader()
	obj.load_model("./res/hito.obj")

	VAO = glGenVertexArrays(1)
	glBindVertexArray(VAO)

	shader = shaderLoader.compile_shader("./shaders/vertex_shader.vs", "./shaders/fragment_shader.fs")

	VBO = glGenBuffers(1) # vertex buffer object for GPU
	glBindBuffer(GL_ARRAY_BUFFER, VBO)
	#upload data to array buffer
	#                 buf type   byte  point     type
	glBufferData(GL_ARRAY_BUFFER, obj.model.itemsize * len(obj.model), obj.model, GL_STATIC_DRAW)

	#get position from vertex_shader variable
	position = glGetAttribLocation(shader, "position")
	glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, obj.model.itemsize * 3, ctypes.c_void_p(0))
	glEnableVertexAttribArray(position)

	texture_cords = glGetAttribLocation(shader, "inTexCords")
	texture_offset = len(obj.vertex_index)*12
	glVertexAttribPointer(texture_cords, 2, GL_FLOAT, GL_FALSE, obj.model.itemsize * 2, ctypes.c_void_p(texture_offset))
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

	image = Image.open("./res/cube_texture.jpg")
	flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)
	image_data = numpy.array(list(flipped_image.getdata()), numpy.uint8)
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)
	# glTexImage2D()

	glUseProgram(shader)

	glClearColor(.2, .3, .2, 1.0)
	glEnable(GL_DEPTH_TEST)
	glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)


	#perspective part
	# view matrix
	view = pyrr.matrix44.create_from_translation(pyrr.Vector3([.0, .0, -3.0]))
	# global view
	# projection matrix
	projection = pyrr.matrix44.create_perspective_projection(90.0, w_width / w_height, 0.1, 100.0)
	# model position matrix
	global model
	model = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0, 0.0, -30.0]))


	view_location = glGetUniformLocation(shader, "view")
	projection_location = glGetUniformLocation(shader, "projection")
	model_location = glGetUniformLocation(shader, "model")

	glUniformMatrix4fv(view_location, 1, GL_FALSE, view)
	glUniformMatrix4fv(model_location, 1, GL_FALSE, model)
	glUniformMatrix4fv(projection_location, 1, GL_FALSE, projection)

	while not glfw.window_should_close(window):
		glfw.poll_events()
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		rot_x = pyrr.Matrix44.from_x_rotation(.5 * glfw.get_time())
		rot_y = pyrr.Matrix44.from_y_rotation(.8 * glfw.get_time())

		transform_location = glGetUniformLocation(shader, "transform")
		# glUniformMatrix4fv(transform_location, 1, GL_FALSE, rot_x * rot_y)
		glUniformMatrix4fv(transform_location, 1, GL_FALSE, rot_y)
		glUniformMatrix4fv(model_location, 1, GL_FALSE, model)
		# glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
		glDrawArrays(GL_TRIANGLES, 0, len(obj.vertex_index))
		glfw.swap_buffers(window)
	
	glfw.terminate()

if __name__ == "__main__":
	main()