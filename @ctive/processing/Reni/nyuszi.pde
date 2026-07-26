void nyuszi(int x, int y) {
  // törzs
  ellipse(x, y, 30, 40);
  // láb 1
  ellipse(x-10, y+20, 10, 20);
  // láb 2
  ellipse(x+10, y+20, 10, 20);
  // fej
  ellipse(x, y-32, 25, 25);
  // kéz 1
  ellipse(x-20, y-20, 30, 10);
  // kéz 2
  ellipse(x+20, y-20, 30, 10);
  
  // fül 1
  pushMatrix();
  translate(x+20, y-50);
  rotate(-PI / 4);
  ellipse(0, 0, 30, 10);
  popMatrix();
  
  // fül 2
  pushMatrix();
  translate(x-20, y-50);
  rotate(PI / 4);
  ellipse(0, 0, 30, 10);
  popMatrix();
}
