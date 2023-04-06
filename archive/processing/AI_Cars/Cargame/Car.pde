class Car //<>// //<>//
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
int starttime;
//Track track = new Track();

Car(){
 starttime = millis();
dead = false;
pos = new PVector(150, 80);
vel = new PVector(0, 0);
dead = false;
score = 0;
}

//--------------------------------------------------------------------------------------------------------

void show(){  
fill(0);
//point(pos.x, pos.y);
ellipse(pos.x, pos.y, 2, 2);
b = 200 * cos(a);
c = 200 * sin(a);
d = 200 * cos(a + .785);
e = 200 * sin(a + .785);

//line(pos.x, pos.y, pos.x + b, pos.y + c);
//line(pos.x, pos.y, pos.x + d, pos.y + e);
//line(pos.x, pos.y, pos.x + e, pos.y - d);
}

//---------------------------------------------------------------------------------------------------------

float[]braininput;

float[] braininput(){
 braininput = new float[7];
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
  a = vel.heading2D() + steering * r;
  vel.x = r * cos(a);
  vel.y = r * sin(a);
  vel.limit(8);
  
  dead = track.collision(pos.x, pos.y, pos.x + vel.x, pos.y + vel.y) || millis() >= starttime + 10000 ;
  if(gates.collision(pos.x, pos.y, pos.x + vel.x, pos.y + vel.y)) score++;
    
  pos.add(vel);
  
}

//------------------------------------------------------------------------------------------------------------



}
