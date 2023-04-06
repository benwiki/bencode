
class MovementHandler{
  //==========================================================
  ArrayList<Movement> movements = new ArrayList<Movement>();
  ArrayList<Movement> remove = new ArrayList<Movement>();
  Button master;
  ////////////////////
  MovementHandler (Button master) { this.master = master; }
  ////////////////////
  //--------------------------------------------------------------

  Movement add (String type, String name) {
    movements.add(new Movement(this, type, name));
    return movements.get(movements.size()-1);
  }
  //-----------------------------------------------------------------

  void run () {
    for (Movement r: remove) movements.remove(r); remove.clear();
    for (Movement m: movements) m.run();
  }
  //-----------------------------------------------------------------

  Movement getByName (String name) {
    for (Movement m: movements)
      if (m.name.equals(name))
        return m;

    print("Nem található!!! Üres Movement-et adok.");
    return new Movement();
  }
  //-----------------------------------

  void KILLME (Movement m) {
    remove.add(m);
  }
  //-----------------------------------
};

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
    else if (timer.get() >= wholetime) {timer.stop(); DONE=true; moha.KILLME(this);}
    else if (timer.get() >= pasttime+to.get(next).z) pasttime += to.get(next++).z;
    // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if (type=="setsize") runSetSize();
  }
  //.............................................................................................

  void runSetSize () {
    if (!DONE) master.size.set(map( timer.get(), 0,to.get(next).z, from.x,to.get(next).x ),
                               map( timer.get(), 0,to.get(next).z, from.y,to.get(next).y ));
    else master.size.set(to.get(to.size()-1).x, to.get(to.size()-1).y);
  }
};
