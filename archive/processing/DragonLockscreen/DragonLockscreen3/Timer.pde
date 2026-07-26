class Timer {
  float time=0, frame=1;
  Timer(){}
  /*void start() { time=millis(); }
  void reset() {start();}
  float get() { return millis()-time; }
  void stop() { time=0; }*/
  void start() { time=0; }
  void reset() {start();}
  float get() { time+=frame; return time; }
  void stop() { time=0; }
}
