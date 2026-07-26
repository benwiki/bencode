
//import android.view.WindowManager;

Dragon dragon;
float w, h;
PVector mouse = new PVector();
float mouseMinDist = width/20;

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
  dragon = new Dragon();
  //surface.setResizable(true);
}

void draw() {
  background(255);

  mouse.set(mouseX, mouseY);

  if (w!=width || h != height) {
    setGlass();
    dragon = new Dragon();
    w = width; h = height;
  }

  dragon.move();
  dragon.showPath();
  dragon.showTimers();
  //showGlass();
}

PVector randomVector() {
  return new PVector(random(width), random(height));
}

PVector randomCheckedVector() {
  PVector pt = new PVector(random(width), random(height));
  while (!dragon.goodPoint(pt)) pt.set(random(width), random(height));
  return pt;
}
