class Handler{
  
  Board board;
  
  ArrayList<Button> executable;
  ArrayList<Player> players;
  ArrayList<Disk> disks;
  ArrayList<Integer> ecolors = new ArrayList<Integer>();
  Player eliminatePlayer = new Player();
  
  Button addPlayer;
  int aP_w = height/10;
  int aP_h = height/10;
  int aP_x = width/2;
  int aP_y = height/2+height/10;
  
  Button startbutton;
  int sB_w = height/5;
  int sB_h = aP_h;
  int sB_in_x = width/2+sB_w;
  
  int pw = height/10, ph = height/10; // player width, height
  int player_y = height/2-ph;
  float playerDist = 1.9; // distance bw players
  
  boolean gameWillStart = false, gameStarted = false, basicGameOperationDone=false, clearExecutable=false;
  boolean startbutton_inside=false, startbutton_added=false;
  
  ArrayList<Integer> choosable;//
  int[] colors= {#777777,#85000D,#FF0000,#FFAA00,#FFFF00,#95FF00,#039C00,#00E5FF,#0000FF,#AA00FF,#FF00C3};
  
  //--------------------------------------------------------
  
  Handler(Board board){
    executable = new ArrayList<Button>();
    removeFromExe = new ArrayList<Button>();
    addToBottomExe = new ArrayList<Button>();
    addToExe = new ArrayList<Button>();
    players = new ArrayList<Player>();
    disks = new ArrayList<Disk>();
    choosable = new ArrayList <Integer>();
    this.board = board;
    get_ready();
  }
  //--------------------------------------------------------
  
  void get_ready(){
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
    if (eliminatePlayer.deleted) {players.remove(eliminatePlayer); eliminatePlayer = new Player();}
    ////////////////////////////////////////////////////////////////////////////////////////////////
    for (Button button: removeFromExe) executable.remove(button);
    removeFromExe.clear();
    for (Button button: addToExe) executable.add(button);
    addToExe.clear();
    for (Button button: addToBottomExe) executable.add(0, button);
    addToBottomExe.clear();
    
    for (Button button: executable)
      if (button.visible){
        button.show();
        if (button.pressed) check_command(button);
      }
    ///////////////////////////////////////////////////////////////////////////////////////////////
    if (startable()) add_startbutton();
    else remove_startbutton();
  }
  //--------------------------------------------------------
  
  void check_command(Button button){
    button.pressed = false;
    switch(button.type){
      ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
      case "addplayer":
      ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
      if (players.size()<maxplayers){
        players.add(new Player(width+width/20, 
                               height/2-ph, pw, ph,
                               colors, choosable));
        
        for (int i=0; i<players.size(); ++i) 
          players.get(i).pbutton.slide(width/2-(float(players.size())/2-i-0.5)*pw*playerDist, 
                                       player_y, 
                                       700, i<players.size()-1?"whole":"half");
      }
      break;
        
      ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
      case "player":
      ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
      if (!basicGameOperationDone){
        if (!button.pmaster.setcolor_active() && !button.pmaster.setcolor.get(0).aas) button.pmaster.show_setcolor();
        else button.pmaster.hide_setcolor();
      }
      else if (!gameStarted){
        if (button.pmaster.aims.size()==0) button.pmaster.add_aim("placing");
        else button.pmaster.clear_aims();
      }
      break;
        
      ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
      case "setcolor": 
      ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
      if(button.pmaster.pbutton.fcolor != color(0)) choosable.add(button.pmaster.pbutton.fcolor);
      button.pmaster.pbutton.fcolor = button.fcolor;
      button.pmaster.pbutton.afcolor = color(button.fcolor, 190);
      button.pmaster.hide_setcolor();
      choosable.remove(choosable.indexOf(button.fcolor));
      for (Player player: players)
        player.update_setcolor();
      break;
      
      ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
      case "delete":
      ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
      if(button.pmaster.pbutton.fcolor != color(0)) choosable.add(button.pmaster.pbutton.fcolor);
      eliminatePlayer = button.pmaster;
      eliminatePlayer.suicide_after_slide();
      for (int i=0; i<players.size(); ++i)
        if (i!=players.indexOf(eliminatePlayer)){
          players.get(i).pbutton.slide(width/2-(float(players.size()-1)/2-(i>players.indexOf(eliminatePlayer)? i-1:i)-0.5)*pw*playerDist, 
                                       player_y, 
                                       700, "whole");
          players.get(i).update_setcolor();
        }
      break;
      
      ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
      case "start":
      ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
      if (startbutton_inside){
        for (Player player: players)
          player.alive = false;
        gameWillStart = true;
        clearExecutable = true;
      }
      break;
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
    boolean startable = true;
    int living_players = 0;
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
      startbutton.sign_acol = 255;
    }
    else if (startbutton_inside){
      startbutton.ascolor = color(255,0,0);
      startbutton.sign_acol = color(255,0,0);
    }
    ecolors.clear();
    return startable;
  }
  
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  
  void check_game(){
    if (clearExecutable) {
      clearExecutable=false;
      for (Player player: players){
        player.hide_setcolor();
        player.hide_delete();
        player.pbutton.slide(height+(width-height)/2, height/players.size()*players.indexOf(player)+height/players.size()/2, 700, "whole");
      }
      addPlayer.slide(-width, addPlayer.pos.y, 400, "whole");
      startbutton.slide(-width/2, startbutton.pos.y, 600, "whole");
    }
    if (gameWillStart){
      if (!players.get(0).pbutton.sliding && !basicGameOperationDone){
        executable.clear();
        for (Player player: players)
          addToExe.add(player.pbutton);
        for (int[] object: board.basic_objects)
          disks.add(new Disk(board, object[0], object[1], object[2]));
        game = new Game(players, disks, this);
        basicGameOperationDone = true;
      }
      else if (basicGameOperationDone && !game.players_placed()){
        game.check_cursor();
        game.execute_aims();
      }
    }
    if (gameStarted){
      
    }
  }
}
