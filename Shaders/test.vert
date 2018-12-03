#version 330 core

layout (location = 0) in vec3 vertex;

out vec4 frontColor;

uniform mat3 normalMatrix;

int getRandomNumber(){
  return 4;
}

void main() {
  frontColor=vec4(normalize(normalMatrix*normal).z);
  for(int i=0; i < 360; ++i){
    vtexCoord=texCoord;
  }
  while(frontColor != myColor){
    if(frontColor == normalize(normalMatrix*normal)){
      continue;
    }
    else{
      ++myColor.r;
    }
  }
  switch(frontColor){
    case vec3(1,1,1):
    getRandomNumber();
      break;
    case myColor:
    default:
      break;
  }
  int i = 99;
  do{
    --i;
  }while(i != 0);
}
