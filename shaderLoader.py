from OpenGL.GL import *
import OpenGL.GL.shaders

def load_shader(shader_file):
	shader_source = ""
	with open(shader_file) as f:
		shader_source = f.read()
	f.close()
	return str.encode(shader_source)

def compile_shader(vs, fs):
	vertex_shader = load_shader(vs)
	fragment_shader = load_shader(fs)

	shader = OpenGL.GL.shaders.compileProgram(
		OpenGL.GL.shaders.compileShader(
			vertex_shader, GL_VERTEX_SHADER
		),
		OpenGL.GL.shaders.compileShader(
			fragment_shader, GL_FRAGMENT_SHADER
		)
	)
	return shader