
class Cube {

  PVector pos = new PVector(), 
    size = new PVector(), 
    corner = new PVector(), 
    onboardpos = new PVector(), 
    p = new PVector(), s = new PVector();
  PShape shape;  
  boolean col = RED, king = false, moving = true;
  float sw = 1;
  int top, fw, side;

  //---------------------------------------------------------

  Cube (float x, float y, boolean col) {
    onboardpos.set(x, y);
    pos.set(width/2+(-4+x)*cs, height/2+(-3.5+y)*cs); p.set(pos);
    size.set(cs, cs); s.set(size);
    corner.set(pos.x-size.x/2, pos.y-size.y/2);
    this.col = col;
    createCube();
  }

  Cube setSides (int t, int f) {
    if (t==0) { king = true; top = KING; fw = KING; }
    else { top = t; fw = f; }
    return this;
  }
  //----------------------

  void resize () {
    pos.set(width/2+(-4+onboardpos.x)*cs, height/2+(-3.5+onboardpos.y)*cs);
    size.set(cs, cs);
    corner.set(pos.x-size.x/2, pos.y-size.y/2);
    createCube();
  }
  //------------------------

  void show () {
    //<<<<<<<<<<<<<<<<<<<<<<<-STILL->>>>>>>>>>>>>>>>>>>>>>>>>>>>
    if (!moving) {
      shape.translate(pos.x, pos.y);
      shape(shape);
      shape.resetMatrix();
      drawDots(top, fw);
    }
    //<<<<<<<<<<<<<<<<<<<<<<<-MOVING->>>>>>>>>>>>>>>>>>>>>>>>>>>>
    else {
      r = float(mouseX)/float(width)*HALF_PI;
      
      shape.translate(pos.x, corner.y+(cos(r)-sin(r))*cs/2);
      shape.scale(1.0, sin(r)+cos(r));
      shape(shape);
      shape.resetMatrix();
      
      shape.translate(pos.x, corner.y+(cos(r)-sin(r)/2)*cs);
      shape.scale(1.0, r>0 ? sin(r) : 0.000000001);
      shape(shape);
      shape.resetMatrix();
      
      shape.translate(pos.x, corner.y+(cos(r)/2-sin(r))*cs);
      shape.scale(1.0, cos(r));
      shape(shape);
      shape.resetMatrix();
      
      p.set(pos.x, corner.y+(cos(r)/2-sin(r))*cs);
      s.set(cs, cos(r)*cs);
      drawDots(top, fw);
      
      p.set(pos.x, corner.y+(cos(r)-sin(r)/2)*cs);
      s.set(cs, sin(r)*cs);
      drawDots(getTopSide(top, fw, 0), getFwSide(top, fw, 0));
    }
  }
  //--------------------------------------------------------------------------------------
  
  int getTopSide (int top, int fw, int dir) { // dir: 0->N, 1->S, 2->W, 3->E
    if (king) return KING;
    if (dir < 0 || dir > 3) { println("Not aproppriate direction for cube", this); return -1; }
    return ( gettop[dir][top-1][fw-1] != 0 ? gettop[dir][top-1][fw-1] : directionWarning() );
  }
  
  int getFwSide (int top, int fw, int dir) {
    if (king) return KING;
    if (dir < 0 || dir > 3) { println("Not aproppriate direction for cube", this); return -1; }
    return ( getfw[dir][top-1][fw-1] != 0 ? getfw[dir][top-1][fw-1] : directionWarning() );
  }

  int directionWarning(){
    println("Top and forward side is equal!!! How???");
    return 0;
  }














  //------------------------------------------------
  //----------- don't touch it part ----------------
  //------------------------------------------------

