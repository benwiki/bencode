
Button test;
Handler handler = new Handler();

ArrayList<Button> exe = new ArrayList<Button>(); 
ArrayList<Button> toexe = new ArrayList<Button>(); 

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
  for (Button b: exe)
    if (b.mouseOver) b.press();
}
