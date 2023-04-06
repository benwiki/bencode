
class Movements{
  
  ArrayList all, to_delete;
  boolean moving = false;
  
  //----------------------------
  
  Movements(){
    all = new ArrayList();
    to_delete = new ArrayList();
  }
  //--------------------------------------
  
  Slide newSlide (Button master) {
    Slide s = new Slide(master, this);
    all.add(s);
    moving = true;
    return s;
  }
  //--------------------------------------------------------------
  
  void run(){
    if (!moving) return;
    
    for (Object d: to_delete) all.remove(d);
    for (Object m: all){
       if      (m instanceof Slide)      ((Slide)m).run();
       else if (m instanceof Rotation)   ((Rotation)m).run();
       else if (m instanceof SizeChange) ((SizeChange)m).run();
    }
    if (all.size()==0) moving = false;
  }
  //----------------------------------------------------------------
  
  void delete (Object m) {
    to_delete.add(m);
  }
  //----------------------------------------------------------------
  
  boolean isMoving () {
    if (all.size()>0) return true;
    else return false;
  }
  //---------------------------------------------------------------
};

//####################################################################################################
//####################################################################################################

class Slide {
  
  /* Usage example *\
  Button my_button = new Button("somebutton", 100, 100, 50, 50);
  Slide my_slide = my_button.slide().setTime(1500)          // given in milliseconds
                                    .setMode("accelerate"); // possible modes: normal, whole (accelerate, then decelerate), accelerate, decelerate
  for (int i=0; i<5; ++i) my_slide.addDestination(random(0, width), random(0, height));
  my_slide.setStyle("separated");
  
  -- inside draw() --
  my_button.show(); //Slide automatically starts
  */
  
  Button mr; //MASTER!!!
  Movements mmr; // Movements master
  
  PVector fix_pos, cur_dest, shift, acc, vel;
  
  ArrayList<PVector> destinations = new ArrayList<PVector>(); // destinations - the z component is the time amount
  FloatList distances = new FloatList(),
            durations = new FloatList();
  String mode="normal", style="united"; // modes: normal, whole, accelerate, decelerate // styles: united, separated
  int destsReached=0;
  long time=0, curtime;
  float fullDistance=0;
  boolean fixTime = false, setup_done = false;
  Timer timer = new Timer();
  
  Slide (Button master, Movements mov_master) {
    this.mr = master;
    this.mmr = mov_master;
    this.mode = mode.toLowerCase();
    cur_dest=master.pos.copy();
    fix_pos = new PVector(0, 0);
    shift   = new PVector(0, 0);
    acc     = new PVector(0, 0);
    vel     = new PVector(0, 0);
  }
  //==============================================================================
  
  Slide setMode  (String mode)  { this.mode = mode;   return this; }
  Slide setStyle (String style) { this.style = style; return this; }
  Slide setTime (int time) {
    this.time = time;
    fixTime = true; 
    return this;
  }
  
  //============================================================================================
  
  Slide addDestination (PVector add_dest) {
    return _addDestination(add_dest);
  }
  
  Slide addDestination (float x, float y) {
    return _addDestination(new PVector(x, y));
  }
  
  Slide _addDestination (PVector add_dest) {
    /////////////////////////////////////
    if (destinations.size()==0 ? 
          mr.pos.equals(add_dest) : 
          destinations.get(destinations.size()-1).equals(add_dest))
      return this;
    /////////////////////////////////////
    fix_pos = mr.pos.copy();
    destinations.add(add_dest.copy());
    
    durations.append(add_dest.z); // ...the z component is the time amount.
    for (PVector d: destinations) d.z = 0;
    
    if (destinations.size()==1){
      cur_dest.set(add_dest.x, add_dest.y);
      shift.set(PVector.sub(cur_dest, mr.pos));
    }
    
    if (destinations.size()==1) distances.append(cur_dest.dist(mr.pos) );
    else distances.append( PVector.dist(destinations.get(destinations.size()-1), 
                                     destinations.get(destinations.size()-2)) );
    return this;
  }
  
