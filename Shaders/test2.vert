#version 330 core

layout (location = 0) in vec3 vertex;
layout (location = 1) in float whatevs;

out vec4 frontColor;
in out int[][64 + 2] speed, velocity;

uniform mat4 modelViewProjectionMatrix;
uniform mat3 normalMatrix;

int foo(int[] a, mat3 whatev){
  float i, otheri;
  if(true){
    bool wat;
  }
}

void main() {
  float i;
  vec3 micolo, tucolo = vec3(0,0,0);
  mat4 blabla[][];
  frontColor=vec4(normalize(normalMatrix*normal).z);
  frontColor += vec3(1,1,1);
  int i = 99;
}
