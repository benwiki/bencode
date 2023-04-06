Try trying;
void setup() {
  size(1200, 1200);
  background(255);
  smooth();
  /*trying = new Try(300, 300, 300/2.3, 2.3);
  trying.disk.setFill(color(0));*/
  //disk = createShape();
  translate(600, 600);
  float outer=1.9375;
  float d = 600/outer;
  beginShape();
  curveTightness(-0.5);
  
  curveVertex(d*outer, 0);
  for (int i=0; i<100; ++i)
    curveVertex(cos(TWO_PI-TWO_PI*i/100)*d*outer, sin(TWO_PI-TWO_PI*i/100)*d*outer);
  curveVertex(d*outer, 0);
  curveVertex(d*outer, 0);
  vertex(d*outer, 0);
  beginContour();
  curveVertex(d, 0);
  //float[] deg = {0, 0.3, 0.65, 1.25, 0.87, 0.75};
  /////////////////////////////////////////////////
  /*disk2:
  float[] deg = {0, 0.3, 0.63, 1.2, 0.77, 0.75};
  float[] dist ={1, 0.88, 0.55, 0.6, 0.64, 0.87};*/
  float[] deg = {0, 0.3, 0.63, 1.2, 0.77, 0.75};
  float[] dist ={1, 0.88, 0.55, 0.6, 0.64, 0.87};
  fill(255,0,0);
  noStroke();
  for (float i=0; i<8; ++i) {
    for (int k=0; k<6; ++k){
      curveVertex(cos(TWO_PI/8*i+TWO_PI/8*deg[k])*d*dist[k], sin(TWO_PI/8*i+TWO_PI/8*deg[k])*d*dist[k]);
      ellipse(cos(TWO_PI/8*i+TWO_PI/8*deg[k])*d*dist[k], sin(TWO_PI/8*i+TWO_PI/8*deg[k])*d*dist[k], 3, 3);
    }
  }
  curveVertex(d, 0);
  curveVertex(d, 0);
  endContour();
  fill(color(0));
  //noFill();
  //stroke(0);
  noStroke();
  endShape(CLOSE);
  save("disk4.png");
}

void draw() {
   /*background(255);
   trying.show();*/
}

float calc_deg(float start, PVector p1, PVector p2) {
  float c = (p1.x-p2.x)/p1.dist(p2);
  float s = (p1.y-p2.y)/p1.dist(p2);
  float recovery = acos(c)*s/abs(s)-start;
  float dgc = acos(cos(recovery));
  float elojel = int(sin(recovery)/abs(sin(recovery)));
  return dgc*elojel;
}
