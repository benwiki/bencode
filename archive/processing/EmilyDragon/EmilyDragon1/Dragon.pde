
class Dragon {
  
  //ArrayList<PVector> path = new ArrayList<PVector>();
  //float speed = float(width+height)/5000, late;
  float speed = float(width+height)/1000, late;
  
  int partnum = 15;
  float partWidth, partHeight, partDistance = 1.2;
  DragonPart[] parts = new DragonPart[partnum];
  DragonPart head;
  boolean gotpictures = false;
  PVector newGoal = new PVector();
  int usedNewGoal = 0;
  
  PImage headimg, bodyimg, tailimg;
  
  //=========================================================================
  Dragon(){
    partWidth = (width+height)/20;
    partHeight = partWidth;
    late = partWidth / speed / 3.5 / 1.2;
    
    //path.add(new PVector(0, height/2));
    //for (int i=1; i<3; ++i) path.add(randomVector());
    
    imageMode(CENTER);
    headimg = requestImage("head.png");
    bodyimg = requestImage("bodypart.png");
    tailimg = requestImage("tail.png");
    
    
    colorMode(HSB, 255);
    PVector firstGoals[] = {randomVector(), randomVector(), randomVector()};
    for (int i=0; i<partnum; ++i) 
      parts[i] = new DragonPart(this, i, firstGoals); //, (i+1)*late, color((i+1)/(float)partnum*255, 255, 255));
    //head = new DragonPart(this, -1, 0, #ffffff);
  }
  //-------------------------------------------------------------------------
  
  void move(){
    if (headimg.width>0 && bodyimg.width>0 && tailimg.width>0){
      headimg.resize(int(partWidth), int(partHeight));
      bodyimg.resize(int(partWidth), int(partHeight));
      tailimg.resize(int(partWidth), int(partHeight));
      this.gotpictures = true;
    }
    //for (DragonPart part: parts) part.move();
    for (int i=partnum; --i>=0;) parts[i].move();
    //head.move();
    //managePath();
  }
  //-----------------------------------------------
  
  //private void managePath(){
  //  if (parts[partnum-1].place == 3) {
  //    path.remove(0);
  //    --head.place;
  //    for (int i=0; i<partnum; ++i) --parts[i].place;
  //  }
  //}
  //------------------------------------------------
  
  void showPath(){
    //parts[0].line.show();
    //parts[partnum-1].line.show();
    for (int i=partnum; --i>=0;) parts[i].line.show();
  }
  //-------------------------------------------------
  
  void showTimers() {
    for (int i=0; i<partnum; ++i) {
      stroke(0);
      strokeWeight(3);
      line(20, (i+1)*20, 20 + parts[i].timer.get()/parts[i].playtime*50, (i+1)*20);
    }
  }
  
  private void _addGoalToPath(){
    
  }
  
  boolean goodPoint(PVector pt){
    /*float angle, distance;
    do {
      angle = random(-PI/2, PI/2);
      angle = tangle(path.get(path.size()-1), path.get(path.size()-2)) + (angle<0 ? -PI/4 : PI/2) + angle;
    } while();
    distance = random(width/4, */
    int headPathEnd = parts[0].path.size();
    return tangleDiff(parts[0].path.get(headPathEnd-1),
                      parts[0].path.get(headPathEnd-2),
                      parts[0].path.get(headPathEnd-1), pt) > PI/4 &&
           PVector.dist(parts[0].path.get(headPathEnd-1), pt) >= width/1;
  }
  //---------------------------------------------------------------------
}
//////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////

class DragonPart {

  Dragon mr; // mr = master
  
  Curve line;
  
  Timer timer = new Timer();
  float playtime;
  
  PVector pos = new PVector();
  ArrayList<PVector> path = new ArrayList<PVector>();
  
  boolean HEAD = false, TAIL = false, can_go = false;

  int place, whichpart, pathEnd;
  
  //=======================================================================
  DragonPart(Dragon master, int whichpart, PVector[] firstGoals) { //, float late, color c){
    this.mr = master;
    
    HEAD = (whichpart == 0);
    TAIL = (whichpart == mr.partnum-1);
    this.whichpart = whichpart;
    
    for (int i=0; i<3; ++i) path.add(firstGoals[i]);
    line = new Curve(path.get(0), path.get(0), path.get(1), path.get(2));
    
    playtime = line.length / mr.speed;
    this.timer.start();
  }
  //-------------------------------------------------------------------
  
  void move() {
    if (!can_go && this.timer.get() < whichpart * mr.late) return;
    else if (!can_go) {
      this.timer.reset();
      can_go = true;
    }
    
    if (this.timer.get() >= playtime) {
      //if (mr.usedNewGoal == 0) {
      //  mr.newGoal.set(randomCheckedVector());
      //  ++mr.usedNewGoal;
      //  println(whichpart, path);
      //}
      //else if (mr.usedNewGoal == mr.partnum) {
      //  mr.usedNewGoal = 0;
      //}
      //else ++mr.usedNewGoal;
      if (HEAD) mr.newGoal.set(randomCheckedVector());

      this.setNewPathGoal(mr.newGoal.copy());
      //if (mr.usedNewGoal == 1) println(path);
    }

    this.pos.set(line.getPt(this.timer.get()/playtime));
    
    pushMatrix();
    translate(pos.x, pos.y);
    if (HEAD) {
      rotate(tangle(pos, mr.parts[1].pos, PI*0.7));
      image(mr.headimg, 0, 0);
    }
    else if (TAIL) {
      rotate(tangle(pos, mr.parts[mr.partnum-2].pos, -PI/2));
      image(mr.tailimg, 0, 0);
    }
    else {
      rotate(tangle(pos, mr.parts[whichpart+1].pos, -PI*0.2));
      image(mr.bodyimg, 0, 0);
    }
    popMatrix();
  }
  //------------------------------------------------------------------
  
  void setNewPathGoal (PVector goal) {
    this.path.add(goal);
    
    pathEnd = path.size()-1;
    line.set(path.get(pathEnd-3),
             path.get(pathEnd-2),
             path.get(pathEnd-1),
             path.get(pathEnd));
             
    this.playtime = line.length / mr.speed;
    this.timer.reset();
  }
}
