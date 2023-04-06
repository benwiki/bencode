int[][] board;
int[][] object;
String[] raw_board;
int cs; //cell size
int r;
int x_coord, y_coord;
int swidth, sheight;

boolean firstTurn=true;

/* Objects:------
1: Gray korong
2: Silver korong
3: Gold korong
-----------------
11: Player 1
12: Player 2
...
-----------------
-1: Gray korong kicsiben (rajta van a kurzor)
-2: Silver ---"---
-3: Gold ---"---
-----------------
*/

/////////////////////////////////////////////////////////////////////////////

void setup(){
  raw_board = loadStrings("repello_table.txt");
  board = new int [raw_board.length][raw_board.length];
  object = new int [raw_board.length][raw_board.length];
  for (int i=0; i<raw_board.length; ++i)
    for (int j=0; j<raw_board.length; ++j){
      board[i][j]=raw_board[i].charAt(j)-'0';
      object[i][j]=0;
    }
  setBasicObjects();
  
  swidth = 1110;
  sheight = 910;
  size(1110, 910);
  background(0);
  cs = height/raw_board.length;
  r = cs/7;
}

///////////////////////////////////////////////////////////////////////////

void draw(){
  clear();
  setTable();
  checkCursor();
  setObjects();
}

////////////////////////////////////////////////////////////////////////////

void setTable(){
  //---------Table setup------------
  strokeWeight(0);
  fill(#002200);
  rect(3*cs, 3*cs, 7*cs, 7*cs);
  fill(0);
  rect(4*cs, 4*cs, 5*cs, 5*cs);
  
  noFill();
  for (int i=0; i<13; ++i){
    for (int j=0; j<13; ++j){
      stroke(255);
      strokeWeight(1);
      if (i==1 || i==6 || i==11){
        if (j==1 || j==6 || j==11){
          strokeWeight(4);
          if (j==6 && i==6){
            stroke(#FFFF00);
      } } }
      if (!(i==6&&j==7) && !(i==7&&j==6))
        rect(i*cs, j*cs, cs, cs);
  } }
  
  strokeWeight(4);
  stroke(#00FF00);
  rect(3*cs, 3*cs, 7*cs, 7*cs);
  rect(4*cs, 4*cs, 5*cs, 5*cs);
  
  strokeWeight(2);
  
  for(int y=0; y < raw_board.length; ++y){
    for(int x=0; x < raw_board.length; ++x){
      switch (board[y][x]){
        case 1: stroke(#FFFF00); break;
        case 2: stroke(#FF00FF); break;
        case 3: stroke(#0033FF); break;
        case 4: stroke(#880088); break;
        case 5: stroke(#00FF00); break;
        case 6: stroke(#FF0000); break;
      } 
      for (int k=1; k<=board[y][x]; ++k)
        ellipse(cs*(x+0.5), cs*(y+0.5), k*r, k*r);
    }
  }
}

////////////////////////////////////////////////////////////////////////////

void setBasicObjects(){
  object[1][1] = 1;
  object[1][6] = 2;
  object[1][11] = 1;
  object[6][1] = 2;
  object[6][6] = 3;
  object[6][11] = 2;
  object[11][1] = 1;
  object[11][6] = 2;
  object[11][11] = 1;
}

////////////////////////////////////////////////////////////////////////////

void setObjects(){
  for (int i=0; i<13; ++i){
    for (int j=0; j<13; ++j){
      switch(object[i][j]){
        case -1:
        case 1: stroke(#777777); fill(#777777); break;
        case -2:
        case 2: stroke(255); fill(255); break;
        case -3:
        case 3: stroke(#FFFF00); fill(#FFFF00); break;
      }
      if (object[i][j]>0) ellipse(cs*(i+0.5), cs*(j+0.5), cs, cs);
      else if (object[i][j]!=0) ellipse(cs*(i+0.25), cs*(j+0.75), cs/2, cs/2);
    }
  }
}

////////////////////////////////////////////////////////////////////////////

void checkCursor(){
  x_coord = floor(mouseX/cs);
  y_coord = floor(mouseY/cs);
  if (mouseX > 0 && mouseY > 0 && mouseX < sheight && mouseY < sheight && object[x_coord][y_coord] != 0){
    object[x_coord][y_coord] = abs(object[x_coord][y_coord])*-1;
  }
  else 
    for (int i=0; i<13; ++i)
      for (int j=0; j<13; ++j)
        object[i][j] = abs(object[i][j]);
}

////////////////////////////////////////////////////////////////////////////

void turn(int player){
  if (firstTurn){
    firstTurn = false;
    
  }
}
