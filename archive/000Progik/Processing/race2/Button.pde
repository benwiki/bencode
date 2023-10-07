class Button {
  
  PVector pos = new PVector(),
          size = new PVector();
  boolean pressed=false, visible=true, active=true, empty=false, firstshow=true;
  String type, name;
  float time=300;
  Timer timer = new Timer();
  
  Button(){empty=true;}
  
  Button(PVector pos, PVector size, String type, String name){
    this.pos.set(pos);
    this.size.set(size);
    this.type=type;
    this.name=name;
  }
  
  void show () {
    if (firstshow) {timer.start(); firstshow=false;}
    
    if (isOver()) fill(255,0,0);
    else fill(0);
    
    if (name=="add" && timer.get()<time) size.set(map(timer.get(), 0,time, 0,200),map(timer.get(), 0,time, 0,200));
    else size.set(200,200);
    
    rectMode(CORNERS);
    noStroke();
    rect(pos.x-size.x/2, pos.y-size.y/2, pos.x+size.x/2, pos.y+size.y/2, 50);
  }
  
  void press(){this.pressed=true;}
  
  boolean isOver(){
    if (mouseX>pos.x-size.x/2 && mouseX<pos.x+size.x/2 && mouseY>pos.y-size.y/2 && mouseY<pos.y+size.y/2) return true;
    else return false;
  }
  
}