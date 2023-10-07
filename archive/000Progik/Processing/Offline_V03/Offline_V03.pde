
int bx, by, board_w, board_h;
int sheight, swidth;
Board board;
Handler handler;
int maxplayers = 4;
float maxalpha = 255;

ArrayList<Button> removeFromExe, addToExe, addToBottomExe;

/////////////////////////////////////////////////////////////////////////////

void setup(){
  //size(1110, 910);
  fullScreen();
  board_w = board_h = height-10;
  bx = by = 5;
  board = new Board(bx, by, board_w, board_h);
  handler = new Handler(board);
}

///////////////////////////////////////////////////////////////////////////

void draw(){
  clear();
  background(0);
  if(handler.basicGameOperationDone) board.update();
  handler.execute_all();
}

////////////////////////////////////////////////////////////////////////////

void mouseReleased(){
  for (Button button: handler.executable)
    if(button.isOver() && button.activated)
      button.pressed = true;
}
