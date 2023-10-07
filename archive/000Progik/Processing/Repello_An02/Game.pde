
class Game{
  
  ArrayList<Disk> disks;
  ArrayList<Player> players;
  Indicator indicators;
  Handler handler;
  boolean players_placed=false, stepDone=false, get_reward= false, empty = false;
  
  Player activePlayer =  emptyPlayer;
  Player currentPlayer = emptyPlayer;
  
  PVector aim_boardpos;
  ArrayList<Disk> gathered, getfrom;
  
  Button pushout = emptyButton;
  color po_color = color(0, 255, 0);
  
  //===============================
  Game(){
    empty = true;
  }
  //================================
  
  Game(ArrayList<Player> players, ArrayList<Disk> disks, Handler handler){
    this.players = players;
    this.disks = disks;
    this.handler = handler;
    aim_boardpos = new PVector();
    indicators = new Indicator();
  }
  //-----------------------------------------------------------------------------------------------------------------------
  
  void check_cursor(){
    int time = 130;
    for (Player player: players){
      if (!(scoreboard.in_graveyard(player) || buttonsToHide.contains(player.pbutton)) && (handler.gameStarted || player.placed) && !player.pbutton.sliding && player.pbutton.slide_backlog.size()==0){
        if (player.place.isOver()){
          player.pbutton.slide(board.boardc_to_c(player.board_place).x-board.cs/4, 
                               board.boardc_to_c(player.board_place).y+board.cs/4, time, "normal");
          player.pbutton.set_size(board.cs/2, board.cs/2, time);
          player.smallMode = true;
        } else {
            player.pbutton.slide(board.boardc_to_c(player.board_place).x, 
                               board.boardc_to_c(player.board_place).y, time, "normal");
          player.pbutton.set_size(board.cs, board.cs, time);
          player.smallMode = false;
        }
      }
    }
    for (Disk disk: disks){
      if (!disk.movable.sliding && disk.movable.slide_backlog.size()==0){
        if (disk.place.isOver()){
          disk.movable.slide(board.boardc_to_c(disk.pos).x-board.cs/4, 
                             board.boardc_to_c(disk.pos).y+board.cs/4, time, "normal");
          disk.movable.set_size(board.cs/2, board.cs/2, time);
          disk.smallMode = true;
        } else {
          disk.movable.slide(board.boardc_to_c(disk.pos).x, 
                             board.boardc_to_c(disk.pos).y, time, "normal");
          disk.movable.set_size(board.cs, board.cs, time);
          disk.smallMode = false;
        }
      }
    }
    // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    if (mouseX > bx + 3*board.cs && mouseX < bx +10*board.cs && 
        mouseY > by + 3*board.cs && mouseY < by +10*board.cs &&
       (mouseX < bx + 4*board.cs || mouseX > bx + 9*board.cs ||
        mouseY < by + 4*board.cs || mouseY > by + 9*board.cs)){
          
      aim_boardpos.set(floor((mouseX-bx)/board.cs), floor((mouseY-by)/board.cs));
      if (!activePlayer.empty && (!activePlayer.placeaim_directed() || 
                                   activePlayer.placeaim_directed() && activePlayer.moved_placeaim(aim_boardpos)))
        { activePlayer.direct_placeaim(aim_boardpos); }
    }
    else if (!activePlayer.empty && activePlayer.placeaim_directed())
      activePlayer.misdirect_placeaim();
  }
  //-------------------------------------------------------------------------------------------------------------------------------------
  
  void execute_aims(){
    for (Player player: players)
      player.show_aims();
    for (Disk disk: disks)
      disk.show_aims();
  }
  //------------------------------------------------------------------------------------------------------------------------------------
  
  void kill_aims(Button for_who){
    if (!for_who.pmaster.empty) for_who.pmaster.kill_aims();
    else if (!for_who.dmaster.empty) for_who.dmaster.kill_aims();
    else if( !for_who.amaster.empty){
      if (!for_who.amaster.pmaster.empty) for_who.amaster.pmaster.kill_aims();
      else if (!for_who.amaster.dmaster.empty) for_who.amaster.dmaster.kill_aims();
    }
  }
  //-------------------------------------------------------------------------------------------------------------------------------------
  void kill_all_aims(){
    for (Player player: players)
      //if (player!=p && (player.aims.size()>0 || player.has_placeaim)) player.clear_aims(); 
      if (player.aims.size()>0 || player.has_placeaim) player.kill_aims();
    for (Disk disk: disks)
      if (disk.aims.size()>0) disk.kill_aims();
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
  
  boolean object_around(PVector pos){
    if (pos.x==-5 && pos.y==-5) return false;
    int sx=-1, sy=-1, ex=1, ey=1; // starting x, y; ending x, y
    if (pos.x==0) sx = 0;
    else if (pos.x==12) ex = 0;
    if (pos.y==0) sy = 0;
    else if (pos.y==12) ey = 0;
    for (int i=sy; i<=ey; ++i)
      for (int j=sx; j<=ex; ++j)
        if (!(i==0 && j==0) && place_taken(PVector.add(pos, new PVector(j, i))))
          return true;
    return false;          
  }
  //--------------------------------------------------------------------------------------------------------------------------------------
  
  void find_goals(Button who){
    PVector p = who.pmaster.board_place;
    boolean can_move = false;
    
    for (int i = (p.y<1?0:-1); i <= (p.y>11?0:1); ++i)
        for (int j = (p.x<1?0:-1); j <= (p.x>11?0:1); ++j){
        if (!(i==0 && j==0)){
          who.pmaster.add_aim("just add please");
          if (
          explore_route(who, who.pmaster.board_place, new PVector(j, i))
          ) can_move = true;
        }
      }
    
    if (!can_move) {
      if (!who.pmaster.has_placeaim) who.pmaster.add_aim("placing");
      else game.kill_aims(who);
    }
  }
  //---------------------------------------------------------------------------------------------------------------------------------------
  
  boolean explore_route(Button who, PVector start, PVector dir){
    PVector curpos = start.copy();
    int step = board.board[int(start.x+dir.x)][int(start.y+dir.y)], counter=0;
    if (!who.pmaster.empty){
      who.pmaster.add_breakpoint_to_last_aim(start); // IMPORTANT!!!!!!!!!!!!!!
      for (int i=0; i<step; ++i){
        curpos.add(dir);
        if (place_taken(curpos)){
          who.pmaster.delete_last_aim();
          return false;
        }
        ++counter;
        if (curpos.x == 0 || curpos.x == 12) dir.x *= -1;
        if (curpos.y == 0 || curpos.y == 12) dir.y *= -1;
        if (curpos.x == 0 || curpos.x == 12 || curpos.y == 0 || curpos.y == 12){
          who.pmaster.add_breakpoint_to_last_aim(new PVector(curpos.x, curpos.y, counter));
          counter = 0;
        }
      }
      who.pmaster.direct_last_aim(curpos, counter);
    }
    return true;
  }
  //-----------------------------------------------------------------------------------------------------------------------------------------
  
  void find_tensioned_goals(Button who){
    PVector goal = new PVector(), p = new PVector();
    
    if (!who.pmaster.empty || !who.dmaster.empty){
      
      if (!who.pmaster.empty) p.set(who.pmaster.board_place);
      else                    p.set(who.dmaster.pos);
      
      for (int i = (p.y<1?0:-1); i <= (p.y>11?0:1); ++i)
        for (int j = (p.x<1?0:-1); j <= (p.x>11?0:1); ++j){
          
          goal.set(PVector.sub(p, new PVector(j, i)));
          
          if (!(i==0 && j==0) && place_taken(PVector.add(p, new PVector(j, i))) && !place_taken(goal)){
            if (goal.x!=-1 && goal.x!=13 && goal.y!=-1 && goal.y!=13){
              if (!who.pmaster.empty){
                who.pmaster.add_aim("just add");
                who.pmaster.direct_last_aim(goal, 1); // 1: one amount of "movetime" is needed
              } else {
                who.dmaster.add_aim();
                who.dmaster.direct_last_aim(goal, 1); // 1: one amount of "movetime" is needed
              }
            }
            else if (!pushout.activated && currentPlayer != who.pmaster)
              set_pushout_button(who, p,
              ( j==-1 ? (i==1 ? 7 : (i==-1 ? 1 : 0)) : (j==1 ? (i==-1 ? 3 : (i==1 ? 5 : 4)) : (i==-1 ? 2 : (i==1 ? 6 : -1)) ) ) ); // this tells you, in which direction the tension comes from
  } }   } }
  //-----------------------------------------------------------------------------------------------------------------------------------------
  
  boolean has_tensions(){
    PVector p = new PVector();
    
    for (Player player: players){
      p.set(player.board_place);
      for (int i = (p.y<1?0:-1); i <= (p.y>11?0:1); ++i)
        for (int j = (p.x<1?0:-1); j <= (p.x>11?0:1); ++j)
          if (!(i==0 && j==0) && player.placed && place_taken(new PVector(player.board_place.x+j, player.board_place.y+i)))
            return true;
    }
    for (Disk disk: disks){
      p.set(disk.pos);
      for (int i = (p.y<1?0:-1); i <= (p.y>11?0:1); ++i)
        for (int j = (p.x<1?0:-1); j <= (p.x>11?0:1); ++j)
          if (!(i==0 && j==0) && place_taken(new PVector(disk.pos.x+j, disk.pos.y+i)))
            return true;
    }
    return false;
  }
  //------------------------------------------------------------------------------------------------------------------------------------------
  
  void set_scoreboard(){
    scoreboard = new Scoreboard("now it's legit");
  }
  //------------------------------------------------------------------------------------------------------------------------------------------------------
  
  void leave_disk(Player player){
    disks.add(new Disk(player.board_place.x, player.board_place.y, 1)); // 1: gray disk
  }
  //-------------------------------------------------------------------------------------------------------------------------------------------------------
  
  void set_pushout_button(Button button, PVector pos, int dir){
    if (!pushout.pmaster.empty || !pushout.dmaster.empty) removeFromExe.add(pushout);
    PVector real_pos = new PVector(board.boardc_to_c(pos).x+board.cs/4, 
                                   board.boardc_to_c(pos).y-board.cs/4);
    pushout = new Button("pushout", real_pos.x, real_pos.y, board.cs/2, board.cs/2, board.cs/16,
                         po_color, color(0, 0), color(red(po_color), green(po_color), blue(po_color), maxalpha*0.7), color(0, 0), maxalpha, "oval");
    pushout.add_sign("poarrow", dir);
    pushout.be_visible();
    pushout.activate();
    if (!button.pmaster.empty) pushout.pmaster = button.pmaster;
    else pushout.dmaster = button.dmaster;
    addToBottomExe.add(pushout); // IMPORTANT!!!! if pushout isn't at the bottom of executable, the deletion of pushout happens before push_out(), and that causes some trouble.
  }
  //- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  
  void delete_pushout_button(){
    removeFromExe.add(pushout);
    pushout = emptyButton;
  }
  //- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  
  void push_out(){
    Disk disk_to_move;
    if (!pushout.pmaster.empty){
      
      Player to_move = pushout.pmaster;
      // Ki az élők közül...
      to_move.board_place.set(-5, -5);
      removeFromExe.add(to_move.place);
      removeFromExe.add(to_move.pbutton);
      buttonsToHide.add(to_move.pbutton);
      
      // Le a pályáról...
      to_move.pbutton.set_size(board.cs, board.cs, 0);
      to_move.pbutton.slide(to_move.place.pos.x+cos(radians(pushout.arrowDir*45))*board.cs*2,
                            to_move.place.pos.y+sin(radians(pushout.arrowDir*45))*board.cs*2, to_move.movetime, "whole");
      to_move.pbutton.slide_backlog.add( new PVector(width+board.cs, height-board.cs*1.5, 0));
      to_move.pbutton.slide_backlog.add( new PVector(height+(width-height)/(scoreboard.graveyard.size()+2)*(scoreboard.graveyard.size()+1), height-board.cs*1.5, -500) );
      for (Player player: scoreboard.graveyard) {
        player.pbutton.slide_backlog.add( new PVector(player.pbutton.pos.x, player.pbutton.pos.y, to_move.movetime) );
        player.pbutton.slide_backlog.add( new PVector(height+(width-height)/(scoreboard.graveyard.size()+2)*(scoreboard.graveyard.indexOf(player)+1), height-board.cs*1.5, 500) );
      }
      // Levonjuk a sarcot....
      Sign s = scoreboard.get_score(to_move).diskcounter.movable.signs.get(0);
      s.text = str(int(s.text)-1);
      
      // Sarc annak aki letolta
      disk_to_move = new Disk (height+(width-height)/(players.size()+1)*(players.indexOf(currentPlayer)+1.5), height+board.cs, board.cs, board.cs, 1, -1);
      scoreboard.get_score(currentPlayer).add_to_counter(1, 1);
      
      // Meg további egy sarc a megszerzettjei közül
      get_reward = true;
      Button gold_reward = new Button("goldreward", height+(width-height) / (handler.players.size()+1) * 0.5, height/8 * 2 + board.cs*3.5, board.cs*1.3, board.cs*1.3, 0,
                                      color(0), color(255, 0, 0), color(0), color(255, 0, 0), maxalpha, "oval");
      Button silver_reward = new Button("goldreward", height+(width-height) / (handler.players.size()+1) * 0.5, height/8 * 1 + board.cs*3.5, board.cs*1.3, board.cs*1.3, 0,
                                      color(0), color(255, 0, 0), color(0), color(255, 0, 0), maxalpha, "oval");
      Button gray_reward = new Button("goldreward", height+(width-height) / (handler.players.size()+1) * 0.5, height/8 * 0 + board.cs*3.5, board.cs*1.3, board.cs*1.3, 0,
                                      color(0), color(255, 0, 0), color(0), color(255, 0, 0), maxalpha, "oval");
      
      if (scoreboard.get_score(to_move).get_disklist(3).size()>0) {
        addToBottomExe.add(gold_reward);
        gold_reward.be_visible();
        gold_reward.activate();
        indicators.add(gold_reward);
      }
      if (scoreboard.get_score(to_move).get_disklist(2).size()>0) {
        addToBottomExe.add(silver_reward);
        silver_reward.be_visible();
        silver_reward.activate();
        indicators.add(silver_reward);
      }
      if (scoreboard.get_score(to_move).get_disklist(1).size()>0) {
        addToBottomExe.add(gray_reward);
        gray_reward.be_visible();
        gray_reward.activate();
        indicators.add(gray_reward);
      }
    }
    
    else {
      scoreboard.get_score(currentPlayer).add_to_counter(1, 1);
      disk_to_move = pushout.dmaster;
      disk_to_move.movable.pos.set(board.boardc_to_c(disk_to_move.pos).x,
                                   board.boardc_to_c(disk_to_move.pos).y);
      disk_to_move.movable.slide(disk_to_move.place.pos.x+cos(radians(pushout.arrowDir*45))*board.cs*2,
                                 disk_to_move.place.pos.y+sin(radians(pushout.arrowDir*45))*board.cs*2, 500, "whole");
      disks.remove(disk_to_move);
      buttonsToHide.add(disk_to_move.movable);
      removeFromExe.add(disk_to_move.place);
      removeFromExe.add(disk_to_move.movable);
      disk_to_move.movable.set_size(board.cs, board.cs, 0);
      disk_to_move.movable.slide_backlog.add(new PVector(height+(width-height)/(players.size()+1)*(players.indexOf(currentPlayer)+1.5), height+board.cs, 0));
    }
    // Csússzon oda a megszerzett korong!
    disk_to_move.movable.slide_backlog.add(new PVector(height+(width-height)/(players.size()+1)*(players.indexOf(currentPlayer)+1.5), 
                                                       height/8*(disk_to_move.movable.fcolor-1)+board.cs*3.5, -700));
    // Csússzanak arrébb az ott lévők...
    gathered = scoreboard.get_score(currentPlayer).get_disklist(disk_to_move.movable.fcolor);
    int c = gathered.size()-1;
    for (Disk disk: gathered){
      disk.movable.slide( height+(width-height)/(players.size()+1)*(players.indexOf(currentPlayer)+1.5) - board.cs/6 * pow(1.2, c), disk.movable.pos.y, 500, "whole");
      disk.movable.alpha = maxalpha * pow(0.8, c-- +1);
    }
  }
  //-------------------------------------------------------------------------------------------------------------------------------------------
  
  void execute_rewards(){
    //if (gold_reward.visible)
  }
  //-----------------------------------------------------------------------------------------------------------------------------------------------------------
  
  boolean someone_is_sliding(){
    for (Button button: handler.executable)
      if (button.sliding) return true;
    for (Button button: buttonsToHide)
      if (button.sliding) return true;
    return false;
  }
  
  //--------------------------------------------
  
  void execute_indicators(){
    indicators.run();
  }
  
  void addIndicatorTo (Button b){
    indicators.add(b);
  }
  void clearIndicators(){
    indicators.clear();
  }
}
