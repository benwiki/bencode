class Board{
  int[][] board;
  int[][] basic_objects = {{1,1,1}, {1,6,2}, {1,11,1}, {6,1,2}, {6,6,3}, {6,11,2}, {11,1,1}, {11,6,2}, {11,11,1}};
  String[] raw_board;
  int cs; //cell size
  int r;
  int x, y, w, h;
  
  /* Objects:------
  1: Gray korong
  2: Silver korong
  3: Gold korong
  ...
  -----------------
  -1: Gray korong kicsiben (rajta van a kurzor)
  -2: Silver ---"---
  -3: Gold ---"---
  -----------------
  */
  
  Board(int x, int y, int w, int h){
    raw_board = loadStrings("repello_table.txt");
    board = new int [raw_board.length][raw_board.length];
    for (int i=0; i<raw_board.length; ++i)
      for (int j=0; j<raw_board.length; ++j){
        board[i][j]=raw_board[i].charAt(j)-'0';
      }
    cs = board_w/raw_board.length;
    r = cs/7;
    this.x = x;
    this.y = y;
    this.w = w;
    this.h = h;
  }
  
  //----------------------------------------------------
  
  void update(){
    setBoard();
  }
  //------------------------------------------------------------
  
  void setBoard(){
    //.........Green starting place's inside...........
    rectMode(CORNER);
    strokeWeight(0);
    fill(#002200);
    rect(x+3*cs, y+3*cs, 7*cs, 7*cs);
    fill(0);
    rect(x+4*cs, y+4*cs, 5*cs, 5*cs);
    
    //.............The grid..............
    noFill();
    for (int i=0; i<13; ++i){
      for (int j=0; j<13; ++j){
        stroke(255);
        strokeWeight(1);
        if (i==1 || i==6 || i==11)
          if (j==1 || j==6 || j==11){
            strokeWeight(4);
            if (j==6 && i==6)
              stroke(#FFFF00);
          }
        if (!(i==6&&j==7) && !(i==7&&j==6))
          rect(x+i*cs, y+j*cs, cs, cs);
      }
    }
    strokeWeight(7);
    stroke(255);
    rect(x, y, w, h);
    //..........Green starting place's outline.............
    strokeWeight(4);
    stroke(#00FF00);
    rect(x+3*cs, y+3*cs, 7*cs, 7*cs);
    rect(x+4*cs, y+4*cs, 5*cs, 5*cs);
    
    //............Creating circles on places...........
    strokeWeight(2);
    for(int i=0; i < raw_board.length; ++i){
      for(int j=0; j < raw_board.length; ++j){
        switch (board[i][j]){
          case 1: stroke(#FFFF00); break;
          case 2: stroke(#FF00FF); break;
          case 3: stroke(#0033FF); break;
          case 4: stroke(#880088); break;
          case 5: stroke(#00FF00); break;
          case 6: stroke(#FF0000); break;
        } 
        for (int k=1; k<=board[i][j]; ++k)
          ellipse(x+cs*(i+0.5), y+cs*(j+0.5), k*r, k*r);
      }
    }
  }
  //---------------------------------------------------------------
}