  //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  
  void run() {
    for (PVector d: destinations) ellipse(d.x, d.y, 10, 10);
    if (!setup_done) slideSetup();
    
    curtime = timer.state();
    
    if (destinations.size() > 0 && curtime < time){
      println(destinations.size()>1, curtime, destsReached, sumListUntil(durations, destsReached));
      if (destinations.size()>1 && (style == "united" ? curtime >= durations.get(destsReached) : curtime >= sumListUntil(durations, destsReached)) ) {
        
        fix_pos.set(destinations.get(0));
        mr.pos.set(fix_pos);
        cur_dest.set(destinations.get(1));
        shift.set(PVector.sub(cur_dest, fix_pos));
        
        ///////////////////////
        destinations.remove(0);
        ++destsReached;
        ///////////////////////
        
        if (style == "united") {
          if (mode=="accelerate" || mode=="decelerate") {
            acc.set( cos(shift.heading())*(fullDistance)*2/pow(time, 2), sin(shift.heading())*(fullDistance)*2/pow(time, 2));
            vel.set( PVector.mult(acc, time) );
          }
          else if (mode=="whole") {
            acc.set( cos(shift.heading())*(fullDistance/2)*2/pow(time/2, 2), sin(shift.heading())*(fullDistance/2)*2/pow(time/2, 2)); 
            vel.set( PVector.mult(acc, time/2) );
          }
          else if (mode=="normal")
            vel.set( cos(shift.heading())*fullDistance/time, sin(shift.heading())*fullDistance/time );
          
        }
        else if (style == "separated") {
          if (mode=="accelerate" || mode=="decelerate") {
            acc.set( PVector.mult(shift, 2/pow(durations.get(destsReached), 2)));
            vel.set( PVector.mult(acc, durations.get(destsReached)) );
          }
          else if (mode=="whole") {
            acc.set( PVector.div(shift, pow(durations.get(destsReached)/2, 2))); // azért csak a time^2-vel osztom el, mert fele utat teszi meg, így nem kell külön elosztanom és beszoroznom 2-vel 
            vel.set( PVector.mult(acc, durations.get(destsReached)/2) );
          }
          else if (mode=="normal")
            vel.set( PVector.div(shift, durations.get(destsReached)) );
        }
        println(time);
      }
      
      PVector fix_modified = (style == "separated" || destsReached == 0 ? fix_pos : PVector.sub(fix_pos, new PVector(cos(shift.heading())*distances.get(destsReached-1), sin(shift.heading())*distances.get(destsReached-1))));
      long modified_curtime = (long)(curtime - (style == "separated" && destsReached != 0 ? durations.get(destsReached-1) : 0));
      long modified_time = (long)(style == "separated" ? durations.get(destsReached) : time);
      
      if (mode=="accelerate") mr.pos.set( PVector.add(fix_modified, PVector.mult(acc, pow(modified_curtime,2) / 2 )) );
      if (mode=="decelerate") mr.pos.set( PVector.add(fix_modified, PVector.sub(PVector.mult(vel, modified_curtime), PVector.mult(acc, pow(modified_curtime,2) / 2 ))) );
      if (mode=="whole") {
        if (curtime < time/2) mr.pos.set( PVector.add(fix_modified, PVector.mult(acc, pow(modified_curtime, 2) / 2 )) );
        else {
          float to_mult_with = (style == "separated" ? 
                                  destsReached == 0 ? 
                                    distances.get(0)/2 : 
                                    valueFromSum(distances, destsReached-1)/2 : 
                                  destsReached == 0 ? 
                                    fullDistance/2 : 
                                    fullDistance/2 - distances.get(destsReached-1));
          mr.pos.set( PVector.add(PVector.add(fix_pos, new PVector(cos(shift.heading())*to_mult_with, 
                                                                   sin(shift.heading())*to_mult_with)), 
                                  PVector.sub(PVector.mult(vel, modified_curtime - modified_time/2), PVector.mult(acc, pow(modified_curtime - modified_time/2, 2) / 2 ))) );
        }
      }
      if (mode=="normal") mr.pos.set( PVector.add(fix_modified, PVector.mult(vel, modified_curtime)) );
    }
    else {
      mr.pos.set(cur_dest);
      timer.reset();
      mmr.delete(this);
    }
  }
  //--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  
  void slideSetup() {

    fullDistance = sumList(distances);
    for (int i=distances.size()-1; i>=0; --i)
      distances.set(i, sumListUntil(distances, i));
    
    if (!fixTime) time = int(sumList(durations));
    //..................................................................
    if (style == "united") {
      
      if (mode=="accelerate") {
        acc.set( cos(shift.heading())*(fullDistance)*2/pow(time, 2), 
                 sin(shift.heading())*(fullDistance)*2/pow(time, 2));
        vel.set( PVector.mult(acc, time) );
        for (int i=0; i<destinations.size(); ++i)
          durations.set(i, sqrt(2*distances.get(i)/acc.mag()));
      }
      else if (mode=="decelerate") {
        acc.set( cos(shift.heading())*(fullDistance)*2/pow(time, 2), 
                 sin(shift.heading())*(fullDistance)*2/pow(time, 2));
        vel.set( PVector.mult(acc, time) );
        for (int i=0; i<destinations.size(); ++i)
          durations.set(i, (vel.mag() - sqrt(pow(vel.mag(), 2) - 2*distances.get(i)*acc.mag())) / acc.mag());
      }
      else if (mode=="whole") {
        acc.set( cos(shift.heading())*(fullDistance/2)*2/pow(time/2, 2), 
                 sin(shift.heading())*(fullDistance/2)*2/pow(time/2, 2) ); 
        vel.set( PVector.mult(acc, time/2) );
        for (int i=0; i<destinations.size(); ++i) {
          if (i == destinations.size()-1)
            durations.set(i, time);
          else if (distances.get(i) <= fullDistance/2)
            durations.set(i, sqrt(2*distances.get(i)/acc.mag()));
          else
            durations.set(i, time/2 + (vel.mag() - sqrt(pow(vel.mag(), 2) - 2*(distances.get(i)-fullDistance/2)*acc.mag())) / acc.mag());
        }
      }
      else if (mode=="normal") {
        vel.set( cos(shift.heading())*fullDistance/time, 
                 sin(shift.heading())*fullDistance/time );
        for (int i=0; i<destinations.size(); ++i)
          durations.set(i, distances.get(i) / vel.mag());
      }
    }
    //..............................................................................................
    else if (style == "separated") {
      /*for (int i=durations.size()-1; i>=0; --i)
        changeValue(durations, i, sumListUntil(durations, i));*/
      
      if (mode=="accelerate" || mode=="decelerate") {
        acc.set( PVector.mult(shift, 2/pow(durations.get(0), 2)) );
        vel.set( PVector.mult(acc, durations.get(0)) );
      }
      else if (mode=="whole") {
        acc.set( PVector.div(shift, pow(durations.get(0)/2, 2)) ); // azért csak a time^2-vel osztom el, mert fele utat teszi meg, így nem kell külön elosztanom és beszoroznom 2-vel 
        vel.set( PVector.mult(acc, durations.get(0)/2) );
      }
      else if (mode=="normal") {
        vel.set( PVector.div(shift, durations.get(0)) );
      }
    }
    
    timer.start();
    setup_done = true;
  }
};

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class Rotation {
  int time, amount=360;
  Rotation(){}
  
  void run() {
    
  }
};

//--------------------------------------------------------------------

class SizeChange {
  int time;
  SizeChange(){}
  
  void run() {
    
  }
};
