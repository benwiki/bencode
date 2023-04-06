float tangle (PVector v1, PVector v2) {
  return PI-atan2(v2.y-v1.y, v1.x-v2.x);
}
PVector mouse = new PVector();
void draw(){
  background(0);
  circle(mouseX, mouseY, 5);
  circle(50, 50, 5);
  if (mouseX != mouse.x || mouseY != mouse.y) mouse.set(mouseX, mouseY);
  println(tangle(new PVector(50, 50), mouse));
}
