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