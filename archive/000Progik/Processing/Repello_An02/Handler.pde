
class Handler{
  
  ArrayList<Button> executable;
  ArrayList<Player> players;
  ArrayList<Disk> disks;
  ArrayList<Integer> ecolors = new ArrayList<Integer>();
  Player eliminatePlayer = emptyPlayer;

  int aP_w, aP_h, aP_x, aP_y;
  int sB_w, sB_h, sB_in_x;
  int pw, ph, player_y;
  float distanceOfPlayers;
  Button addPlayer;
  Button startbutton;
  
  boolean gameWillStart = false, gameStarted = false, basicGameOperationDone=false, clearExecutable=false;
  boolean startbutton_inside=false, startbutton_added=false, startable=false;
  
  ArrayList<Integer> choosable;//
  //int[] colors=         {#7d6468,#777777,#646d7d,#7d7c57,#9c0525,#ff1808,#ff7f0f, #fa6f48,   #b3ff00,   #158556,  #00bbff,  #15307a,    #AA00FF,   #f786c6};
  int[] colors=         {#33353d,#9c0525,#ff1808,#ff7f0f, #fa6f48,   #b3ff00,   #158556,  #00bbff,  #15307a,    #AA00FF,   #f786c6};
  String[] colornames = {"gray", "bordo", "red", "orange", "barack", "green", "darkgreen", "blue", "darkblue", "purple", "rozsaszin"};
  
  //--------------------------------------------------------
  
  Handler(){
    if (gamemode == "desktop"){
      aP_w = height/10;
      aP_h = height/10;
      aP_x = width/2;
      aP_y = height/2+height/10;
      
      sB_w = height/5;
      sB_h = aP_h;
      sB_in_x = width/2+sB_w;
      
      pw = height/10;
      ph = height/10; // player width, height
      player_y = height/2-ph;
      distanceOfPlayers = 1.9; // distance between players
    }
    else {
      aP_w = height/5;
      aP_h = height/5;
      aP_x = width/2;
      aP_y = height*5/6;
      
      sB_w = width/5;
      sB_h = aP_h;
      sB_in_x = width/2+sB_w;
      
      pw = height/5;
      ph = height/5; // player width, height
      player_y = height/2;
      distanceOfPlayers = 1.9; // distance between players
    }
    executable = new ArrayList<Button>();
    players = new ArrayList<Player>();
    disks = new ArrayList<Disk>();
    choosable = new ArrayList <Integer>();

    addPlayer = new Button("addplayer", aP_x, aP_y, aP_w, aP_h, 5, color(255), color(0), color(255), color(50), maxalpha, "rect");
    executable.add(addPlayer);
    addPlayer.add_sign("plus");
    addPlayer.be_visible();
    addPlayer.activate();
    for(int i = 0; i < colors.length; ++i) choosable.add(colors[i]);
  }
  //--------------------------------------------------------
  
  void execute_all(){
    //=======================================
                   check_game();
    //=======================================
    if (eliminatePlayer.deleted) {players.remove(eliminatePlayer); eliminatePlayer = emptyPlayer;}
    ////////////////////////////////////////////////////////////////////////////////////////////////
    for (Button button: addToExe) executable.add(button);
    addToExe.clear();
    for (Button button: addToBottomExe) executable.add(0, button);
    addToBottomExe.clear();
    for (Button button: removeFromExe) executable.remove(button);
    removeFromExe.clear();
    
    for (Button button: executable){
      if (button.visible) button.show();
      if (button.pressed) check_command(button);
    }
    if (gameStarted &&!scoreboard.empty) scoreboard.run_counters();
    ///////////////////////////////////////////////////////////////////////////////////////////////
    if (startable()) add_startbutton();
    else remove_startbutton();
  }
  //--------------------------------------------------------
  
  void check_command(Button button){
    
    button.pressed = false;
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    if(button.type=="addplayer"){
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
      if (players.size()<maxplayers){
        players.add(new Player(width+width/20, 
                               player_y, pw, ph,
                               colors, choosable));
        
        for (int i=0; i<players.size(); ++i) 
          players.get(i).pbutton.slide(width/2-(float(players.size())/2-i-0.5)*pw*distanceOfPlayers, 
                                       player_y, 
                                       700, i<players.size()-1?"whole":"half");
      }
    }
        
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    if (button.type=="player"){
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
      if (gameStarted) checkIndicators(button); 
      if (!basicGameOperationDone){
        if (!button.pmaster.setcolor_active() && !button.pmaster.setcolor.get(0).aas) button.pmaster.show_setcolor();
        else button.pmaster.hide_setcolor();
      }
      else if (!gameStarted &&!button.pmaster.placed){
        if (!button.pmaster.has_placeaim) button.pmaster.add_aim("placing");                // Itt rakj rendet a statementek közt!!!
        else game.kill_aims(button);
      }
      else if (game.currentPlayer==button.pmaster && scoreboard.in_graveyard(button.pmaster)){
        if (!button.pmaster.has_placeaim) button.pmaster.add_aim("placing");
        else game.kill_aims(button);
      }
      //println("playerrrrrrrrr", gameStarted, game.currentPlayer==button.pmaster , !scoreboard.empty && scoreboard.graveyard.contains(button.pmaster) && scoreboard.in_graveyard(button.pmaster), button.pmaster.has_placeaim);
    }
        
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    if (button.type=="setcolor"){
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
      if(button.pmaster.pbutton.fcolor != color(0)) choosable.add(button.pmaster.pbutton.fcolor);
      button.pmaster.pbutton.fcolor = button.fcolor;
      button.pmaster.pbutton.afcolor = color(red(button.fcolor), green(button.fcolor), blue(button.fcolor), 190);
      button.pmaster.hide_setcolor();
      choosable.remove(choosable.indexOf(button.fcolor));
      for (Player player: players)
        player.update_setcolor();
    }
      
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    if (button.type=="delete"){
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
      if(button.pmaster.pbutton.fcolor != color(0)) choosable.add(button.pmaster.pbutton.fcolor);
      eliminatePlayer = button.pmaster;
      eliminatePlayer.suicide_after_slide();
      for (int i=0; i<players.size(); ++i)
        if (i!=players.indexOf(eliminatePlayer)){
          players.get(i).pbutton.slide(width/2-(float(players.size()-1)/2-(i>players.indexOf(eliminatePlayer)? i-1:i)-0.5)*pw*distanceOfPlayers, 
                                       player_y, 
                                       700, "whole");
          players.get(i).update_setcolor();
        }
    }
      
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    if (button.type=="start"){
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
      if (startbutton_inside){
        gameWillStart = true;
        clearExecutable = true;
      }
    }
    
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    if (button.type=="aimend"){
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
      if (gameStarted && !game.stepDone && !scoreboard.in_graveyard(button.amaster.pmaster)){
        if (!button.amaster.pmaster.empty) game.leave_disk(button.amaster.pmaster);
        if (!game.has_tensions()) step_done();
      }
      button.amaster.place_master();
      game.kill_aims(button);
    }
    
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    if (button.type=="pplace"){
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
      if (gameStarted && !removeFromExe.contains(button)) checkIndicators(button); 
      if (gameStarted && ((!game.stepDone && game.currentPlayer == button.pmaster) || game.stepDone)){
        if (button.pmaster.aims.size()==0 && (!game.pushout.activated || game.pushout.pmaster!=button.pmaster)){
          game.kill_all_aims();
          if (game.stepDone) game.find_tensioned_goals(button);
          else game.find_goals(button);
        }
        else {
          game.kill_aims(button);
          game.delete_pushout_button();
        }
      }
    }
    
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    if (button.type=="dplace"){
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
      //game.set_pushout_button(button, button.dmaster.pos, 7);
      if (gameStarted && !removeFromExe.contains(button)) checkIndicators(button); 
      if (gameStarted && game.stepDone && button.dmaster.aims.size()==0 && (!game.pushout.activated || game.pushout.dmaster!=button.dmaster)){ //SZAR!!!!!!!!!!!!!
        game.kill_all_aims();
        game.find_tensioned_goals(button);
      }
      else {
        button.dmaster.kill_aims();
        game.delete_pushout_button();
      }
    }
    
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    if (button.type=="pushout"){
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
      game.push_out();
    }
    
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    if (button.type=="mdisk"){
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
      if (gameStarted) checkIndicators(button); 
    }
    
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    if (button.type=="debugger"){
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
      for (Button button2: executable)
        println(button2.type, button2.amaster.empty, button2.amaster.boardgoal, button2.amaster.directed, button2.amaster.breakpoints);
      print('\n');
    }
  }
  //--------------------------------------------------------------------------
  
  color colorscale(float a, float b, float brightness){
    int R, G, B;
    int where = int(256*5*(a/b));
    if (where < 256) {R=255; G=where; B=0;}
    else if(where < 512) {R=255-(where-256); G=255; B=0;}
    else if (where < 768) {R=0; G=255; B=where-512;}
    else if (where < 1024) {R=0; G=255-(where-768); B=255;}
    else {R=where-1024; G=0; B=255;}
    return color(int(R*brightness), int(G*brightness), int(B*brightness));
  }
  //-------------------------------------------------------------------------------
  
  void checkIndicators(Button button) {
    if (!button.pmaster.empty && (game.stepDone && !game.object_around(button.pmaster.board_place) || 
                                  !game.stepDone && button.pmaster!=game.currentPlayer) || 
        !button.dmaster.empty && (game.stepDone && !game.object_around(button.dmaster.pos) || !game.stepDone)) {
      if (game.stepDone) {
        for (Player p: players)
          if (p.pbutton!=button && game.object_around(p.board_place)) game.addIndicatorTo(p.pbutton);
        for (Disk d: disks)
          if (d.movable!=button && game.object_around(d.pos)) game.addIndicatorTo(d.movable);
      }
      else game.addIndicatorTo(game.currentPlayer.pbutton);
    }
    else game.clearIndicators();
  }
  //----------------------------------------------------------------------------------------------
  
  void add_startbutton(){
    if (!startbutton_added){
      startbutton = new Button("start", width+width/10, aP_y,
                                       sB_w, sB_h, 5,
                                       color(255), color(0), color(255, 0, 0), color(0), maxalpha, "rect");
      executable.add(startbutton); 
      startbutton.add_sign("arrow");
      startbutton.be_visible();
      startbutton.activate();
      startbutton_added = true;
    }
    if (!startbutton_inside){
      startbutton.slide(sB_in_x, aP_y, 1000, "half");
      startbutton.activate();
      startbutton_inside = true;
    }
  }
  //---------------------------------------------------------------------------------------------
  
  void remove_startbutton(){
    if (startbutton_inside){
      startbutton.slide(width+width/10, aP_y, 500, "whole");
      startbutton.deactivate();
      startbutton_inside = false;
    }
  }
  //------------------------------------------------------------------------------------------------
  
  boolean startable(){
    startable = true;
    int living_players = 0;
    ecolors.clear();
    for (Player player: players){
      if (!ecolors.contains(player.pbutton.fcolor) && player.pbutton.fcolor != color(0))
        ecolors.add(player.pbutton.fcolor);
      else {
        startable = false;
        break;
      }
      if (!player.eliminated) ++living_players;
    }
    if (living_players<=1) startable = false;
    
    if (!startable && startbutton_inside) {
      startbutton.ascolor = 255;
      startbutton.signs.get(0).setColors(color(255), color(255));
    }
    else if (startbutton_inside){
      startbutton.ascolor = color(255,0,0);
      startbutton.signs.get(0).setColors(color(255), color(255,0,0));
    }
    return startable;
  }
  
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  
  void check_game(){                 // Function to run after the user added the players, and selected the colors //
    if (clearExecutable) { // Players slide to the right side, placing the players begins //
      clearExecutable=false;
      for (Player player: players){
        player.hide_setcolor();
        player.hide_delete();
        player.pbutton.slide(height+(width-height)/2, height/players.size()*players.indexOf(player)+height/players.size()/2, 700, "whole");
        if (player.pbutton.w>(width-height)/2) player.pbutton.set_size((width-height)/2, (width-height)/2, 700);
      }
      addPlayer.slide(-width, addPlayer.pos.y, 400, "whole");
      startbutton.slide(-width/2, startbutton.pos.y, 600, "whole");
    }
    if (gameWillStart){ // placing the players... //
      if (!players.get(0).pbutton.sliding && !basicGameOperationDone){ // clearing and resetting "executable" //
        executable.clear();
        for (Player player: players)
          addToExe.add(player.pbutton);
        for (int[] object: board.basic_objects)
          disks.add(new Disk(object[0], object[1], object[2]));
        game = new Game(players, disks, this);
        /////////////////////////////////////////////////////////////////////////////
        /*Button debugger = new Button("debugger", 100, 100, 50, 50, 10,
                               color(255,0,0), 0, 255, 0, maxalpha, "oval");
        debugger.be_visible();
        debugger.activate();
        addToExe.add(debugger);*/
        //////////////////////////////////////////////////////////////////////////////
        
        basicGameOperationDone = true;
      }
      else if (basicGameOperationDone){ // Actually placing the players. //
        if(!game.players_placed()){
          game.check_cursor();
          game.execute_aims();
        }
        else { // All players are placed, game begins //
          gameWillStart = false;
          gameStarted = true;
          game.currentPlayer = players.get(0);
          game.set_scoreboard();
        }
      }
    }
    /////////// loop of the game ////////////
    if (gameStarted){ 
    
      game.check_cursor();
      game.execute_aims();
      game.execute_indicators();
      game.execute_rewards();
      
      if (game.stepDone && !game.someone_is_sliding() && !game.has_tensions()){
        /// Step NOT Done yet! ///
        game.stepDone = false;
        if (!game.currentPlayer.zombie) game.currentPlayer = players.get(players.indexOf(game.currentPlayer)+1==players.size() ? 0 : players.indexOf(game.currentPlayer)+1);
        else game.currentPlayer.zombie = false;
        
        scoreboard.playerstate.signs.get(0).text = "N E X T";
        scoreboard.playerstate.slide(scoreboard.get_score(game.currentPlayer).player_icon.pos.x,
                                     board.cs*2.5, 700, "whole");
      }
    }
  }
  //---------------------------------------------------------------------------------------------------------------------------------------
  
  void step_done(){
    game.stepDone = true;
    scoreboard.playerstate.signs.get(0).text = "PLAYING";
    Sign s = scoreboard.get_score(game.currentPlayer).diskcounter.movable.signs.get(0);
    s.text = str(int(s.text)-1);
  }
}
