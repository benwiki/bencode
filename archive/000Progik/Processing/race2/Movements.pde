
class MovementHandler{
  ArrayList<Movement> movements = new ArrayList<Movement>();
  
  MovementHandler () {}
  
  Movement add (String type, String name) {
    movements.add(new Movement(type, name));
    return movements.get(movements.size()-1);
  }
  
  void runall () {
    for (Movement m: movements) m.run();
  }
  
  Movement getbyname (String name) {
    for (Movement m: movements)
      if (m.name.equals(name))
        return m;
        
    print("Nem található!!!");
    return movements.get(0);
  }
};

class Movement {
  String type, name;
  float time;
  boolean firstrun = false;
  PVector from = new PVector(),
          to = new PVector();
  Timer timer = new Timer();
  Button master = new Button();
  
  Movement (String type, String name) {
    this.type = type;
    this.name = name;
  }
  
  Movement setDestination(){return this;}
  
  Movement setSize(Button button, PVector resize, float time){
    master = button;
    from.set(button.size);
    to.set(resize);
    this.time = time;
    return this;
  }
  
  void run() {
    if (firstrun) {timer.start(); firstrun=false;}
    
    if (type=="setsize"){
      master.size.set(map(timer.get(), 0,time, from.x,to.x),
                      map(timer.get(), 0,time, from.y,to.y));
    }
  }
};
