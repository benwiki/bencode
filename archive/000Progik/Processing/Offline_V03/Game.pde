class Game{
  ArrayList<Disk> disks;
  ArrayList<Player> players;
  Handler handler;
  boolean players_placed = false;
  
  Game(ArrayList<Player> players, ArrayList<Disk> disks, Handler handler){
    this.players = players;
    this.disks = disks;
    this.handler = handler;
  }
  //-----------------------------------------------------------------------------------------------------------------------
  
  void check_cursor(){
    int time = 130;
    for (Player player: players){
      if (!player.smallMode && player.pbutton.isOver() && (handler.gameStarted || player.placed)){
        player.pbutton.slide(player.pos.x-board.cs/4, player.pos.y+board.cs/4, time, "normal");
        player.pbutton.set_size(board.cs/2, board.cs/2, time);
        player.smallMode = true;
      }
      else if (player.smallMode && !player.pbutton.isOver()){
        player.pbutton.slide(player.pos.x+board.cs/4, player.pos.y-board.cs/4, time, "normal");
        player.pbutton.set_size(board.cs, board.cs, time);
        player.smallMode = false;
      }
    }
    for (Disk disk: disks){
      if (!disk.smallMode && disk.place.isOver()){
        disk.movable.slide(board.x+(disk.pos.x+0.5)*board.cs-board.cs/4, board.y+(disk.pos.y+0.5)*board.cs+board.cs/4, time, "normal");
        disk.movable.set_size_by_value(board.cs/2, board.cs/2, time);
        disk.smallMode = true;
      }
      else if (disk.smallMode && !disk.place.isOver()){
        disk.movable.slide(board.x+(disk.pos.x+0.5)*board.cs, board.y+(disk.pos.y+0.5)*board.cs, time, "normal");
        disk.movable.set_size_by_value(board.cs, board.cs, time);
        disk.smallMode = false;
      }
    }
    // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    
  }
  //-------------------------------------------------------------------------------------------------------------------------------------
  
  void execute_aims(){
    for (Player player: players)
      if (player.aims.size()>0)
        player.show_aims();
  }
  //-------------------------------------------------------------------------------------------------------------------------------------
  
  boolean players_placed(){
    players_placed = true;
    for (Player player: players) if (!player.placed) players_placed=false;
    return players_placed;
  }
}
