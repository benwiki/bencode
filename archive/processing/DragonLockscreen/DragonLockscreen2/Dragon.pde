
class Dragon {
  
  ArrayList<PVector> path = new ArrayList<PVector>();
  float speed = float(width+height)/500, late;
  
  int partnum = 20;
  float partWidth, partHeight, partDistance = 1.2;
  //DragonPart[] parts = new DragonPart[partnum];
  PVector[] parts = new PVector[partnum];
  DragonPart head;
  
  //=========================================================================
  Dragon(){
    partWidth = (width+height)/40;
    partHeight= partWidth;
    late = partWidth / speed / 3;
    
    path.add(new PVector(-partWidth*partnum, height/2));
    for (int i=1; i<3; ++i) path.add(randomVector());
    
    colorMode(HSB, 255);
    /*for (int i=0; i<partnum; ++i) 
      parts[i] = new DragonPart(this, (i+1)*late, color((i+1)/(float)partnum*255, 255, 255));*/
    for (int i=0; i<partnum; ++i) parts[i] = new PVector();
    head = new DragonPart(this, 0, #ffffff);
  }
  //-------------------------------------------------------------------------
  
  void move(){
    //for (int i=partnum; --i>=0;) parts[i].move();
    head.move();
    dragSegment(0, head.pos);
    for(int i=0; i<partnum-1; ++i) {
      dragSegment(i+1, parts[i]);
    }
    
    managePath();
  }
  
  void dragSegment(int i, PVector in) {
    PVector d = PVector.sub(in, parts[i]);
    float angle = atan2(d.y, d.x);
    parts[i].set(in.x - cos(angle) * partWidth / partDistance, 
                 in.y - sin(angle) * partWidth / partDistance);
    show(parts[i], angle);
  }
  //------------------------------------------------------------------
  
  void show(PVector p, float a) {
    pushMatrix();
    translate(p.x, p.y);
    rotate(a);
    rectMode(CENTER);
    rect(0, 0, partWidth, partWidth);
    //line(0, 0, segLength, 0);
    popMatrix();
  }
  //-----------------------------------------------
  
  private void managePath(){
    //if (parts[partnum-1].place == 3) {
    if (head.place == 3) {
      path.remove(0);
      --head.place;
      //for (int i=0; i<partnum; ++i) --parts[i].place;
    }
  }
  //------------------------------------------------
  
  void showPath(){
    head.line.show();
    //parts[partnum-1].line.show();
  }
  //-------------------------------------------------
  
  boolean goodPoint(PVector pt){
    return tangleDiff( path.get(path.size()-1), path.get(path.size()-2), path.get(path.size()-1), pt ) > PI/4 &&
           PVector.dist(path.get(path.size()-1), pt) >= width/4;
  }
  //---------------------------------------------------------------------
}
//////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////

class DragonPart {
  
  Dragon mr;
  Curve line;
  Timer timer = new Timer();
  float playtime, late;
  PVector pos = new PVector();
  boolean go=false, HEAD = false;
  color col;
  int place;
  
  //=======================================================================
  DragonPart(Dragon master, float late, color c){
    this.mr = master;
    this.late = late;
    this.col = c;
    if (late == 0) HEAD = true;
    playtime = PVector.dist(mr.path.get(0), mr.path.get(1)) / mr.speed;
    line = new Curve(mr.path.get(0), mr.path.get(0), mr.path.get(1), mr.path.get(2));
    place = 2;
    timer.start();
  }
  //-------------------------------------------------------------------
  
  void move() {
    if (!go && timer.get()<late) return;
    else if (!go) {
      timer.reset();
      go = true;
    }
    if (go && timer.get()>=playtime) {
      ++place;
      if (HEAD) mr.path.add(randomCheckedVector());
      line.set(mr.path.get(place-3), mr.path.get(place-2), mr.path.get(place-1), mr.path.get(place));
      playtime = line.length / mr.speed;
      timer.reset();
    }
    fill(col);
    pos.set(line.getEqPt(timer.get()/playtime));
    ellipse(pos.x, pos.y, mr.partWidth, mr.partHeight);
  }
  //------------------------------------------------------------------
}
