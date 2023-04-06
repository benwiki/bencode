class Try{
  PShape disk;
  PVector pos = new PVector(150, 150);
  
  Try(float x, float y, float d, float outer){
    pos.set(x, y);
    disk = createShape();
    disk.beginShape();
    disk.curveTightness(-0.5);
    disk.fill(color(255,0,0));
    disk.noStroke();
    disk.curveVertex(d*outer, 0);
    for (int i=0; i<30; ++i)
      disk.curveVertex(cos(TWO_PI-TWO_PI*i/30)*d*outer, sin(TWO_PI-TWO_PI*i/30)*d*outer);
    disk.curveVertex(d*outer, 0);
    disk.curveVertex(d*outer, 0);
    disk.vertex(d*outer, 0);
    disk.beginContour();
    disk.curveVertex(d, 0);
    for (float i=0; i<8; ++i) {
      disk.curveVertex(cos(TWO_PI/8*i)*d, sin(TWO_PI/8*i)*d);
      disk.curveVertex(cos(TWO_PI/8*i+TWO_PI/8*0.3)*d*0.9, sin(TWO_PI/8*i+TWO_PI/8*0.3)*d*0.9);
      disk.curveVertex(cos(TWO_PI/8*i+TWO_PI/8*0.53)*d*0.57, sin(TWO_PI/8*i+TWO_PI/8*0.53)*d*0.57);
      disk.curveVertex(cos(TWO_PI/8*i+TWO_PI/8*1.2)*d*0.65, sin(TWO_PI/8*i+TWO_PI/8*1.2)*d*0.65);
      disk.curveVertex(cos(TWO_PI/8*i+TWO_PI/8*0.8)*d*0.7, sin(TWO_PI/8*i+TWO_PI/8*0.8)*d*0.7);
      disk.curveVertex(cos(TWO_PI/8*i+TWO_PI/8*0.75)*d*0.9, sin(TWO_PI/8*i+TWO_PI/8*0.75)*d*0.9);
    }
    disk.curveVertex(d, 0);
    disk.curveVertex(d, 0);
    disk.endContour();
    disk.endShape(CLOSE);
  }
  
  void show(){
    push();
    translate(pos.x, pos.y);
    shape(disk);
    pop();
  }
}
