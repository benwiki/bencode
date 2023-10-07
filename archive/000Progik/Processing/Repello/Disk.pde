
class Disk{
  
  PVector pos = new PVector();
  float w, h;
  boolean smallMode=false, empty = false;
  
  Button place, movable;
  ArrayList<Aim> aims = new ArrayList<Aim>();
  
  int movetime = 100;
  
  //======
  Disk(){
    empty = true;
  }
  //======
  Disk(float x, float y, float w, float h, color col, int disknum){
    pos.set(x, y);
    this.w = w;
    this.h = h;
    movable = new Button("mdisk", x, y, w, h, 0,
                         col, col, col, col, maxalpha, "disk");
    movable.be_visible();
    movable.activate();
    movable.dmaster = this;
    if (disknum != -1) movable.add_sign("text", str(disknum), new PVector(-board.cs/8, -board.cs/8));
    addToBottomExe.add(movable);
  }
  
  Disk(float x, float y, int col){
    pos.set(x, y);
    set_buttons(col);
  }
  //--------------------------------------------------------------------------
  
  void set_buttons(int col){
    //col = which_color(col);
    place = new Button("dplace", board.boardc_to_c(pos).x, board.boardc_to_c(pos).y,
                       board.cs, board.cs, 0,
                       color(0, 0), color(0, 0), 
                       color(100,0,0,100), color(0, 0), 0, "rect");

    place.be_visible();
    place.activate();
    place.dmaster = this;
    addToBottomExe.add(place);
    movable = new Button("mdisk", board.boardc_to_c(pos).x, board.boardc_to_c(pos).y,
                         board.cs, board.cs, 0,
                         col, col, col, col, maxalpha, "disk");
    movable.be_visible();
    movable.activate();
    movable.dmaster = this;
    //movable.add_sign("text", str(++diskcounter));
    addToBottomExe.add(movable);
  }
  //--------------------------------------------------------------------------
  
  void add_aim(){
    aims.add(new Aim(this));
  }
  //--------------------------------------------------------------------------
  
  void kill_aims(){
    for (Aim aim: aims)
      aim.kill();
    aims.clear();
  }
  //---------------------------------------------------------------------------
  
  void show_aims(){
    for (int i=aims.size()-1; i>=0; --i){
      aims.get(i).show();
      if (!aims.get(i).alive) aims.remove(i);
    }
  }
  //------------------------------------------------------------------------
  
  void direct_last_aim(PVector point, int last_counter){
    aims.get(aims.size()-1).direct(point, last_counter);
  }
  //--------------------------------------------------------------------------
  
  void move(Aim mover, PVector board_place){
    this.pos.set(board_place);
    place.deactivate();
    movable.deactivate();
    for (PVector stop: mover.breakpoints){
      place.slide_backlog.add(new PVector(board.boardc_to_c(stop).x, board.boardc_to_c(stop).y, movetime*stop.z));
      movable.slide_backlog.add(new PVector(board.boardc_to_c(stop).x, board.boardc_to_c(stop).y, movetime*stop.z));
    }
    place.activate_after_slide();
    movable.activate_after_slide();
    place.slide_backlog.add(new PVector(board.boardc_to_c(board_place).x, board.boardc_to_c(board_place).y, 
                                        movetime*mover.last_counter));
    movable.slide_backlog.add(new PVector(board.boardc_to_c(board_place).x, board.boardc_to_c(board_place).y, 
                                          movetime*mover.last_counter));
  }
}
