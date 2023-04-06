
class AnimationHandler {
  AnimationHandler () {
    
  }
  
  void run(){
  
  }
};

class Animation {
  String type;
  PVector pos = new PVector(), size = new PVector();
  MovementHandler moha;
  
  Animation(String type, PVector pos, PVector size){
    this.pos.set(pos);
    this.size.set(size);
    moha = new MovementHandler(pos, size);
    this.type=type;
    check(type);
  }
  
  void check (String type) {
    if (type == "popup") popup();
  }
  
  void popup(){
    moha.add("setsize", "popset-1").setSize(PVector.mult(size,2));
  }
};
