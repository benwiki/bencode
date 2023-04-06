class Disk{
  PVector pos = new PVector();
  PShape disk_shape;
  float outer = 2.3;
  boolean smallMode=false, empty = false;
  
  Button place, movable;
  Board board;
  ArrayList<Aim> aims = new ArrayList<Aim>();
  
  int movetime = 800;
  
  //======
  Disk(){
    empty = true;
  }
  //======
  
  Disk(Board board, float x, float y, int col){
    this.board = board;
    pos.set(x, y);
    set_buttons(col);
  }
  //--------------------------------------------------------------------------
  
  void set_buttons(int col){
    //col = which_color(col);
    place = new Button("dplace", board.boardc_to_c(pos, 'x'), board.boardc_to_c(pos, 'y'),
                       board.cs, board.cs, 0,
                       color(0, 0), color(0, 0), 
                       color(100,0,0,100), color(0, 0), 0, "rect");
    place.be_visible();
    place.activate();
    addToExe.add(place);
    movable = new Button("mdisk", bx+(pos.x+0.5)*board.cs, by+(pos.y+0.5)*board.cs,
                         board.cs, board.cs, 0,
                         col, col, col, col, 0, "disk");
    movable.be_visible();
    movable.activate();
    addToExe.add(movable);
  }
  //--------------------------------------------------------------------------
  
  void clear_aims(){
    for (Aim aim: aims)
      aim.kill();
    aims.clear();
    game.activeAimName = "none";
  }
  //---------------------------------------------------------------------------------------------------------
  
  void place(PVector dest, PVector board_place){
    
  }
  //--------------------------------------------------------------------------
  
  void move(Aim mover, PVector board_place){
    this.pos.set(board_place);
    place.deactivate();
    movable.deactivate();
    for (PVector stop: mover.breakpoints){
      place.slide_backlog.add(new PVector(board.boardc_to_c(stop).x, board.boardc_to_c(stop).y, movetime/mover.breakpoints.size()));
      movable.slide_backlog.add(new PVector(board.boardc_to_c(stop).x, board.boardc_to_c(stop).y, movetime/mover.breakpoints.size()));
    }
    place.activate_after_slide();
    movable.activate_after_slide();
    place.slide_backlog.add(new PVector(board.boardc_to_c(board_place).x, board.boardc_to_c(board_place).y, movetime/mover.breakpoints.size()));
    movable.slide_backlog.add(new PVector(board.boardc_to_c(board_place).x, board.boardc_to_c(board_place).y, movetime/mover.breakpoints.size()));
  }
}
