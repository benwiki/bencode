
class Dragon {
  
  ArrayList<PVector> path = new ArrayList<PVector>();
  //float speed = float(width+height)/5000, late;
  float speed = normalDragonSpeed, late;
  
  int partnum = 15, usedNewGoal = 0;
  float partWidth, partHeight, partDistance = 1.2;
  DragonPart[] parts = new DragonPart[partnum];
  DragonPart head;
  boolean gotpictures = false;
  
  PImage headimg, bodyimg, tailimg;
  
  //=========================================================================
  Dragon(PVector startingPoint){
    partWidth = (width+height)/20;
    //partWidth=width/6;
    partHeight= partWidth;
    //late = partWidth / speed / 2.3;
    late = partWidth / speed / 3.5 / 1.2;
    
    //path.add(new PVector(0, height/2));
    path.add(startingPoint.copy());
    for (int i=1; i<3; ++i) path.add(randomVector());
    
    imageMode(CENTER);
    //runOnUiThread(new Runnable() {
    //    @Override
    //    public void run() {
    
    //        headimg = requestImage("head.png");
    //bodyimg = requestImage("bodypart.png");
    //tailimg = requestImage("tail.png");
    
    //    }
    //});
    headimg = requestImage("head.png");
    bodyimg = requestImage("bodypart.png");
    tailimg = requestImage("tail.png");
    
    
    colorMode(HSB, 255);
    for (int i=0; i<partnum; ++i) 
      parts[i] = new DragonPart(this, i, (i+1)*late, color((i+1)/(float)partnum*255, 255, 255));
    head = new DragonPart(this, -1, 0, #ffffff);
  }
  //-------------------------------------------------------------------------
  
  void move(){
    if (headimg.width>0 && bodyimg.width>0 && tailimg.width>0){
      //println(partWidth, partHeight, width, height);
      headimg.resize(int(partWidth), int(partHeight));
      bodyimg.resize(int(partWidth), int(partHeight));
      tailimg.resize(int(partWidth), int(partHeight));
      this.gotpictures = true;
    }
    for (int i=partnum; --i>=0;) parts[i].move();
    head.move();
    managePath();
  }
  //-----------------------------------------------
  
  private void managePath(){
    if (parts[partnum-1].place == 4) {
      path.remove(0);
      --head.place;
      for (int i=0; i<partnum; ++i) --parts[i].place;
    }
  }
  //------------------------------------------------
  
  void showPath(){
    head.line.show();
    parts[partnum-1].line.show();
  }
  //-------------------------------------------------
  
  boolean goodPoint(PVector pt){
    /*float angle, distance;
    do {
      angle = random(-PI/2, PI/2);
      angle = tangle(path.get(path.size()-1), path.get(path.size()-2)) + (angle<0 ? -PI/4 : PI/2) + angle;
    } while();
    distance = random(width/4, */
    return tangleDiff( path.get(path.size()-1), path.get(path.size()-2), path.get(path.size()-1), pt ) > PI/4 &&
           PVector.dist(path.get(path.size()-1), pt) >= width/4;
  }
  //---------------------------------------------------------------------
  
  void setSpeedRelated (float newSpeed) {
    head.setSpeedRelated(newSpeed);
    for (int i=partnum; --i>=0;) parts[i].setSpeedRelated(newSpeed); 
  }
  //----------------------------------------------------------------------
  
  void setSizeRelated(float newSize) {
    head.setSizeRelated(newSize);
    for (int i=partnum; --i>=0;) parts[i].setSizeRelated(newSize);
  }
}
//////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////

class DragonPart {
  
  PVector prev = new PVector();
  Dragon mr;
  Curve line;
  Timer timer = new Timer();
  float playtime, late;
  PVector pos = new PVector();
  boolean go=false, HEAD = false, TAIL = false;
  color col;
  int place, whichpart;
  
  //=======================================================================
  DragonPart(Dragon master, int i, float late, color c){
    this.mr = master;
    this.late = late;
    this.col = c;
    if (late == 0) HEAD = true;
    TAIL = i==mr.partnum-1;
    playtime = PVector.dist(mr.path.get(0), mr.path.get(1)) / mr.speed;
    line = new Curve(mr.path.get(0), mr.path.get(0), mr.path.get(1), mr.path.get(2));
    place = 2;
    whichpart = i;
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
      //if (mr.path.get(mr.path.size()-1) == mouse && mousePressed && PVector.dist(mr.path.get(mr.path.size()-1), mouse) < 5) return;
      ++place;
      //if (HEAD) mr.path.add(randomCheckedVector());
      
      //if (mr.usedNewGoal == 0 || HEAD) {
      //  mr.path.add(randomCheckedVector());
      //  ++mr.usedNewGoal;
      //}
      //else if (mr.usedNewGoal == mr.partnum-1) {
      //  mr.usedNewGoal = 0;
      //}
      //else ++mr.usedNewGoal;
      
      if (HEAD) {
        if (mousePressed) mr.path.add(mouse.copy());
        else mr.path.add(randomCheckedVector());
      }
      //if (PVector.dist(prev, mouse) >= mouseMinDist){
      //  prev.set(mouse);
      //  mr.path.add(mouse.copy());
      //}
      //println(whichpart, mr.usedNewGoal);
      line.set(mr.path.get(place-3), mr.path.get(place-2), mr.path.get(place-1), mr.path.get(place)); //<>//
      playtime = line.length / mr.speed;
      timer.reset();
    }
    //if (!mr.gotpictures){
      fill(col);
      pos.set(line.getPt(timer.get()/playtime));
      //ellipse(pos.x, pos.y, mr.partWidth, mr.partHeight);
    //}
    //else{
    //  pushMatrix();
    //  runOnUiThread(new Runnable() {

    //      @Override
    //      public void run() {
      
              
    //          translate(pos.x, pos.y);
    //          if (HEAD) {
    //            rotate(tangle(pos, mr.parts[0].pos, PI*0.7));
    //            image(mr.headimg, 0, 0);
    //          }
    //          else if (TAIL) {
    //            rotate(tangle(pos, mr.parts[mr.partnum-2].pos, -PI/2));
    //            image(mr.tailimg, 0, 0);
    //          }
    //          else {
    //            rotate(tangle(pos, mr.parts[whichpart+1].pos, -PI*0.2));
    //            image(mr.bodyimg, 0, 0);
    //          }
              
      
    //      }
    //  });
    //  popMatrix();
      
    //}
    pushMatrix();
    translate(pos.x, pos.y);
    if (HEAD) {
      rotate(tangle(pos, mr.parts[0].pos, PI*0.7));
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
  
  void setSpeedRelated (float newSpeed) {
    //playtime = line.length / mr.speed;
    this.timer.frame = newSpeed;
  }
  //------------------------------------------------------------------
  
  void setSizeRelated (float newSize) {
    //playtime = line.length / mr.speed;
    
  }
}
