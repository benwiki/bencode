
class AnimationHandler {
  AnimationHandler () {
    
  }
  
  void run(){
  
  }
};

class Animation {
  Button master;
  String type;
  MovementHandler moha;
  
  Animation(Button button, String type){
    this.master=button;
    moha = new MovementHandler(this.master);
    this.type=type;
    check(type);
  }
  
  void check (String type) {
    if (type == "popup") popup();
  }
  
  void popup(){
    moha.add("setsize", "popset-1").setSize(PVector.mult(master.size, 2));
  }
};
