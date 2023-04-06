class Game{
  ArrayList<Disk> disks;
  ArrayList<Player> players;
  Handler handler;
  boolean players_placed = false;
  
  String activeAimName = "none";
  Player activePlayer;
  Disk activeDisk;
  
  PVector aim_boardpos;
  
  Game(ArrayList<Player> players, ArrayList<Disk> disks, Handler handler){
    this.players = players;
    this.disks = disks;
    this.handler = handler;
    aim_boardpos = new PVector();
  }
  //-----------------------------------------------------------------------------------------------------------------------
  
  void check_cursor(){
    int time = 130;
    for (Player player: players){
      if ((handler.gameStarted || player.placed) && !player.pbutton.sliding && player.pbutton.slide_backlog.size()==0){
        if (!player.smallMode && player.place.isOver()){
          player.pbutton.slide(board.boardc_to_c(player.board_place, 'x')-board.cs/4, 
                               board.boardc_to_c(player.board_place, 'y')+board.cs/4, time, "normal");
          player.pbutton.set_size(board.cs/2, board.cs/2, time);
          player.smallMode = true;
        }
        else if (player.smallMode && !player.place.isOver()){
          player.pbutton.slide(board.boardc_to_c(player.board_place, 'x'), 
                               board.boardc_to_c(player.board_place, 'y'), time, "normal");
          player.pbutton.set_size(board.cs, board.cs, time);
          player.smallMode = false;
        }
      }
    }
    for (Disk disk: disks){
      if (!disk.movable.sliding && disk.movable.slide_backlog.size()==0){
        if (!disk.smallMode && disk.place.isOver()){
          disk.movable.slide(board.boardc_to_c(disk.pos, 'x')-board.cs/4, 
                             board.boardc_to_c(disk.pos, 'y')+board.cs/4, time, "normal");
          disk.movable.set_size(board.cs/2, board.cs/2, time);
          disk.smallMode = true;
        }
        else if (disk.smallMode && !disk.place.isOver()){
          disk.movable.slide(board.boardc_to_c(disk.pos, 'x'), 
                             board.boardc_to_c(disk.pos, 'y'), time, "normal");
          disk.movable.set_size(board.cs, board.cs, time);
          disk.smallMode = false;
        }
      }
    }
    // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    if (mouseX>bx+3*board.cs && mouseX<bx+10*board.cs && 
        mouseY>by+3*board.cs && mouseY<by+10*board.cs &&
        (mouseX<bx+4*board.cs || mouseX>bx+9*board.cs ||
        mouseY<by+4*board.cs || mouseY>by+9*board.cs)){
          
      aim_boardpos.set(floor((mouseX-bx)/board.cs), floor((mouseY-by)/board.cs));
      if (activeAimName == "player" && (!activePlayer.placeaim_directed() || (activePlayer.placeaim_directed() && activePlayer.moved_placeaim(aim_boardpos))))
        activePlayer.direct_placeaim(aim_boardpos);
    }
    else 
      if (activeAimName == "player" && activePlayer.placeaim_directed())
        activePlayer.misdirect_placeaim();
  }
  //-------------------------------------------------------------------------------------------------------------------------------------
  
  void execute_aims(){
    for (Player player: players)
      player.show_aims();
  }
  //------------------------------------------------------------------------------------------------------------------------------------
  
  void kill_other_aims(Player p){
    for (Player player: players)
      if (player!=p && (player.aims.size()>0 || player.has_placeaim)) player.clear_aims(); 
  }
  //-------------------------------------------------------------------------------------------------------------------------------------
  
  boolean players_placed(){
    players_placed = true;
    for (Player player: players) if (!player.placed) players_placed=false;
    return players_placed;
  }
  //--------------------------------------------------------------------------------------------------------------------------------------
  
  boolean place_taken(PVector pt){
    for (Player player: players)
      if (pt.x == player.board_place.x && pt.y == player.board_place.y) return true;
    for (Disk disk: disks)
      if (pt.x == disk.pos.x && pt.y == disk.pos.y) return true;
    return false;
  }
  //--------------------------------------------------------------------------------------------------------------------------------------
  
  void find_goals(Button who){
    if (!who.pmaster.empty){
      int sx=-1, sy=-1, ex=1, ey=1; // starting x, y; ending x, y
      if (who.pmaster.board_place.x==0) sx = 0;
      else if (who.pmaster.board_place.x==12) ex = 0;
      if (who.pmaster.board_place.y==0) sy = 0;
      else if (who.pmaster.board_place.y==12) ey = 0;
      
      for (int i=sy; i<=ey; ++i)
        for (int j=sx; j<=ex; ++j){
          if (!(i==0 && j==0)){
            who.pmaster.add_aim("just add please");
            explore_route(who, who.pmaster.board_place, new PVector(j, i));
          }
        }
    }
  }
  //---------------------------------------------------------------------------------------------------------------------------------------
  
  void explore_route(Button who, PVector start, PVector dir){
    PVector curpos = new PVector();
    curpos.set(start);
    int step = board.board[int(start.x+dir.x)][int(start.y+dir.y)];
    if (!who.pmaster.empty){
      who.pmaster.add_breakpoint_to_last_aim(start); // IMPORTANT!!!!!!!!!!!!!!
      for (int i=0; i<step; ++i){
        curpos.add(dir);
        if (place_taken(curpos)){
          who.pmaster.delete_last_aim();
          return;
        }
        if (curpos.x == 0 || curpos.x == 12) dir.x *= -1;
        if (curpos.y == 0 || curpos.y == 12) dir.y *= -1;
        if (curpos.x == 0 || curpos.x == 12 || curpos.y == 0 || curpos.y == 12) who.pmaster.add_breakpoint_to_last_aim(curpos);
      }
      who.pmaster.direct_last_aim(curpos);
    }
  }
}
