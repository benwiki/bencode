class Slider {
  color sliderColor;
  float radius, sliderHeight, sliderWidth;
  float round = 8;
  int colorValue = 0;
  PVector start, end;
  PVector pos;
  
  Slider(float h, float w) {
    this.sliderHeight = h;
    this.sliderWidth = w;
    start = new PVector((width - w) / 2, h);
    end = new PVector(width - (width - w) / 2, h);
    pos = start.copy();
  };
  
  Slider setColor(color col) { this.sliderColor = col; return this; }
  Slider setRadius(float radius) { this.radius = radius; return this; }
  
  void setToMousePos() {
    if (mouseX < start.x) { pos.x = start.x; return; }
    if (mouseX > end.x) { pos.x = end.x; return; }
    this.pos.x = mouseX;
  }
  
  void draw() {
    colorValue = (int) map(this.pos.x, start.x, end.x, 0, 255);
    
    fill(255);
    rectMode(CORNERS);
    rect(start.x - round, start.y - round, end.x + round, end.y + round, round);
    fill(this.sliderColor);
    noStroke();
    rect(start.x - round, start.y - round, pos.x + round, pos.y + round, round);
    ellipse(pos.x, pos.y, radius, radius);
    fill(0);
    text(colorValue, pos.x, pos.y - 5);
  }
  
  boolean mouseOver() {
    return PVector.dist(mouse, this.pos) <= radius ||
           (mouseX >= (start.x - round) && mouseY >= (start.y - round) &&
            mouseX <= (end.x + round)   && mouseY <= (end.y + round)); 
  }
  
  int get() {
    return colorValue;
  }
}
