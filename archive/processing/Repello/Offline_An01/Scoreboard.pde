class Scoreboard{
  
  ArrayList<Score> player_scores;
  ArrayList<Player> graveyard;
  Disk[] disk_icons;
  Button playerstate;
  
  boolean empty = false;
  
  //==============================
  Scoreboard() { empty = true; }
  //==============================
  
  Scoreboard(String just_to_make_sure_it_is_not_the_empty_constructor){
    player_scores = new ArrayList<Score>();
    graveyard = new ArrayList<Player>();
    for (Player player: handler.players)
      player_scores.add( new Score(player) );
    
    disk_icons = new Disk[3];
    for (int i=0; i<3; ++i) {
      disk_icons[i] = new Disk(width+board.cs, height/8*(i+1.5)+board.cs, board.cs, board.cs, i+1, -1);
      disk_icons[i].movable.slide(height+(width-height) / (handler.players.size()+1) * 0.5,
                                  height/8 * i + board.cs*3.5, 
                                  1000 + 100*i, "whole");
    }
    
    playerstate = new Button("playerstate", width+2*board.cs, board.cs*2.5, board.cs*1.5, board.cs*5/9, board.cs/10,
                             color(255,0,0), color(0), color(255,0,0), color(0), maxalpha, "rect");
    playerstate.slide(height+(width-height) / (handler.players.size()+1) * 1.5, board.cs*2.5, 1000, "whole");
    //playerstate.slide(player_scores.get(0).player_icon.pbutton.pos.x, board.cs*2.5, 1000, "whole");
    playerstate.be_visible();
    playerstate.add_sign("text", "N E X T", new PVector(0, -board.cs/17));
    addToExe.add(playerstate);
  }
  //------------------------------------------------------------------------------------------------------
  
  Score get_score (Player player){
    for (Score score: player_scores)
      if (score.master == player)
        return score;
        
    println("ERROR!!! score not found");
    return new Score(new Player());
  }
  //----------------------------------------------
  
  boolean in_graveyard (Player p){
    if (empty) return false;
    if (graveyard.contains(p)) return true;
    else return false;
  }
  
};

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class Score{
  
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
  
  Score(Player master){
    this.master = master;
    player_icon = new Player(width+board.cs, board.cs*1.5, board.cs, board.cs, master.pbutton.fcolor);
    player_icon.pbutton.slide(height+(width-height) / (handler.players.size()+1) * (handler.players.indexOf(master) + 1.5), 
                              board.cs*1.5, 
                              1000 + 150*handler.players.indexOf(master), "whole");
                       
    diskcounter = new Disk(width+board.cs, board.cs*1.5 - board.cs * 2/3, board.cs * 2/3, board.cs * 2/3, 1, 15);
    diskcounter.movable.slide(height+(width-height) / (handler.players.size()+1) * (handler.players.indexOf(master) + 1.5) - board.cs/2,
                              board.cs*1.5 - board.cs/2, 
                              1000 + 150*handler.players.indexOf(master), "whole");
    
    gray_disks = new ArrayList<Disk>();
    silver_disks = new ArrayList<Disk>();
    golden_disks = new ArrayList<Disk>();
    
    /*int i=0;
    //,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
    graycounter = new Button("counter", width+board.cs, height/8*(i++ + 1.5)+board.cs, board.cs*2/3, board.cs*2/3, 0, 
                             color(0), color(0), color(0), color(0), maxalpha, "oval");
    graycounter
    graycounter.slide(
    //..................................................................................................................
    silvercounter = new Button("counter", width+board.cs, height/8*(i++ + 1.5)+board.cs, board.cs*2/3, board.cs*2/3, 0, 
                               color(0), color(0), color(0), color(0), maxalpha, "oval");
    silvercounter.slide(
    //..................................................................................................................
    goldencounter = new Button("counter", width+board.cs, height/8*(i++ + 1.5)+board.cs, board.cs*2/3, board.cs*2/3, 0, 
                               color(0), color(0), color(0), color(0), maxalpha, "oval");
    goldencounter.slide(*/
  }
  //----------------------------------------------------------------------------------------------------------------------------------
  
  ArrayList<Disk> get_disklist (Disk colordisk){
    if      (colordisk.movable.fcolor == 1) return this.gray_disks;
    else if (colordisk.movable.fcolor == 2) return this.silver_disks;
    else                                    return this.golden_disks;
  }
  //-----------------------------------------------------------------------
  
};
