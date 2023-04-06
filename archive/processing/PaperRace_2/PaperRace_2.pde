
Button test;
Handler handler = new Handler();

boolean happening=false;
void happening(){happening = true;}



void setup(){
  fullScreen();
  //size(700, 1000);
  test = new Button(new PVector(width/2, height/2), new PVector(width/4, height/4), "navi")
                  .setFillColor(color(0))
                  .setActiveFillColor(color(random(255), random(255), random(255)))
                  .setStrokeWeight(0);
  handler.toexe(test);
  rectMode(CENTER);
}

void draw(){
  background(255);
  handler.runall();
}

void mouseReleased(){
  /*int v=0;
  for (Button b: exe) if(b.visible) ++v;
  println(v, exe.size());
  happening();*/
  handler.checkPressed();
}
