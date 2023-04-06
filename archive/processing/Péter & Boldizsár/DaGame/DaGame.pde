String name = "";
boolean game_started = false;

void setup(){
  size(1000, 1000);
  background(255);
  
  textAlign(CENTER, CENTER);
  textFont(createFont("Comic Sans MS", 30));
}

void draw(){
  background(255);
  if (!game_started){
    fill(0);
    text("Please type your name here:", 500, 450);
    text(name, 500, 550);
  }
  else
    text("Game is on", 500, 500);
}

void keyPressed(){
  if (keyCode == BACKSPACE && name.length() != 0) name = name.substring(0, name.length()-1);
  else if (keyCode == ENTER) game_started = true;
  else if (key != CODED && keyCode != BACKSPACE) name += key;
}
