class Handler{
  
  Handler(){}
  
  void runall(){
    for (Button b: toexe) exe.add(b); toexe.clear();
    for (Button button: exe){
      if (button.visible) button.show();
      if (button.active && button.pressed) command(button);
    }
  }
  
  void command(Button button){
    button.pressed=false;
    if (button.type.equals("navi")){
      toexe(new Button(new PVector(random(0, width), random(0,height)), new PVector(200,200),"navi", "add"));
    }
  }
  
  void toexe(Button button){
    toexe.add(button);
  }
}