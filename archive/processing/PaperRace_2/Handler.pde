class Handler{
  
  ArrayList<Button> exe = new ArrayList<Button>(); 
  ArrayList<Button> toexe = new ArrayList<Button>();
  ArrayList<Button> kill = new ArrayList<Button>(); 
  
  ////////////
  Handler(){}
  ////////////
  //----------------------------------------------------------
  
  void runall(){
    for (Button t: toexe) exe.add(t); toexe.clear();
    for (Button k: kill)  exe.remove(k); kill.clear();
    for (Button button: exe){
      if (button.visible) button.show();
      if (button.pressed && button.active) command(button);
    }
    /*if (happening) {
      for (Button curbutton: exe) {
        for (Button button: exe) {
           if (curbutton.overlapping(button)) button.hide();
           else if (button.overlapping(curbutton)) { curbutton.hide(); break; }
        }
      }
      happening = false;
    }*/
  }
  //--------------------------------------------------------------------------------------
  void toexe (Button button) { toexe.add(button); }
  void kill (Button button) { kill.add(button); }
  //--------------------------------------------------------------------------------------
  
  void checkPressed(){
    for (Button b: exe)
      if (b.mouseOver) b.press();
  }
  //----------------------------------
  
  void command(Button button){
    button.pressed=false;
    if (button.type.equals("navi")) navi();
  }
  // . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  void navi () {
    toexe( new Button(new PVector(random(0, width), random(0,height)), new PVector(0, 0), "navi")
               .setSize(new PVector(random(width/4, width/3), random(height/4, height/3), 300))
               .setFillColor(color(0))
               .setActiveFillColor(color(random(255), random(255), random(255)))
               .setStrokeWeight(0) );
  }
  // . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
}
