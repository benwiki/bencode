class Car //<>// //<>// //<>// //<>// //<>// //<>// //<>// //<>//
{
PVector pos;
PVector vel;
float a;
float b;
float c;
float d;
float e;
float r;
boolean dead;
int score;
int own_iteration=iteration;
color carcolor;
float size=1.0;

Car(){
  dead = false;
  pos = handler.startingPoint.pos.copy();
  vel = new PVector(0, 0);
  score = 0;
}

//--------------------------------------------------------------------------------------------------------

void show(){  
  b = 10 * cos(a);
  c = 10 * sin(a);
  d = 200 * cos(a + .785);
  e = 200 * sin(a + .785);
  
  push();
  fill(carcolor);
  stroke(carcolor);
  strokeWeight(3*size);
  //ellipse(pos.x, pos.y, 3*size, 3*size);
  line(pos.x, pos.y, pos.x + b, pos.y + c);
  pop();
  stroke(0);
  fill(0);
  
  /*strokeWeight(1);
  line(pos.x, pos.y, pos.x + b, pos.y + c);
  line(pos.x, pos.y, pos.x + d, pos.y + e);
  line(pos.x, pos.y, pos.x + e, pos.y - d);*/
}

//---------------------------------------------------------------------------------------------------------

float[]braininput;

float[] braininput(){
  braininput = new float[5];
  if(track.collision(pos.x, pos.y, pos.x + b, pos.y + c)) braininput[1] = track.distance(pos.x, pos.y, pos.x + b, pos.y + c);
  if(track.collision(pos.x, pos.y, pos.x + d, pos.y + e)) braininput[2] = track.distance(pos.x, pos.y, pos.x + d, pos.y + e);
  if(track.collision(pos.x, pos.y, pos.x + e, pos.y - d)) braininput[0] = track.distance(pos.x, pos.y, pos.x + e, pos.y - d);
  braininput[3] = vel.mag();
  braininput[4] = 1;
  return braininput;
}

//--------------------------------------------------------------------------------------------------------

void drive(float gas, float steering){
  
  if(!(gas <= 0 && vel.mag() <= gas * -1)) r = vel.mag() + gas;
  else r = .00001;
  a = vel.heading() + steering * r;
  vel.x = r * cos(a);
  vel.y = r * sin(a);
  vel.limit(8);
  
  if (track.collision(pos.x, pos.y, pos.x + vel.x, pos.y + vel.y)){
    if (carcolor != color(255, 0, 0)) carcolor = color(0,255,0);
    dead = true;
  }
  else if (iteration >= own_iteration + dead_iteration){
    carcolor = color(170,0,250);
    dead = true;
  }
      
  //dead = track.collision(pos.x, pos.y, pos.x + vel.x, pos.y + vel.y) || millis() >= starttime + 10000;
  if(gates.collision(pos.x, pos.y, pos.x + vel.x, pos.y + vel.y)){
    ++score;
    own_iteration = iteration;
  }
  
  pos.add(vel);
  
}

//------------------------------------------------------------------------------------------------------------



}
