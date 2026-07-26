
PImage glass;

void setGlass(){
  fill(#99b3bd);//fill(#0AA3FF);
  rect(0, 0, width, height);
  glass = get();
  fill(255);
  rect(0, 0, width, height);
  fill(0);
  for (int i=-1; i<=1; ++i)
    for (int k=1; k<=3; ++k)
      ellipse(width/2+i*width/4, height-k*width/4, width/6, width/6);
  glass.mask(get());
}

void showGlass(){
  push();
  tint(255, 230);
  imageMode(CENTER);
  image(glass, width/2, height/2);
  noFill();
  stroke(255);
  strokeWeight(3);
  for (int i=-1; i<=1; ++i)
    for (int k=1; k<=3; ++k)
      ellipse(width/2+i*width/4, height-k*width/4, width/6, width/6);
  pop();
}
