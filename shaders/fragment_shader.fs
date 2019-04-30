#version 410 core
in vec3 newColor;
in vec2 newTexCords;

out vec4 outColor;
uniform sampler2D sampleTex;
uniform vec4 color = vec4(1.0, 0.0, 0.0, 1.0);

void main()
{
	outColor = texture(sampleTex, newTexCords);// * vec4(newColor, 1.0f);
	outColor = color;
}