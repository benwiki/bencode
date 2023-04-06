int[][] board;
String[] raw_board;
int cs; //cell size
int r;
/////////////////////////////////////////////////////////////////////////////

void setup(){
   raw_board = loadStrings("repello_table.txt");
   //println(raw_board[0]);
   board = new int [raw_board.length] [raw_board.length];
   for (int i=0; i<raw_board.length; ++i){
     for (int j=0; j<raw_board.length; ++j){
       board[i][j] =raw_board[i].charAt(j)-'0';
       print(board[i][j]);
     }
     println("");
  }
   
   size(910, 910);
   background(0);
   cs = width/raw_board.length;
   r = cs/6;
}

///////////////////////////////////////////////////////////////////////////

void draw(){
  for(int y=0; y < raw_board.length; ++y){
    for(int x=0; x < raw_board.length; ++x){
      switch (board[y][x]){
        case 1:
          stroke(#FFFF00);
          break;
        case 2:
          stroke(#FF00FF);
          break;
        case 3:
          stroke(#0033FF);
          break;
        case 4:
          stroke(#880088);
          break;
        case 5:
          stroke(#00FF00);
          break;
        case 6:
          stroke(#FF0000);
          break;
      }
      noFill();
      //rect(cs*x, cs*y, cs*(x+1),cs*(y+1)); 
      for (int k=1; k<=board[y][x]; ++k)
        ellipse(cs*(x+0.5), cs*(y+0.5), k*r, k*r);
    }
  }
  
  stroke(255);
  rect(3*cs,3*cs,7*cs,7*cs);
  rect(4*cs,4*cs,5*cs,5*cs);
}

////////////////////////////////////////////////////////////////////////////

void turn(int player){
  
  
  
}
