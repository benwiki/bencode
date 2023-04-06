/////////////////////////////////////////////////////////////////

Map map;
int[] clicked;

int DEAD = 0, ALIVE = 1;
PVector prev, cur;

boolean pressed = false;
int turn_counter = 0;

//.................................................

void setup(){
  //fullScreen();
  size(700, 700);
  map = new Map(50);
  
  cur = new PVector();
  prev = new PVector();
  textFont(createFont("Comic Sans MS", 30));
}
//.................................................

void draw(){
  background(255);
  
  map.show();
  cur.set(map.track());
  
  if (pressed && !map.same(cur, prev)){
    prev.set(cur);
    map.set_cell(cur.copy());
  }
  
  fill(255,0,0);
  text(str(turn_counter), 100, 100);
}
//-------------------------------------------

void mousePressed(){
  pressed = true;
}
//-----------------------------------

void mouseReleased(){
  //map.set_cell(map.track());
  pressed = false;
}
//-----------------------------------

void keyPressed(){
  if (key == ' ')
    map.turn();
  if (key == 'e')
    map.erase();
  if(key == '+')
    ++map.cs;
  else if(key == '-')
    --map.cs;
  if(keyCode == UP)
    --map.y;
  else if(keyCode == DOWN)
    ++map.y;
  if(keyCode == LEFT)
    --map.x;
  else if(keyCode == RIGHT)
    ++map.x;
}

//////////////////////////////////////////////////////////////////
