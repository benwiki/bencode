
class Curve {
  
  private final int SEGMENT_COUNT=100;
  private PVector p1, p2, cp1, cp2, fin = new PVector();
  private float[] lengths = new float[SEGMENT_COUNT+1];
  float length;
  
  //=========================================================
  Curve (PVector p1, PVector p2, PVector p3, PVector p4) {
    this.cp1 = p1.copy();
    this.p1 = p2.copy();
    this.p2 = p3.copy();
    this.cp2 = p4.copy();
    calculateLength();
  }
  //------------------------
  
  float length(){
    return length;
  }
  //------------------------
  
  void set (PVector p1, PVector p2, PVector p3, PVector p4) {
    this.cp1.set(p1);
    this.p1.set(p2);
    this.p2.set(p3);
    this.cp2.set(p4);
    calculateLength();
  }
  //---------------------------------------------------
  
  void show(){
    stroke(0); noFill();
    curve(cp1.x, cp1.y, p1.x, p1.y, p2.x, p2.y, cp2.x, cp2.y);
    ellipse(p1.x, p1.y, 10, 10);
    ellipse(p2.x, p2.y, 10, 10);
    /*beginShape();
    curveVertex(path.get(0).x, path.get(0).y);
    for (int i=0; i<path.size()-1; ++i) {
      curveVertex(path.get(i).x, path.get(i).y);
      ellipse(path.get(i).x, path.get(i).y, 10, 10);
    }
    curveVertex(path.get(path.size()-1).x, path.get(path.size()-1).y);
    endShape();*/
  }
  //--------------------------------
  
  PVector getPt (float rate) {
    fin.set(curvePoint(cp1.x, p1.x, p2.x, cp2.x, rate), 
            curvePoint(cp1.y, p1.y, p2.y, cp2.y, rate));
    return fin;
  }
  //------------------------------------------------------------------------
  
  PVector getEqPt(float r) {
    return pointAtLength(length * r);
  }
  //----------------------------------------------------------------------
  
  PVector pointAtLength(float wantedLength) {
    wantedLength = constrain(wantedLength, 0.0, length);
    int index = java.util.Arrays.binarySearch(lengths, wantedLength);
    float mappedIndex;

    if (index < 0) {
      if (index == -1) return getPt(map(wantedLength, 0,lengths[0], 0,1) / SEGMENT_COUNT);
      int nextIndex = -(index + 1);
      int prevIndex = nextIndex - 1;
      mappedIndex = map(wantedLength, lengths[prevIndex], lengths[nextIndex], prevIndex, nextIndex);
    }
    else mappedIndex = index;
    
    return getPt(mappedIndex / SEGMENT_COUNT);
  }
  //----------------------------------------------------------------------
  
  private void calculateLength(){
    PVector prev = new PVector(), point = new PVector();
    prev.set(p1);
    
    length=0;
    for (int i = 0; i <= SEGMENT_COUNT; i++) {
      float t = (float) i / SEGMENT_COUNT;
      point = getPt(t);
      float distanceFromPrev = PVector.dist(prev, point);
      length += distanceFromPrev;
      lengths[i] = length;
      prev.set(point);
    }
  }
}
