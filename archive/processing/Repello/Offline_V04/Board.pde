class Board{
  int[][] board = 
{{3,4,5,6,1,2,3,4,5,6,1,2,3},
{5,6,1,2,3,4,5,6,1,2,3,4,5},
{1,2,3,4,5,6,3,2,3,4,5,6,1},
{4,5,6,1,2,3,4,5,6,1,2,3,4},
{6,1,2,3,4,5,6,1,2,3,4,5,6},
{2,3,4,5,6,1,2,3,4,5,6,1,2},
{4,5,6,1,2,3,4,5,6,1,2,3,4},
{6,1,2,3,4,5,6,1,2,3,4,5,6},
{2,3,4,5,6,1,2,3,4,5,6,1,2},
{5,6,5,2,3,4,5,6,1,2,3,4,5},
{1,2,3,4,5,6,3,2,3,4,5,6,1},
{3,4,5,6,1,2,1,4,5,6,1,2,3},
{5,6,1,2,3,4,5,6,1,2,3,4,5}};
  int[][] basic_objects = {{1,1,1}, {1,6,2}, {1,11,1}, {6,1,2}, {6,6,3}, {6,11,2}, {11,1,1}, {11,6,2}, {11,11,1}};
  int cs; //cell size
  int r;
  int x, y, w, h;
  int dot = 10;
  
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
    /*raw_board = loadStrings("repello_table.txt");
    board = new int [board.length][raw_board.length];
    for (int i=0; i<board.length; ++i)
      for (int j=0; j<board.length; ++j){
        board[i][j]=board[i].charAt(j)-'0';
      }*/
    cs = w/board.length;
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
    for (int i=0; i<13; ++i){
      for (int j=0; j<13; ++j){
        noFill();
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
        fill(255);
        noStroke();
        if (i==0 && j==0) ellipse(x*2+j*cs, y*2+i*cs, dot, dot);
        else if (i==0) ellipse(x+j*cs, y*2+i*cs, dot, dot);
        else if (j==0) ellipse(x*2+j*cs, y+i*cs, dot, dot);
        else ellipse(x+j*cs, y+i*cs, dot, dot);
      }
      if (i==0) ellipse(x+13*cs, y*2+i*cs, dot, dot);
      else ellipse(x+13*cs, y+i*cs, dot, dot);
    }
    ellipse(x*2, y+13*cs, dot, dot);
    for (int i=1; i<14; ++i)
      ellipse(x+i*cs, y+13*cs, dot, dot);
      
    strokeWeight(7);
    stroke(255);
    noFill();
    rect(x, y, w, h);
    //..........Green starting place's outline.............
    strokeWeight(4);
    stroke(#00FF00);
    rect(x+3*cs, y+3*cs, 7*cs, 7*cs);
    rect(x+4*cs, y+4*cs, 5*cs, 5*cs);
    
    //............Creating circles on places...........
    strokeWeight(2);
    int col=0;
    for(int i=0; i < board.length; ++i){
      for(int j=0; j < board.length; ++j){
        switch (board[i][j]){
          case 1: col=#FFFF00; break;
          case 2: col=#FF00FF; break;
          case 3: col=#0033FF; break;
          case 4: col=#880088; break;
          case 5: col=#00FF00; break;
          case 6: col=#FF0000; break;
        } 
        stroke(col, maxalpha/2);
        for (int k=1; k<=board[i][j]; ++k)
          ellipse(x+cs*(i+0.5), y+cs*(j+0.5), k*r, k*r);
      }
    }
  }
  //---------------------------------------------------------------
  
  float boardc_to_c(PVector c, char xy){
    if(xy=='x')
      return x+(c.x+0.5)*cs;
    else
      return y+(c.y+0.5)*cs;
  }
  
  PVector boardc_to_c(PVector c){
    return new PVector(x+(c.x+0.5)*cs, y+(c.y+0.5)*cs);
  }
}
