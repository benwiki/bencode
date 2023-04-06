class Handler{
  ////////////
  Handler(){}
  ////////////
  //----------------------------------------------------------

  void runall(){
    for (Button b: toexe) exe.add(b); toexe.clear();
    for (Button button: exe){
      if (button.visible) button.show();
      if (button.pressed && button.active) command(button);
    }
  }
  //--------------------------------------------------------------------------------------
  void toexe (Button button) { toexe.add(button); }
  //--------------------------------------------------------------------------------------

  void command(Button button){
    button.pressed=false;
    if (button.type.equals("navi")) this.navi(); 
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
