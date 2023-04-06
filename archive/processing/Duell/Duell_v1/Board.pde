
class Board {

  PVector pos;
  Cube[] vanillas = new Cube[9], reds = new Cube[9];

  Board () {
    pos  = new PVector(0, 0);
    if (height<width*8/9) cs = height/8*brate;
    else cs = width/9*brate;
    for (int i=0; i<9; ++i) {
      vanillas[i] = new Cube(i, bottomplayer==VANILLA? 7:0, VANILLA) . setSides(starting_sides[i], bottomplayer==VANILLA? 4:3);
      reds[i] = new Cube(i, bottomplayer==RED? 7:0, RED) . setSides(starting_sides[i], bottomplayer==RED? 4:3);
    }
  }

  void show () {
    lines();
    for (int i=0; i<9; ++i) {
      vanillas[i].show();
      reds[i].show();
    }
  }

  void resize () {
    if (height<width*8/9) cs = height/8*brate;
    else cs = width/9*brate;
    for (int i=0; i<9; ++i) {
      vanillas[i].resize();
      reds[i].resize();
    }
  }



















  private void lines() {
    stroke(60);
    strokeWeight(cs*(1-curveWidthRate)/2);
    for (int i=0; i<10; ++i) {
      line(width/2+(-4.5+i)*cs, height/2-4*cs, width/2+(-4.5+i)*cs, height/2+4*cs);
      if (i<9) line(width/2-4.5*cs, height/2+(-4+i)*cs, width/2+4.5*cs, height/2+(-4+i)*cs);
    }
    noStroke();
    fill(60);

    //for (int i=0; i<4; ++i) ellipse(width/2+4.5*cs*(i<2?1:-1)*0.999, height/2-4*cs*(i<1||i>2?1:-1)*0.999, cs*(1-rate2), cs*(1-rate2));
  }
};
