#version 330 core

layout (location = 0) in vec3 vertex;
layout (location = 1) in float whatevs;

out vec4 frontColor;
in out int[][64 + 2] speed, velocity;

uniform mat3 normalMatrix;

int getRandomNumber(int i, vec3 cosa){
  return 4;
}

void main() {
  float i;
  frontColor=vec4(normalize(normalMatrix*normal).z);
  for(int i=0; i < 360; ++i){
    vtexCoord=texCoord;
  }
  while(frontColor != myColor && speed[][] > 10 && vertex.xyz != frontColor.rgb){
    if(frontColor == normalize(normalMatrix*normal)){
      frontColor += vec3(1,1,1);
      frontColor.b += 2;
      continue;
    }
    else if(1 == 1){
        frontColor.b += 3;
    }
    else{
      ++myColor.r;
      velocity = speed;
    }
  }
  switch(frontColor){
    case vec3(1,1,1):
    getRandomNumber();
    frontColor();
      break;
    case myColor:
    default:
      break;
  }
  int i = 99; //decl and assig are ok
  do{
    --i;
  }while(i != 0);
}
