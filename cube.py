import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
import random

vertices = (
	(1, -1, -1),
	(1, 1, -1),
	(-1, 1, -1),
	(-1, -1, -1),
	(1, -1, 1),
	(1, 1, 1),
	(-1, -1, 1),
	(-1, 1, 1),
)

edges = (
	(0, 1),
	(0, 3),
	(0, 4),
	(2, 1),
	(2, 3),
	(2, 7),
	(6, 3),
	(6, 4),
	(6, 7),
	(5, 1),
	(5, 4),
	(5, 7),
)

surfaces = (
	(0, 1, 2, 3),
	(3, 2, 7, 6),
	(6, 7, 5, 4),
	(4, 5, 1, 0),
	(1, 5, 7, 2),
	(4, 0, 3, 6),
)

colors = (
	(1, 0, 0),
	(0, 1, 0),
	(1, 1, 0),
	(0, 0, 0),
	(1, 1, 1),
	(0, 1, 1),
	(0, 1, 1),
)

ground_vertices = (
	(-10, -1.1, 20),
	(10, -1.1, 20),
	(-10, -1.1, -300),
	(10, -1.1, -300),
)

def ground():
	glBegin(GL_QUADS)
	for vertex in ground_vertices:
		glColor3fv((0, 0.5, 0.5))
		glVertex3fv(vertex)
	glEnd()

def Cube(vertices):
	glBegin(GL_QUADS)
	for surface in surfaces:
		x = 0
		for vertex in surface:
			x += 1
			glColor3fv(colors[x])
			glVertex3fv(vertices[vertex])
	glEnd()

	glBegin(GL_LINES)
	for edge in edges:
		for vertex in edge:
			glVertex3fv(vertices[vertex])
	glEnd()

def set_vertices(max_distance, min_distance = 20):
	x_value_change = random.randrange(-10, 10)
	y_value_change = 0 #random.randrange(-10, 10)
	z_value_change = random.randrange(-1 * max_distance, min_distance)

	new_vertices = []
	for vert in vertices:
		new_vert = []
		new_x = vert[0] + x_value_change
		new_y = vert[1] + y_value_change
		new_z = vert[2] + z_value_change
		new_vert.append(new_x)
		new_vert.append(new_y)
		new_vert.append(new_z)
		new_vertices.append(new_vert)
	return new_vertices

def main():
	pygame.init()
	display = (800, 600)
	max_distance = 100
	pygame.display.set_mode(display, DOUBLEBUF | OPENGL) # buffer in the background
	gluPerspective(45, (display[0]/display[1]), 0.1, max_distance) #FOV, aspect ratio, clipping plain
	glTranslatef(random.randrange(-5,5), random.randrange(-5,5), -40)
	
	x_move = 0
	y_move = 0
	cube_dict = {}

	for x in range(20):
		cube_dict[x] = set_vertices(max_distance)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					quit()
				elif event.key == pygame.K_LEFT:
					x_move = 0.3
				elif event.key == pygame.K_RIGHT:
					x_move = -0.3
				elif event.key == pygame.K_UP:
					y_move = 0.3
				elif event.key == pygame.K_DOWN:
					y_move = -0.3
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					x_move = 0
				elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					y_move = 0
		#keys = pygame.key.get_pressed()
		#if keys[pygame.K_LEFT]:
		#	glRotatef(1, 0, 1, 0)
		#if keys[pygame.K_RIGHT]:
		#	glRotatef(1, 0, -1, 0)
		#glRotatef(1, 1, 3, 1) # angle, x, y, z
		x = glGetDoublev(GL_MODELVIEW_MATRIX)
		#print(x)
		camera_z = x[3][2]
		camera_x = x[3][0]
		camera_y = x[3][1]
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) #clear frame
		glTranslatef(x_move, y_move, 0.1)

		#ground()
		for each_cube in cube_dict:
			Cube(cube_dict[each_cube])
		
		for each_cube in cube_dict:
			if camera_z <= cube_dict[each_cube][0][2]:
				print("passed a cube")
				new_max = int(-1 * (camera_z - max_distance))
				cube_dict[each_cube] = set_vertices(new_max, int(camera_z))
		pygame.display.flip()
		pygame.time.wait(10)

main()
pygame.quit()
quit()
