
class Aim{
  Button start, middle, end;
  PVector boardgoal = new PVector(0, 0);
  Player pmaster;
  Disk dmaster;
  String mode="";
  int breaks_done=0, waytime=100, placewaytime=300, last_counter=0;
  float wayWidth = board.cs/4;
  boolean empty = false, alive=true, directed = false, goBack = false;
  
  ArrayList<PVector> breakpoints = new ArrayList<PVector>();
  //=====
  Aim(){
    empty = true;
  }
  //=====

  Aim(String mode, Player pmaster){
    this.mode = mode;
    this.pmaster = pmaster;
    this.dmaster = emptyDisk;

    //- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if (mode=="placing"){
      start = new Button("aimstart", pmaster.pos.x, pmaster.pos.y, pmaster.pbutton.w, pmaster.pbutton.h, 0,
                         0, color(255,0,0), 0, color(255,0,0), maxalpha/1.2, "circle");
      start.set_size(pmaster.pbutton.w*1.5, pmaster.pbutton.h*1.5, 250);
    }
    else
      start = new Button("aimstart", pmaster.place.pos.x, pmaster.place.pos.y, pmaster.place.w, pmaster.place.h, 0,
                         0, color(255,0,0), 0, color(255,0,0), maxalpha/1.2, "rect");
    start.be_visible();
    start.amaster = this;
    addToBottomExe.add(start);
    //- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if (mode=="placing")
      middle = new Button("aimmid", pmaster.pos.x, pmaster.pos.y, board.cs, board.cs, 0,
                          0, 0, 0, 0, 0, "rect");
    else
      middle = new Button("aimmid", pmaster.place.pos.x, pmaster.place.pos.y, board.cs, board.cs, 0,
                          0, 0, 0, 0, 0, "rect");
    middle.be_visible();
    middle.amaster = this;
    addToBottomExe.add(middle);
    //- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    end = new Button("aimend", pmaster.pos.x, pmaster.pos.y, board.cs, board.cs, 0,
                     0, color(255,0,0), 0, color(255,0,0), 0, "rect");
    end.be_visible();
    end.amaster = this;
    addToBottomExe.add(end);
  }
  //---------------------------------------------------------------------------------------------------------------
  
  Aim(Disk dmaster){
    this.mode = "disk";
    this.dmaster = dmaster;
    this.pmaster = emptyPlayer;

    start = new Button("aimstart", board.boardc_to_c(dmaster.pos).x, board.boardc_to_c(dmaster.pos).y, board.cs, board.cs, 0,
                         0, color(255,0,0), 0, color(255,0,0), maxalpha/1.2, "rect");
    start.be_visible();
    start.amaster = this;
    addToBottomExe.add(start);
    //- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    middle = new Button("aimmid", board.boardc_to_c(dmaster.pos).x, board.boardc_to_c(dmaster.pos).y, board.cs, board.cs, 0,
                          0, 0, 0, 0, 0, "rect");
    middle.be_visible();
    middle.amaster = this;
    addToBottomExe.add(middle);
    //- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    end = new Button("aimend", board.boardc_to_c(dmaster.pos).x, board.boardc_to_c(dmaster.pos).y, board.cs, board.cs, 0,
                     0, color(255,0,0), 0, color(255,0,0), 0, "rect");
    end.be_visible();
    end.amaster = this;
    addToBottomExe.add(end);
  }
  //----------------------------------------------------------------------------------------------------------------
  
  void show(){
    if (empty) return;
    if (alive){
      stroke(255,0,0, maxalpha/2);
      strokeWeight(wayWidth);
      
      if (breakpoints.size()>1){
        line(board.boardc_to_c(breakpoints.get(breaks_done)).x,
             board.boardc_to_c(breakpoints.get(breaks_done)).y,
             middle.pos.x, middle.pos.y);
             
        for (int i=0; i<breaks_done; ++i){
          line(board.boardc_to_c(breakpoints.get(i)).x,
               board.boardc_to_c(breakpoints.get(i)).y,
               board.boardc_to_c(breakpoints.get(i+1)).x,
               board.boardc_to_c(breakpoints.get(i+1)).y);
        }
        
        if (breaks_done < breakpoints.size()-1 &&
            middle.pos.x==board.boardc_to_c(breakpoints.get(breaks_done+1)).x &&
            middle.pos.y==board.boardc_to_c(breakpoints.get(breaks_done+1)).y){
            
            ++breaks_done;
            if (breaks_done == breakpoints.size()-1)
              middle.slide(end.pos.x, end.pos.y, waytime*last_counter, "normal");
            else
              middle.slide(board.boardc_to_c(breakpoints.get(breaks_done+1)).x,
                           board.boardc_to_c(breakpoints.get(breaks_done+1)).y, int(waytime*breakpoints.get(breaks_done+1).z), "normal");
        }
      }
      else if (directed || goBack) line(start.pos.x, start.pos.y, middle.pos.x, middle.pos.y);
    }
  }
  //---------------------------------------------------------------------------------------------------------------
  
  void direct(PVector boardgoal, int last_counter){
    end.pos.set(board.boardc_to_c(boardgoal));
    this.boardgoal.set(boardgoal);
    this.last_counter = last_counter;
    if(mode=="placing"){
      if (directed) middle.slide(end.pos.x, end.pos.y, 0, "whole");
      else middle.slide(end.pos.x, end.pos.y, placewaytime, "whole");
    }
    else if(breakpoints.size()>1)
      middle.slide(board.boardc_to_c(breakpoints.get(1)).x, 
                   board.boardc_to_c(breakpoints.get(1)).y, int(waytime*breakpoints.get(1).z), "normal");
    else
      middle.slide(end.pos.x, end.pos.y, waytime*last_counter, "normal");
    end.alpha = maxalpha/2;
    end.activate();
    directed = true;
    goBack = false;
  }
  //----------------------------------------------------------------------------------------------------------------
  
  void misdirect(){
    end.alpha = 0;
    end.deactivate();
    middle.slide(start.pos.x, start.pos.y, placewaytime, "whole");
    directed = false;
    goBack = true;
  }
  //-----------------------------------------------------------------------------------------------------------------
  
  void kill(){
    if (mode == "placing" && !pmaster.placed){
      if (pmaster.place.empty) start.set_size(pmaster.pbutton.w, pmaster.pbutton.h, 250);
      else                     start.set_size(board.cs, board.cs, 700);
      if (!pmaster.place.empty)start.slide(end.pos.x, end.pos.y, 700, "whole");
      start.suicide_after_sizechange();
    }
    else 
      removeFromExe.add(start);
    removeFromExe.add(middle);
    removeFromExe.add(end);
    alive = false;
  }
  //------------------------------------------------------------------------------------------
  
  void place_master(){
    if (game.place_taken(boardgoal) || (mode=="placing" && !scoreboard.in_graveyard(pmaster) && game.object_around(boardgoal))) return;
    if (!pmaster.empty){
      if (pmaster.placed && !scoreboard.in_graveyard(pmaster)) pmaster.move(this, boardgoal);
      else pmaster.place(end.pos, boardgoal);
    }
    else
      dmaster.move(this, boardgoal);
  }
  //-----------------------------------------------------------------------------------------------------------
}
