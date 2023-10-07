
class Indicator{
  
  Player pmaster = emptyPlayer;
  Disk dmaster = emptyDisk;
  
  PVector pos;
  Timer time = new Timer();
  long timestate;
  float dist = 0,
        disttime = 800, // in milliseconds
        wid  = board.cs/5;
  
  Indicator (Disk dmaster){
    //this.pos = dmaster.movable.pos.copy();
    this.dmaster = dmaster;
    time.start();
  }
  
  Indicator (Player pmaster){
    //this.pos = pmaster.pbutton.pos.copy();
    this.pmaster = pmaster;
    time.start();
  }
  
  void show(){
    /*push();
    noFill();
    stroke(0,255,0, maxalpha/2);
    strokeWeight(wid);
    ellipseMode(CENTER);
    dist = map((disttime/2-(timestate) % disttime)*(timestate%(disttime*2)<disttime?1:-1), -disttime/2,disttime/2, board.cs,board.cs*2);
    ellipse(pos.x, pos.y, dist, dist);
    pop();*/
    timestate = time.state();
    if      (!pmaster.empty) pmaster.pbutton.alpha = map((disttime/2-timestate% disttime)*(timestate%(disttime*2)<disttime?1:-1),  -disttime/2,disttime/2,  maxalpha*0.45,maxalpha);
    else if (!dmaster.empty) dmaster.movable.alpha = map((disttime/2-timestate% disttime)*(timestate%(disttime*2)<disttime?1:-1),  -disttime/2,disttime/2,  maxalpha*0.45,maxalpha);
  }
}
