
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
  float cs; //cell size
  float r, b;
  float x=1, y=1, w, h, d;
  float border;
  int dot;
  
  Board(int d){
    border = d;
  }
  
  //------------------------------------------------------------
  
  void update(){
    w = height-3;
    h = height-3;
    cs = this.w/board.length;
    r = cs/10;
    b = cs/5;
    dot = (int)cs/7;
    //.........Green starting place's inside...........
    rectMode(CORNER);
    strokeWeight(0);
    fill(#002200);
    rect(x+3*cs, y+3*cs, 7*cs, 7*cs);
    fill(0);
    rect(x+4*cs, y+4*cs, 5*cs, 5*cs);
    
    //textSize(cs/5);
    textFont(font, cs/5);
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
        
        color col=0;
        switch (board[i][j]){
          case 1: col=#FFFF00; break;
          case 2: col=#FF00FF; break;
          case 3: col=#0033FF; break;
          case 4: col=#880088; break;
          case 5: col=#00FF00; break;
          case 6: col=#FF0000; break;
        } 
        fill(col, maxalpha/2);
        
        text(str(board[i][j]), x+(i+0.5)*cs, y+(j+0.5)*cs-1);
        
        fill(255);
        noStroke();
        if (i>0 && j>0) ellipse(x+j*cs, y+i*cs, dot, dot);
      }
    }
    //strokeWeight(border);
    //stroke(255);
    noFill();
    //rect(x-d, y-d, w-d/2-1, h-d/2-1);
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
          ellipse(x+cs*(i+0.5), y+cs*(j+0.5), b+k*r, b+k*r);
      }
    }
    
    ////////////////////////////////////////////////////////////
    for (int i=buttonsToHide.size()-1; i>=0; --i){
      if (buttonsToHide.get(i).visible) buttonsToHide.get(i).show();
      if (!buttonsToHide.get(i).sliding) {
        if (!buttonsToHide.get(i).pmaster.empty) {
          scoreboard.graveyard.add(buttonsToHide.get(i).pmaster);
          addToExe.add(buttonsToHide.get(i));
        }
        else if (!buttonsToHide.get(i).dmaster.empty) scoreboard.get_score(game.currentPlayer).get_disklist(buttonsToHide.get(i).dmaster.movable.fcolor).add(buttonsToHide.get(i).dmaster);
        else println("ERROR!!! sth is not right in buttonsToHide...");
        addToExe.add(buttonsToHide.get(i));
        buttonsToHide.get(i).show();
        buttonsToHide.remove(i);        
      }
    }
    ////////////////////////////////////////////////////////////
    
    noStroke();
    fill(0);
    rectMode(CORNERS);
    rect(x+w+border, 0, width, height);
    
    pushMatrix();
    textSize(cs/2);
    fill(255);
    if (handler.gameStarted) text("GRAVEYARD", width-(width-height)/2, height/2+cs*3.5);
    else if (handler.gameEnded) {
      textSize(cs);
      fill(50);
      text("THE END", width-(width-height)/2-textAscent()/20, height/2+cs*3.5-textAscent()/20);
      fill(255);
      text("THE END", width-(width-height)/2, height/2+cs*3.5);
    }
    
    popMatrix();
  }
  //---------------------------------------------------------------
  
  PVector boardc_to_c(PVector c){
    return new PVector(x+(c.x+0.5)*cs, y+(c.y+0.5)*cs);
  }
  
  PVector c_to_boardc(PVector c){
    return new PVector(int((c.x-x)/cs), int((c.y-y)/cs));
  }
}
