class Player{
  int playerWidth;
  PVector pos, size; // position on display
  int disks; // number of possessed disks
  boolean alive=true, eliminated=false, deleted=false, smallMode=false, placed=false; // smallMode: mikor az egérrel fölémész, lekicsinyül
  Button pbutton, delete, place;
  
  ArrayList<Button> setcolor;
  ArrayList<Integer> choosable;
  int[] colors;
  
  ArrayList<Aim> aims;
  
  //----------------
  Player(){}
  //----------------
  
  Player(int x, int y, int pw, int ph, int[] colors, ArrayList<Integer> choosable){
    this.colors = colors;
    this.choosable = choosable;
    this.size = new PVector(pw, ph);
    
    pbutton = new Button("player", x, y, 
                         pw, ph, 5, color(255), color(0), 
                         color(255), color(100), maxalpha, "oval");
    //pbutton.pos.set(x, y);
    pos = pbutton.pos;
    pbutton.pmaster = this;
    pbutton.be_visible();
    pbutton.activate();
    pbutton.add_sign("dot");
    addToExe.add(pbutton);
    
    delete = new Button("delete", int(pos.x), int(pos.y-pbutton.w*1.2),
                        pbutton.w/3, pbutton.h/3, 3,
                        color(255,150,150), 0, color(255,0,0), 0, maxalpha, "oval");
    delete.add_sign("x");
    delete.sign_acol = color(255,0,0);
    delete.bind_pos(pbutton);
    delete.pmaster = this;
    delete.be_visible();
    delete.activate();
    addToExe.add(delete);
    
    setcolor = new ArrayList<Button>();
    add_setcolor();
    show_setcolor();
    
    aims = new ArrayList<Aim>();
  }
  //-----------------------------------------------------------------------------
  
  void do_suicide(){
    removeFromExe.add(pbutton);
    removeFromExe.add(delete);
    for (Button sc: setcolor)
      removeFromExe.add(sc);
    setcolor.clear();
  }
  //-------------------------------------------------------------------------------
  
  void suicide_after_slide(){
    eliminated = true;
    hide_setcolor();
    pbutton.slide(pos.x, -height/2, 700, "whole");
    pbutton.deactivate();
    delete.slide(pos.x, -height/2, 350, "whole");
    delete.deactivate();
  }
  //-----------------------------------------------------------------------------------
  
  void add_setcolor(){
    for (int col: choosable) add_fleck(col);
  }
  //-----------------------------------------------------------------------------------

  void update_setcolor(){
    Button to_delete = new Button();
    int to_add=0;
    for (int col: choosable){
      to_add = col;
      for (Button sc: setcolor)
        if (sc.fcolor==col) {to_add = 0; break;}
      if (to_add!=0) break;
    }
    for (Button sc: setcolor)
      if (!choosable.contains(sc.fcolor)){ to_delete = sc; break; }
      
    if (to_add!=color(0) && to_add!=0 && choosable.size() >= setcolor.size()) add_fleck(to_add);
    if (choosable.size() <= setcolor.size()){ 
      removeFromExe.add(to_delete);
      setcolor.remove(to_delete);
    }
    if (setcolor_active()){
      setcolor.get(setcolor.size()-1).be_visible();
      setcolor.get(setcolor.size()-1).activate_after_slide();
      send_flecks_to_place();
    }
  }
  //-----------------------------------------------------------------------------------
  
  void add_fleck(color col){
    setcolor.add(new Button("setcolor", int(pos.x), int(pos.y),
                            pbutton.w/3, pbutton.h/3, 0, 
                            color(col), color(col), 
                            color(col, 120), color(col, 120), maxalpha, "oval"));
                                       
    setcolor.get(setcolor.size()-1).pmaster = this;                                    
    setcolor.get(setcolor.size()-1).bind_pos(pbutton);
    addToExe.add(setcolor.get(setcolor.size()-1));
  }
  //-----------------------------------------------------------------------------------
  
  void send_flecks_to_place(){
    for (Button sc: setcolor)
      sc.slide(pos.x + cos(float(setcolor.indexOf(sc))/setcolor.size()*TWO_PI)*(pbutton.w/2*1.5), 
               pos.y + sin(float(setcolor.indexOf(sc))/setcolor.size()*TWO_PI)*(pbutton.w/2*1.5),
               400, "half");
  }
  //----------------------------------------------------------------------------------
  
  void show_setcolor(){
    for (Button sc: setcolor){
      sc.be_visible();
      sc.activate_after_slide();
      sc.has = false;
    }
    send_flecks_to_place();
  }
  //----------------------------------------------------------------------------------
  
  boolean setcolor_visible(){
    for (Button sc: setcolor)
      if (sc.visible) return true;
    return false;
  }
  //-----------------------------------------
  
  boolean setcolor_active(){
    for (Button sc: setcolor)
      if (sc.activated) return true;
    return false;
  }
  //----------------------------------------------------------------------------------
  
  void hide_setcolor(){
    for (Button sc: setcolor){
      sc.deactivate();
      sc.slide(pos.x, pos.y, 400, "whole");
      sc.has = true;
    }
  }
  //----------------------------------------------------------------------------------
  /*
  int place_in_choosable(color col){
    if (choosable.contains(col)) return choosable.indexOf(col);
    else
      for (...
  }*/
  
  void hide_delete(){
    delete.deactivate();
    delete.hide();
  }
  //----------------------------------------------------------------------------------
  
  void hide_other_stuff(ArrayList<Player> players){
    for (Player player: players)
      if (player.setcolor_visible())
        player.hide_setcolor();
  }
  
  //////////////////////////////////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////////////////////////
  
  void add_aim(String mode){
    aims.add(new Aim(mode, this));
  }
  //----------------------------------------
  
  void clear_aims(){
    for (Aim aim: aims)
      aim.kill();
  }
  //----------------------------------------
  
  void show_aims(){
    for (int i=aims.size()-1; i>=0; --i){
      aims.get(i).show();
      if (!aims.get(i).alive) aims.remove(i);
    }
  }
}
