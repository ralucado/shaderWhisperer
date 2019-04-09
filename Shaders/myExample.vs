#version 330 core

layout (location = 0) in vec3 vertex;
layout (location = 1) in vec3 normal;
layout (location = 2) in vec3 color;
layout (location = 3) in vec2 texCoord;

out vec4 frontColor;
out vec2 vtexCoord;

uniform mat4 modelViewProjectionMatrix;
uniform mat3 normalMatrix;

uniform float time;
uniform float amplitude=0.1;
uniform float freq=1;

float PI=acos(-1.0);

vec4 foo(vec3 N){
	return vec4(color, 1.0)*N.z;
}

void main() {
    vec3 N = normalize(normalMatrix*normal);
    frontColor=foo(N);
    gl_Position=modelViewProjectionMatrix*vec4(vertex, 1);
}




uniform mat4 modelViewProjectionMatrix;
uniform mat4 modelViewMatrix;
uniform mat3 normalMatrix; 

void main() {
    vec3 N;
    N = normalize(normalMatrix*normal);
    bool a = true; 
    while(a){
		frontColor = vec4(color, 1.0)*N.z;
		a = false;
    }
    P = (modelViewMatrix*vec4(vertex, 1)).xyz; //P = eye
    if(a)
    	P=(modelViewMatrix*vec4(vertex, 1)).xyz; //P = wrong
    else
    	P=(modelViewProjectionMatrix*vec4(vertex, 1)).xyz; //window
    gl_Position=modelViewProjectionMatrix*vec4(vertex, 1); //wrong,window
}

