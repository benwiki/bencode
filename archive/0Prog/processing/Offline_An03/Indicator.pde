
class Indicator{
  
  ArrayList<Button> manage = new ArrayList<Button>(),
                    show_me_for_ducks_sake = new ArrayList<Button>();
  
  PVector pos;
  Timer time = new Timer();
  long timestate;
  float disttime = 800, mapped, rate=1.2; // in milliseconds
  boolean started = false, growing=true;
  
  Indicator(){}
  
  void add(Button button) {
    if (!manage.contains(button)) {
      manage.add(button);
      time.start();
    }
    /*else if (!show_me_for_ducks_sake.contains(button)) {
      show_me_for_ducks_sake.add(button);
      sizeLaunch(button);
      time.start();
    }*/
  }
  
  void clear() {
    for (Button b: manage) b.alpha = maxalpha;
    manage.clear();
    /*for (Button button: show_me_for_ducks_sake) {
      if (button.isOver()) button.set_size(board.cs/2, board.cs/2, 0);
      else button.set_size(board.cs, board.cs, 0);
    }
    //for (Button button: show_me_for_ducks_sake) button.slide(board.boardc_to_c(!button.pmaster.empty ? button.pmaster.board_place : button.dmaster.pos).x-board.cs/4, 
      //                                                       board.boardc_to_c(!button.pmaster.empty ? button.pmaster.board_place : button.dmaster.pos).y+board.cs/4, 0, "normal");
    show_me_for_ducks_sake.clear();*/
  }
  
  void run(){
    if (!started) { time.start(); started = true; }
    timestate = time.state();
    if (timestate>disttime) {
      time.reset(disttime);
      //for (Button button: show_me_for_ducks_sake) sizeLaunch(button);
      //growing = !growing;
    }
    //mapped = timestate%disttime;
    for (Button button: manage) button.alpha = map( timestate%disttime,  disttime,0,  maxalpha*0.45,maxalpha );
  }
  /*
  void sizeLaunch(Button button) {
    if (!button.pmaster.empty && button.pmaster.smallMode || !button.dmaster.empty && button.dmaster.smallMode) return;
    if (growing) button.set_size(board.cs*rate, board.cs*rate, (int)(disttime));
    else button.set_size(board.cs/rate, board.cs/rate, (int)(disttime));
  }*/
}
