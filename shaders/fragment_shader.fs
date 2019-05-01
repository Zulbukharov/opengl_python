#version 410 core
in vec3 newColor;
in vec2 newTexCords;
in vec3 fragNormal;

out vec4 outColor;
uniform sampler2D sampleTex;
// uniform vec4 color = vec4(1.0, 0.0, 0.0, 1.0);

void main()
{
	vec3 ambientLightIntensity = vec3(0.3f, 0.2f, 0.4f);
	vec3 sunLightIntensity = vec3(0.9f, 0.9f, 0.9f);
	vec3 sunLightDirection = normalize(vec3(0.0f, 0.0f, 2.0f));

	vec4 texel = texture(sampleTex, newTexCords);
	vec3 lightIntensity = ambientLightIntensity + sunLightIntensity *
		max(dot(fragNormal, sunLightDirection), 0.0f);
	outColor = vec4(texel.rgb * lightIntensity, texel.a);// * vec4(newColor, 1.0f);
}