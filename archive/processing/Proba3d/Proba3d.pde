
PShape s;

void setup(){
  fullScreen(P3D);
  s = createShape();
  s.beginShape();
  s.fill(0, 0, 0);
  s.stroke(0);
  s.vertex(0, 0, 0);
  s.vertex(0, 10, 0);
  s.vertex(10, 10, 0);
  s.vertex(10, 0, 0);
  s.vertex(0, 0, 20);
  s.vertex(0, 0, 0);
  s.vertex(0, 10, 0);
  s.vertex(0, 0, 20);
  s.vertex(10, 10, 0);
  s.vertex(10, 0, 0);
  s.bezierVertex(10, 0, 0, 5, 10, 0, 0, 0, 0);
  s.endShape();
  stroke(0);
}

void draw(){
  //shape(s);
  background(255);
  
  translate(width/2, height/2, 800);
  rotateY(float(mouseX)/float(width)*TWO_PI);
  rotateZ(TWO_PI-float(mouseY)/float(height)*TWO_PI);
  shape(s);
}
