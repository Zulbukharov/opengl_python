#version 410 core
in vec3 position; // py => shader
// in vec3 color; // py => shader
in vec2 inTexCords;
in vec3 vertexNormal;

// out vec3 newColor; // => GPU => window
out vec2 newTexCords;
out vec3 fragNormal;

uniform mat4 transform;
uniform mat4 light;
uniform mat4 view;
uniform mat4 projection;
uniform mat4 model;

void main()
{
	fragNormal = (light * vec4(vertexNormal, 0.0f)).xyz;
	gl_Position = projection * view * model * vec4(position, 1.0f);
	// newColor = color;
	newTexCords = inTexCords;
}