
class MovementHandler{
  //==========================================================
  ArrayList<Movement> movements = new ArrayList<Movement>();
  ArrayList<Movement> remove = new ArrayList<Movement>();
  Button master;
  boolean moving = false;
  ////////////////////
  MovementHandler (Button master) { this.master = master; }
  ////////////////////
  //-----------------------------------------------------------------
  
  void run () {
    for (Movement r: remove) movements.remove(r); remove.clear();
    for (Movement m: movements) m.run();
    //if (!happening && moving) happening=true;
  }
  //-----------------------------------------------------------------
  
  Movement getByName (String name) {
    for (Movement m: movements)
      if (m.name.equals(name))
        return m;
        
    print("<", name, "> Movement could not be found in this MovementHandler! Empty Movement is given.");
    return new Movement();
  }
  //--------------------------------------------------------------
  
  Movement add (String type, String name) {
    if (!moving) moving = true;
    movements.add(new Movement(this, type, name));
    return movements.get(movements.size()-1);
  }
  //-----------------------------------
  
  void KILL (Movement m) {
    if (movements.contains(m)) {
      remove.add(m);
      if (movements.size() <= remove.size()) moving=false;
    }
    else println("Could not kill <", m.name, "> movement of type <", m.type, "> because this MovementHandler doesn't contain it."); 
  }
  //-----------------------------------
};

//#######################################################################################################
//#######################################################################################################
//#######################################################################################################

class Movement {
  
  MovementHandler moha;
  String type, name;
  float wholetime=0, pasttime=0;
  boolean firstrun=true, DONE=false, empty=false;
  
  PVector from = new PVector();
  ArrayList<PVector> to = new ArrayList<PVector>();
  int next=0;
  
  Timer timer = new Timer();
  Button master = new Button();
  //////////////////////////////////////////////////////////
  Movement(){empty=true;}
  //////////////////////////////////////////////////////////
  Movement (MovementHandler moha, String type, String name) {
    this.moha = moha;
    this.master = moha.master;
    this.type = type;
    this.name = name;
  }
  ///////////////////////////////////////////////////////////
  //-----------------------------------------------------------------------
  
  Movement setDestination () {
    return this;
  }
  //-----------------------------------------------------------------------
  
  Movement setSize(PVector resize){
    from.set(master.size);
    to.add(resize.copy());
    wholetime += resize.z;
    return this;
  } 
  Movement setSize(PVector resize, float time){
    resize.z = time;
    return setSize(resize);
  }
  //---------------------------------------------------------------------------------------------
  
  void run () {
    if (firstrun) {timer.start(); firstrun=false;}
    else if (timer.get() >= wholetime) {timer.stop(); DONE=true; moha.KILL(this);}
    else if (timer.get() >= pasttime+to.get(next).z) pasttime += to.get(next++).z; 
    // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if      (type=="setsize") this.runSetSize();
    else if (type=="slide")   this.runSlide();
  }
  //.............................................................................................
  
  void runSetSize () {
    if (!DONE) master.size.set(map( timer.get(), 0,to.get(next).z, from.x,to.get(next).x ), // ITT volt egy index error, 1 elem, 1-es index...
                               map( timer.get(), 0,to.get(next).z, from.y,to.get(next).y ));
    else master.size.set(to.get(to.size()-1).x, to.get(to.size()-1).y);
  }
  //.............................................................................................
  void runSlide() {
    
  }
};
