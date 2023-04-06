class Player{
  int playerWidth;
  PVector pos, board_place; // position on display
  int disks; // number of possessed disks
  boolean alive=true, eliminated=false, deleted=false;
  boolean smallMode=false, placed=false, has_placeaim=false; // smallMode: mikor az egérrel fölémész, lekicsinyül
  boolean empty = false;
  Button pbutton, delete, place;
  int del_s;
  
  ArrayList<Button> setcolor;
  ArrayList<Integer> choosable;
  int[] colors;
  
  Aim placeaim;
  ArrayList<Aim> aims;
  
  int movetime = 800;
  
  //----------------
  Player(){
    empty = true;
  }
  //----------------
  
  Player(int x, int y, int pw, int ph, int[] colors, ArrayList<Integer> choosable){
    this.colors = colors;
    this.choosable = choosable;
    
    pbutton = new Button("player", 0, 0, 
                         pw, ph, 5, color(255), color(0), 
                         color(255), color(100), maxalpha, "oval");
    pbutton.pos.set(x, y);
    pos = pbutton.pos;
    pbutton.pmaster = this;
    pbutton.be_visible();
    pbutton.activate();
    pbutton.add_sign("dot");
    addToExe.add(pbutton);
    
    del_s = pw/3;
    delete = new Button("delete", int(pos.x), int(pos.y-pbutton.w*1.2),
                        del_s, del_s, 3,
                        color(255,150,150), 0, color(255,0,0), 0, maxalpha, "oval");
    delete.add_sign("x");
    delete.sign_acol = color(255,0,0);
    delete.bind_pos(pbutton);
    delete.pmaster = this;
    delete.be_visible();
    delete.activate();
    addToExe.add(delete);
    
    place = new Button();
    
    setcolor = new ArrayList<Button>();
    add_setcolor();
    show_setcolor();
    
    aims = new ArrayList<Aim>();
    placeaim = new Aim();
    
    this.board_place = new PVector(0, 0);
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
                            color(red(col), green(col), blue(col), 120), color(red(col), green(col), blue(col), 120), maxalpha, "oval"));
                                       
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
      sc.hide_after_slide();
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
    if (mode=="placing"){
      has_placeaim = true;
      placeaim = new Aim(mode, this);
      game.kill_other_aims(this);
    }
    else aims.add(new Aim(mode, this));
    
    game.activeAimName = "player";
    game.activePlayer = this;
  }
  //----------------------------------------
  
  void clear_aims(){
    has_placeaim=false;
    placeaim.kill();
    for (Aim aim: aims)
      aim.kill();
    aims.clear();
    game.activeAimName = "none";
  }
  //----------------------------------------
  
  void show_aims(){
    if (placeaim.alive) placeaim.show();
    for (int i=aims.size()-1; i>=0; --i){
      aims.get(i).show();
      if (!aims.get(i).alive) aims.remove(i);
    }
  }
  //------------------------------------------------------
  
  void delete_last_aim(){
    aims.get(aims.size()-1).kill();
    aims.remove(aims.size()-1);
  }
  //----------------------------------------------------
  
  void add_breakpoint_to_last_aim(PVector point){
    aims.get(aims.size()-1).breakpoints.add(new PVector(point.x, point.y));
  }
  //---------------------------------------------------
  
  void direct_last_aim(PVector point){
    aims.get(aims.size()-1).direct(point);
  }
  ////////////////////////////////////////////////////////////////////////////////////
  
  void direct_placeaim(PVector bp){
    placeaim.direct(bp);
  }
  //-----------------------------------------------------
  
  void misdirect_placeaim(){
    placeaim.misdirect();
  }
  //------------------------------------------------------
  
  boolean placeaim_directed(){
    if (placeaim.directed) return true;
    return false;
  }
  //-------------------------------------------------------
  
  boolean moved_placeaim(PVector check){
    if (placeaim.boardgoal.x != check.x || placeaim.boardgoal.y != check.y) return true;
    return false;
  }
  //////////////////////////////////////////////////////////////////////////////////////
  
  void place(PVector dest, PVector board_place){
    this.board_place.set(board_place);
    place = new Button("pplace", pos.x, pos.y, board.cs, board.cs, 0,
                     0, 0, 0, 0, 0, "rect");
    place.slide(dest.x, dest.y, 700, "whole");
    place.activate_after_slide();
    place.be_visible();
    place.pmaster = this;
    addToExe.add(place);
    
    pbutton.deactivate();
    pbutton.activate_after_slide();
    pbutton.slide(dest.x, dest.y, 700, "whole");
    pbutton.set_size(board.cs, board.cs, 700);
    pbutton.afcolor = pbutton.fcolor;
    pbutton.place_after_slide();
  }
  //----------------------------------------------------------------------------------
  
  void move(Aim mover, PVector board_place){
    this.board_place.set(board_place);
    place.deactivate();
    pbutton.deactivate();
    for (PVector stop: mover.breakpoints){
      place.slide_backlog.add(new PVector(board.boardc_to_c(stop).x, board.boardc_to_c(stop).y, movetime/mover.breakpoints.size()));
      pbutton.slide_backlog.add(new PVector(board.boardc_to_c(stop).x, board.boardc_to_c(stop).y, movetime/mover.breakpoints.size()));
    }
    place.activate_after_slide();
    pbutton.activate_after_slide();
    place.slide_backlog.add(new PVector(board.boardc_to_c(board_place).x, board.boardc_to_c(board_place).y, movetime/mover.breakpoints.size()));
    pbutton.slide_backlog.add(new PVector(board.boardc_to_c(board_place).x, board.boardc_to_c(board_place).y, movetime/mover.breakpoints.size()));
  }
}
