
ArrayList<Layer> layers = new ArrayList<Layer>();

int layernum=5, empty=0;

void setup(){
  rectMode(CORNER);
  noStroke();
  newLayers();
}

void draw(){
  background(0);
  for (int i=layers.size(); --i>=0;) layers.get(i).show();
  if (mousePressed)
    for (Layer layer: layers)
      if (layer.over()) break;
}

void newLayers(){
  layers.clear();
  empty=0;
  for (int i=1;i<layernum+1;++i)
    layers.add(new Layer(randomColor(), i*4, i*4));
}

color randomColor(){
  return color(random(0,255), random(0,255), random(0,255));
}