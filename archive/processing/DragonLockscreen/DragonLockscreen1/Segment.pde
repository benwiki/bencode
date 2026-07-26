
class Segments {
  
  PVector[] lines = new PVector[20];
  PVector m = new PVector();
  float segLength = 9;
 
  Segments(){
    
  }

  void setSegments(){
    for (int i=0; i<lines.length; ++i) lines[i] = new PVector();
  }
  //------------------------------------------------------------------
  
  void dragSegment(int i, PVector in) {
    PVector d = PVector.sub(in, lines[i]);
    float angle = atan2(d.y, d.x);
    lines[i].set(in.x - cos(angle) * segLength, in.y - sin(angle) * segLength);
    show(lines[i], angle);
  }
  //------------------------------------------------------------------
  
  void show(PVector p, float a) {
    pushMatrix();
    translate(p.x, p.y);
    rotate(a);
    line(0, 0, segLength, 0);
    popMatrix();
  }
  //--------------------------------------------------
}