  private void createCube() {
    shape = null;
    shape = createShape(PShape.PATH);
    shape.beginShape();
    if (col==RED) shape.fill(redcolor);
    else shape.fill(vanillacolor);
    shape.stroke(0);
    shape.strokeWeight(sw);
    if (cubedesign=="Aron") shape.vertex(-size.x/2*innerRate, -size.y/2);
    else shape.vertex(-size.x/2*curveWidthRate, -size.y/2);
    for (int i=0; i<4; ++i) {
      if (cubedesign == "Cool" || cubedesign == "Simple") {
        shape.vertex      (size.x/2*(i<2?1:-1)*(i%2==0?curveWidthRate:1), size.y/2*(i<1||i>2?-1:1)*(i%2==1?curveWidthRate:1));
        shape.bezierVertex(size.x/2*(i<2?1:-1)*(i%2==0?curveWidthRate:1), size.y/2*(i<1||i>2?-1:1)*(i%2==1?curveWidthRate:1), 
                           size.x/2*(i<2?1:-1)*curveRate,             size.y/2*(i<1||i>2?-1:1)*curveRate, 
                           size.x/2*(i<2?1:-1)*(i%2==1?curveWidthRate:1), size.y/2*(i<1||i>2?-1:1)*(i%2==0?curveWidthRate:1));
        shape.vertex(size.x/2*(i<2?1:-1)*(i%2==1?curveWidthRate:1), size.y/2*(i<1||i>2?-1:1)*(i%2==0?curveWidthRate:1));
      }
      if (cubedesign == "Aron") {
        shape.vertex(size.x/2*(i<2?1:-1)*(i%2==0?innerRate:1), size.y/2*(i<1||i>2?-1:1)*(i%2==1?innerRate:1));
        shape.vertex(size.x/2*(i<2?1:-1)*innerRate, size.y/2*(i<1||i>2?-1:1)*innerRate);
        shape.vertex(size.x/2*(i<2?1:-1)*(i%2==1?innerRate:1), size.y/2*(i<1||i>2?-1:1)*(i%2==0?innerRate:1));
      }
    }
    if (cubedesign == "Aron" || cubedesign == "Cool"){
      shape.vertex(-size.x/2*innerRate, -size.y/2*innerRate);
      for (int i=0; i<4; ++i) {
        shape.vertex(size.x/2*(i<2?1:-1)*innerRate, size.y/2*(i<1||i>2?-1:1)*innerRate);
        if (cubedesign == "Cool"){
          shape.vertex(size.x/2*(i<2?1:-1)*(i%2==1?curveWidthRate:1), size.y/2*(i<1||i>2?-1:1)*(i%2==0?curveWidthRate:1));
          shape.vertex(size.x/2*(i<2?1:-1)*innerRate, size.y/2*(i<1||i>2?-1:1)*innerRate);
        }
      }
    }
    shape.endShape();
  }

  private void drawDots(int top, int fw) {
    noStroke();
    if (col==RED) fill(vanillacolor);
    else fill(redcolor);
    if (top==1 || top==3 || top==5 || king) ellipse(p.x, p.y, s.x*dotrate, s.y*dotrate);
    if (top==2 && (fw==3||fw==4) || top==3 && fw!=3 && fw!=4 || top==4 || top==5 || top==6) {
      ellipse(p.x-s.x/4, p.y-s.y/4, s.x*dotrate, s.y*dotrate);
      ellipse(p.x+s.x/4, p.y+s.y/4, s.x*dotrate, s.y*dotrate);
    }
    if (top==2 && fw!=3 && fw!=4 || top==3 &&(fw==3||fw==4) || top==4 || top==5 || top==6) {
      ellipse(p.x+s.x/4, p.y-s.y/4, s.x*dotrate, s.y*dotrate);
      ellipse(p.x-s.x/4, p.y+s.y/4, s.x*dotrate, s.y*dotrate);
    }
    if (top==6 && (fw==3||fw==4)) {
      ellipse(p.x+s.x/4, p.y, s.x*dotrate, s.y*dotrate);
      ellipse(p.x-s.x/4, p.y, s.x*dotrate, s.y*dotrate);
    } else if (top==6) {
      ellipse(p.x, p.y+s.x/4, s.x*dotrate, s.y*dotrate);
      ellipse(p.x, p.y-s.x/4, s.x*dotrate, s.y*dotrate);
    }
    if (king) {
      ellipse(p.x+s.x/6, p.y, s.x*sdotrate, s.y*sdotrate);
      ellipse(p.x-s.x/6, p.y, s.x*sdotrate, s.y*sdotrate);
      ellipse(p.x, p.y+s.y/6, s.x*sdotrate, s.y*sdotrate);
      ellipse(p.x, p.y-s.y/6, s.x*sdotrate, s.y*sdotrate);
    }
  }
};
