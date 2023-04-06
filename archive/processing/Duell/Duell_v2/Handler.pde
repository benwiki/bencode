
class Handler {
  ArrayList<Button> exe = new ArrayList<Button>(),
                  toexe = new ArrayList<Button>(), 
                  rmexe = new ArrayList<Button>();
  ////////////
  Handler(){}
  ////////////
  //----------------------------------------------------------
  
  void runall(){
    for (Button t: toexe) exe.add(t); toexe.clear();
    for (Button r: rmexe) exe.remove(r); rmexe.clear();
    for (Button button: exe){
      if (button.visible) button.show();
      if (button.pressed && button.active) command(button);
    } 
  }
  //--------------------------------------------------------------------------------------
  void toexe (Button button) { toexe.add(button); }
  void remove (Button button) { rmexe.add(button); }
  //--------------------------------------------------------------------------------------
  
  void command(Button button){
    button.pressed=false;
    if (button.type.equals("navi")) navi();
  }
  // . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  void navi () {
    println(exe.size());
    toexe( new Button(new PVector(random(0, width), random(0,height)), new PVector(0, 0), "navi")
               .setSize(new PVector(random(100, 200), random(100, 200), 300))
               .setFillColor(color(0))
               .setActiveFillColor(color(random(255), random(255), random(255)))
               .setStrokeWeight(0) );
  }
  // . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
}
