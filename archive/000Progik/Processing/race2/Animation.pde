class AnimationHandler {
  ArrayList<Animation> animations = new ArrayList<Animation>();
  Button master;
  
  AnimationHandler(){}
  
  Animation add (Button button, String type, String name) {
    animations.add(new Animation());
    return animations.get(animations.size()-1);
  }
}

class Animation () {
  MovementHandler mohand = new MovementHandler();
  
  Animation(Button button, String type){
    
  }
  
  void check (Button button) {
    
  }
  
  void run(){
    
  }
}

