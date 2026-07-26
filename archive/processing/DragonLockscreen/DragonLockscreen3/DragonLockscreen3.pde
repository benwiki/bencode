
//import android.view.WindowManager;

Dragon dragon;
float w, h;
PVector mouse = new PVector();
float mouseMinDist = width/20;
float normalDragonSpeed = float(width+height)/100;

void setup() {

   //getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON|
   //             WindowManager.LayoutParams.FLAG_DISMISS_KEYGUARD|
   //             WindowManager.LayoutParams.FLAG_SHOW_WHEN_LOCKED|
   //             WindowManager.LayoutParams.FLAG_TURN_SCREEN_ON);

  size(400, 700);
  //fullScreen();
  w = width; h = height;
  setGlass();
  showGlass();
  dragon = new Dragon(new PVector(0, height/2));
  surface.setResizable(true);
}

void draw() {
  background(0);

  mouse.set(mouseX, mouseY);

  if (w!=width || h != height) {
    setGlass();
    dragon = new Dragon(new PVector(0, height/2));
    w = width; h = height;
  }

  dragon.move();
  showGlass();
}

void mousePressed(){
  dragon.setSpeedRelated(5.0);
}

void mouseReleased(){
  //dragon.setSpeedRelated(1.0);
  //for (DragonPart part: dragon.parts) {
  //  part.go=false;
  //  //part.late = dragon.partWidth / dragon.speed / 3.5 / 1.3;
  //}
  dragon = new Dragon(mouse);
}

PVector randomVector() {
  return new PVector(random(width), random(height));
}

PVector randomCheckedVector() {
  PVector pt = new PVector(random(width), random(height));
  while (!dragon.goodPoint(pt)) pt.set(random(width), random(height));
  return pt;
}
