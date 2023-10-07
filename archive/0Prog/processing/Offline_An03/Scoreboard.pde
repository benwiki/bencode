class Scoreboard {

  ArrayList<Score> player_scores;
  ArrayList<Player> graveyard;
  Disk[] disk_icons;
  Button[] rewards;
  Button[] dead;
  Button playerstate;


  boolean empty = false;

  //==============================
  Scoreboard() { 
    empty = true;
  }
  //==============================

  Scoreboard(String just_to_make_sure_it_is_not_the_empty_constructor) {
    player_scores = new ArrayList<Score>();
    graveyard = new ArrayList<Player>();
    for (Player player : handler.players)
      player_scores.add( new Score(player) );

    disk_icons = new Disk[3];
    for (int i=0; i<3; ++i) {
      disk_icons[i] = new Disk(width+board.cs, height/8*(i+1.5)+board.cs, board.cs, board.cs, i+1, -1);
      disk_icons[i].movable.slide(height+(width-height) / (handler.players.size()+1) * 0.5, 
        height/8 * i + board.cs*3.5, 
        1000 + 100*i, "whole");
    }

    playerstate = new Button("playerstate", width+2*board.cs, board.cs*2.5, board.cs*1.5, board.cs*5/9, board.cs/10, 
      color(255, 0, 0), color(0), color(255, 0, 0), color(0), maxalpha, "rect");
    playerstate.slide(height+(width-height) / (handler.players.size()+1) * 1.5, board.cs*2.5, 1000, "whole");
    //playerstate.slide(player_scores.get(0).player_icon.pbutton.pos.x, board.cs*2.5, 1000, "whole");
    playerstate.be_visible();
    playerstate.add_sign("text", "N E X T", new PVector(0, -board.cs/17));
    addToExe.add(playerstate);

    //................................REWAAAAAAAAAAAAAAAARDS.......................................
    rewards = new Button[3];
    for (int i=0; i<3; ++i) {
      rewards[i] = new Button("reward_"+colors[i], height+(width-height) / (handler.players.size()+1) * 0.5, height/8 * i + board.cs*3.5, board.cs*1.3, board.cs*1.3, 0, 
        color(0), color(255, 0, 0), color(0), color(255, 0, 0), maxalpha, "oval");
      addToBottomExe.add(rewards[i]);
    }

    //............ THE DEAD SIGNS ..............//
    dead = new Button[handler.players.size()];
    for (int i=0; i<dead.length; ++i) {
      dead[i] = new Button("death", height+(width-height) / (handler.players.size()+1) * (i + 1.5), board.cs*0.5, board.cs*0.3, board.cs*0.3, board.cs*0.05, 
        color(255, 0, 0), color(0), color(255, 0, 0), color(0), maxalpha, "oval");
      dead[i].add_sign("stroke");
      addToExe.add(dead[i]);
    }
  }
  //------------------------------------------------------------------------------------------------------

  Score get_score (Player player) {
    for (Score score : player_scores)
      if (score.master == player)
        return score;

    println("ERROR!!! score not found");
    return new Score(new Player());
  }
  //----------------------------------------------

  boolean in_graveyard (Player p) {
    if (empty) return false;
    if (graveyard.contains(p)) return true;
    else return false;
  }
  //---------------------------------------------------------------
  
  //Player getPlayerFromGraveyard 
  /*boolean isIcon (Disk d) {
   return disk_icons[0]==d || disk_icons[1]==d || disk_icons[2]==d;
   }*/
  //----------------------------------------------------------------

  void runCounters() {
    for (Score s : player_scores) {
      s.graycounter.show();
      s.silvercounter.show();
      s.goldencounter.show();
    }
  }
  //-------------------------------------------

  void activateRewards(Player p) {
    for (int i=0; i<3; ++i) {
      if (get_score(p).get_disklist(i+1).size()==0) continue;
      game.get_reward = true; // azért ide rakom, mert fáradtságos lenne ellenőrizni, hogy van-e korong amit el lehet lopni. Így ha nincs, ez egyszer sem fog lefutni.
      rewards[i].activate();
      rewards[i].be_visible();
      game.addIndicatorTo(rewards[i]);
    }
  }
  //-----------------------------------------

  void deactivateRewards() {
    for (int i=0; i<3; ++i) {
      rewards[i].deactivate();
      rewards[i].hide();
    }
    game.clearIndicators();
  }
  //------------------------------------
  void destroy_scoreboard(){
    int destroytime = 1000;
    for (Score s: player_scores) s.slide(width*1.2, destroytime, "whole");
    for (Player p: graveyard) p.pbutton.slide(p.pbutton.pos.x, height*1.2, destroytime, "whole");
    for (Disk d: disk_icons) d.movable.slide(width*1.2, d.movable.pos.y, destroytime, "whole");
    for (Button b: rewards) b.slide(width*1.2, b.pos.y, destroytime, "whole");
    for (Button b: dead) b.slide(width*1.2, b.pos.y, destroytime, "whole");
    playerstate.slide(width*1.2, playerstate.pos.y, destroytime, "whole");
    //for (Player p: this.graveyard) {
    //  p.do_suicide();
    //  println(p); //<>//
    //}
  }
};

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class Score {

  Player master;

  Player player_icon;
  Disk diskcounter;

  ArrayList<Disk> gray_disks;
  ArrayList<Disk> silver_disks;
  ArrayList<Disk> golden_disks;

  Button graycounter;
  Button silvercounter;
  Button goldencounter;

  ////////////////////////////////////////////

  Score(Player master) {
    this.master = master;
    player_icon = new Player(width+board.cs, board.cs*1.5, board.cs, board.cs, master.pbutton.fcolor);
    player_icon.pbutton.slide(height+(width-height) / (handler.players.size()+1) * (handler.players.indexOf(master) + 1.5), 
      board.cs*1.5, 
      1000 + 150*handler.players.indexOf(master), "whole");

    diskcounter = new Disk(width+board.cs, board.cs*1.5 - board.cs * 2/3, board.cs * 2/3, board.cs * 2/3, 1, startingDiskNum);
    diskcounter.movable.slide(height+(width-height) / (handler.players.size()+1) * (handler.players.indexOf(master) + 1.5) - board.cs/2, 
      board.cs*1.5 - board.cs/2, 
      1000 + 150*handler.players.indexOf(master), "whole");

    gray_disks = new ArrayList<Disk>();
    silver_disks = new ArrayList<Disk>();
    golden_disks = new ArrayList<Disk>();

    int i=0; /////////////// MINDIG ELÖL KELL, HOGY LEGYENEK!!!!!!!!! \\\\\\\\\\\\\\\\\\
    //,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
    graycounter = new Button("counter", width+board.cs, height/8 * i + board.cs*3.8, board.cs*2/3, board.cs*2/3, board.cs/20, 
      color(255), color(0), color(255), color(0), maxalpha, "oval");
    //graycounter.be_visible();
    graycounter.add_sign("text", "0", new PVector(0, -board.cs/20));

    graycounter.slide(height+(width-height) / (handler.players.size()+1) * (handler.players.indexOf(master) + 1.5), height/8 * i + board.cs*3.8, 1000 + 150*handler.players.indexOf(master), "whole");
    ++i;
    //..................................................................................................................
    silvercounter = new Button("counter", width+board.cs, height/8 * i + board.cs*3.8, board.cs*2/3, board.cs*2/3, board.cs/20, 
      color(255), color(0), color(255), color(0), maxalpha, "oval");
    //silvercounter.be_visible();
    silvercounter.add_sign("text", "0", new PVector(0, -board.cs/20));

    silvercounter.slide(height+(width-height) / (handler.players.size()+1) * (handler.players.indexOf(master) + 1.5), height/8 * i + board.cs*3.8, 1000 + 150*handler.players.indexOf(master), "whole");
    ++i;
    //..................................................................................................................
    goldencounter = new Button("counter", width+board.cs, height/8 * i + board.cs*3.8, board.cs*2/3, board.cs*2/3, board.cs/20, 
      color(255), color(0), color(255), color(0), maxalpha, "oval");
    //goldencounter.be_visible();
    goldencounter.add_sign("text", "0", new PVector(0, -board.cs/20));

    goldencounter.slide(height+(width-height) / (handler.players.size()+1) * (handler.players.indexOf(master) + 1.5), height/8 * i + board.cs*3.8, 1000 + 150*handler.players.indexOf(master), "whole");
    ++i;
  }
  //----------------------------------------------------------------------------------------------------------------------------------

  ArrayList<Disk> get_disklist (int col) {
    if      (col == GRAY)   return this.gray_disks;
    else if (col == SILVER) return this.silver_disks;
    else                    return this.golden_disks; // if GOLD
  }
  //-----------------------------------------------------------------------
  void add_to_counter(int col, int val) {
    if      (col==GRAY)   graycounter.signs.get(0).text   = str(int(graycounter.signs.get(0).text)+val);
    else if (col==SILVER) silvercounter.signs.get(0).text = str(int(silvercounter.signs.get(0).text)+val);
    else if (col==GOLD)   goldencounter.signs.get(0).text = str(int(goldencounter.signs.get(0).text)+val);
  }
  //------------------------------------------------------------------------------------------

  void addToDiskCounter (int val) {
    diskcounter.movable.signs.get(0).addToText(val);
  }

  boolean outOfDisks () {
    return diskcounter.movable.signs.get(0).text.equals("0");
  }
  
  int sum () {
    return gray_disks.size() + silver_disks.size()*2 + golden_disks.size()*5;
  }
  
  void slide(float x, int millis, String mode){
    master.pbutton.slide(x, master.pbutton.pos.y, millis, mode);
    diskcounter.movable.slide(x, diskcounter.movable.pos.y, millis, mode);
    for (Disk d: gray_disks) d.movable.slide(x, d.movable.pos.y, millis, mode);
    for (Disk d: silver_disks) d.movable.slide(x, d.movable.pos.y, millis, mode);
    for (Disk d: golden_disks) d.movable.slide(x, d.movable.pos.y, millis, mode);

    graycounter.slide(x, graycounter.pos.y, millis, mode);
    silvercounter.slide(x, silvercounter.pos.y, millis, mode);
    goldencounter.slide(x, goldencounter.pos.y, millis, mode);
  }
};
