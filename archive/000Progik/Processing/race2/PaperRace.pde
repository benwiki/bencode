
Button test;
Handler handler = new Handler();

ArrayList<Button> exe = new ArrayList<Button>(); 
ArrayList<Button> toexe = new ArrayList<Button>(); 

void setup(){
  fullScreen();
  test = new Button(new PVector(width/2, height/2), new PVector(100,100), "navi", "start");
  handler.toexe(test);
}

void draw(){
  background (255);
  handler.runall();
}

void mouseReleased(){
  for (Button b: exe)
    if (b.isOver()) b.press();
}