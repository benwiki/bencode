
class Indicator{
  
  ArrayList<Button> manage = new ArrayList<Button>();
  
  PVector pos;
  Timer time = new Timer();
  long timestate;
  float disttime = 800; // in milliseconds
  boolean started = false;
  
  Indicator(){}
  
  void add(Button button) {
    if (!manage.contains(button))
      manage.add(button);
  }
  
  void clear() {
    for (Button b: manage) b.alpha = maxalpha;
    manage.clear();
  }
  
  void run(){
    if (!started) { time.start(); started = true; }
    timestate = time.state();
    for (Button button: manage) button.alpha = map( (disttime/2 - timestate%disttime)*(timestate%(disttime*2)<disttime?1:-1),  -disttime/2,disttime/2,  maxalpha*0.45,maxalpha );
  }
}
