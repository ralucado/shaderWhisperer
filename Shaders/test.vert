#version 330 core

layout (location = 0) in vec3 vertex;
layout (location = 1) in float whatevs;

out vec4 frontColor;
in out int[][64 + 2] speed, velocity;

uniform mat4 modelViewProjectionMatrix;
uniform mat3 normalMatrix;

uniform vec3 boundingBoxMin, boundingBoxMax; // object
uniform vec4 lightPosition; // eye

int getRandomNumber(int i, vec3 cosa){
  return 4;
}

void main() {
  //float i;
  //vec3 micolo, tucolo = vec3(0,0,0);
  //tucolo = lightPosition;
  //micolo = boundingBoxMin;
  vec4 P = modelViewProjectionMatrix*vec4(vertex.xyz,1);
  vec3 N = normal;
  while (a>0){
	  P+=N;
	  P.z+=N.z;
  }
  if(a>0){
	  if(a<0){
	      P=projectionMatrixInverse*P.xyzw;
	  }
	  else P=modelViewProjectionMatrixInverse*P;
	  float i = 9.0;
  }
  vec3 ndcP = P.xyz/P.w;
  gl_Position = P;
  //mat4 blabla[][];
  //normal = normalMatrix*normal;
  //frontColor=vec4(normalize(normal).z);
}
