class Disk{
  PVector pos = new PVector();
  
  PShape disk_shape;
  float outer = 2.3;
  boolean smallMode=false;
  
  Button place, movable;
  Board board;
  ArrayList<Aim> aims;
  
  //======
  Disk(){}
  //======
  
  Disk(Board board, int x, int y, int col){
    this.board = board;
    pos.set(x, y);
    set_buttons(col);
  }
  //--------------------------------------------------------------------------
  
  void set_buttons(int col){
    //col = which_color(col);
    place = new Button("place", int(board.x+(pos.x+0.5)*board.cs), int(board.y+(pos.y+0.5)*board.cs),
                       board.cs, board.cs, 0,
                       color(0, 0), color(0, 0), 
                       color(100,0,0,100), color(0, 0), 0, "rect");
    place.be_visible();
    place.activate();
    addToExe.add(place);
    movable = new Button("mdisk", int(board.x+(pos.x+0.5)*board.cs), int(board.y+(pos.y+0.5)*board.cs),
                         board.cs, board.cs, 0,
                         col, col, col, col, 0, "disk");
    movable.be_visible();
    movable.activate();
    addToExe.add(movable);
  }
  //--------------------------------------------------------------------------
}
