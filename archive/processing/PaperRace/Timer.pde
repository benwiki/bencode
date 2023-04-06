
class Timer {
  float time;
  Timer(){}
  void start(){
    time = millis();
  }
  float get(){
    return millis()-time;
  }
  void stop(){
    time=0;
  }
};
