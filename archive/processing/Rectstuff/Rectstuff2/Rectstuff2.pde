
import android.view.WindowManager;

ArrayList<Layer> layers = new ArrayList<Layer>();
PVector deletepoint = new PVector(-1, -1);
int layernum=5, empty=0, next=0;
boolean released=false;

void setup(){
  getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON|
                WindowManager.LayoutParams.FLAG_DISMISS_KEYGUARD|
                WindowManager.LayoutParams.FLAG_SHOW_WHEN_LOCKED|
                WindowManager.LayoutParams.FLAG_TURN_SCREEN_ON);
  fullScreen();
  //boolean[] l = {true, true, true};
  //Boolist bl = new Boolist(l);
  rectMode(CORNER);
  noStroke();
  textFont(createFont("Serif-Italic", width/10));
  textAlign(CENTER, CENTER);
  newLayers();
}

void draw(){
  background(0);
  text((hour()<10?"0":"")+str(hour())+":"+(minute()<10?"0":"")+str(minute())+":"+(second()<10?"0":"")+str(second()), width/2, height/2);
  if (mousePressed){
    for (Layer layer: layers)
      if (layer.checkpt()) break;
    if (released) released=false;
  }
  else if (!released) released=true;
  for (int i=layers.size(); --i>=0;) layers.get(i).show();

  //fill(255);
  //text(str(layers.size()), 100, 100);
}

void newLayers(){
  layers.clear();
  empty=0;
  for (int i=0;i<layernum;++i)
    layers.add(new Layer(randomColor(), (i+1)*4,(i+1)*4));
}

color randomColor(){
  return color(random(0,256), random(0,256), random(0,256));
}
