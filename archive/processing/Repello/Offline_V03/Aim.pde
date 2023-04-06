class Aim{
  
  Button start, end;
  Player pmaster, dmaster;
  String mode;
  float way;
  boolean alive=true, killing_it=false;
  
  //=====
  Aim(){}
  //=====

  Aim(String mode, Player pmaster){
    this.mode = mode;
    this.pmaster = pmaster;
    
    if (mode=="placing"){
      start = new Button("aimstart", pmaster.pos.x, pmaster.pos.y, pmaster.pbutton.w, pmaster.pbutton.h, 0,
                         0, color(255,0,0), 0, color(255,0,0), maxalpha/1.2, "circle");
      start.set_size(pmaster.pbutton.w*1.5, pmaster.pbutton.h*1.5, 250);
    }
    else
      start = new Button("aimstart", pmaster.place.pos.x, pmaster.place.pos.y, pmaster.place.w, pmaster.place.h, 0,
                         0, color(255,0,0), 0, color(255,0,0), maxalpha/1.2, "rect");
    start.be_visible();
    start.amaster = this;
    addToBottomExe.add(start);
    
    end = new Button("aimend", pmaster.pos.x, pmaster.pos.y, board.cs, board.cs, 0,
                     0, color(255,0,0), 0, color(255,0,0), 0, "rect");
    end.be_visible();
    end.amaster = this;
    addToBottomExe.add(end);
  }
  //----------------------------------------------------------------------------------------------------------------
  
  void show(){
    if (killing_it && !start.sliding && !start.sizechange && !end.sliding && !end.sizechange){
      removeFromExe.add(start);
      removeFromExe.add(end);
      killing_it = false;
      alive = false;
    }
  }
  //-----------------------------------------------------------------------------------------------------------------
  
  void kill(){
    if (mode=="placing")
      start.set_size(pmaster.pbutton.w, pmaster.pbutton.h, 250);
    killing_it=true;
  }
  
}
