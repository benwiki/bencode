interface ShapeButton {
  void drawForm();
  boolean mouseOver();
}

abstract class Command {
  String name;
  Button buttonToChange;
  Screen screenToChange;
    
  void setButtonToChange(Button button) { this.buttonToChange = button; }
  void setScreenToChange(Screen screen) { this.screenToChange = screen; }
  
  abstract void run();
}

// =======================================================================

class Button {
  color bgColor = color(0), fgColor = color(255), strokeColor = color(255);
  color hoverBgColor = color(255), hoverFgColor = color(0), hoverStrokeColor = color(0);
  color activeBgColor = color(220), activeFgColor = color(30), activeStrokeColor = color(30);
  boolean hover = false, active = false;
  boolean visible = true, activated = true;
  float borderRadius = 5, strokeWidth = 3;
  PVector topLeft, bottomRight;
  PVector pos, size, relTextPos = new PVector(0, -3);
  String text = "";
  int textSize = width / 25;
  int horizontalTextAlign = CENTER, verticalTextAlign = CENTER;
  Command command;
  
  Button() {}
  
  Button(PVector pos, PVector size) {
    this.pos = pos;
    this.size = size;
    this.topLeft = PVector.sub(pos, PVector.div(size, 2));
    this.bottomRight = PVector.add(pos, PVector.div(size, 2));
  }
  
  void draw() {
    drawForm();  
    drawText();
  }
  
  void drawForm() {
    fill(active ? activeBgColor : hover ? hoverBgColor : bgColor);
    stroke(active ? activeStrokeColor : hover ? hoverStrokeColor : strokeColor);
    strokeWeight(strokeWidth);
    rectMode(CENTER);
    rect(pos.x, pos.y, size.x, size.y, borderRadius);
  }
  
  void drawText() {
    fill(active ? activeFgColor : hover ? hoverFgColor : fgColor);
    textAlign(horizontalTextAlign, verticalTextAlign);
    textFont(createFont(/*"Tahoma Bold"*/"Arial", this.textSize));
    text(this.text, pos.x + relTextPos.x, pos.y + relTextPos.y);
  }
  
  boolean mouseOver() {
    return (mouseX >= topLeft.x     && mouseY >= topLeft.y &&
            mouseX <= bottomRight.x && mouseY <= bottomRight.y);
  }
  
  Button setBackgroundColor(color col) { this.bgColor = col; return this; }
  Button setForegroundColor(color col) { this.fgColor = col; return this; }
  Button setStrokeColor(color col) { this.strokeColor = col; return this; }
  Button setColors(color bg, color fg, color stroke) {
    this.setBackgroundColor(bg);
    this.setForegroundColor(fg);
    this.setStrokeColor(stroke);
    return this;
  }
  Button setHoverBackgroundColor(color col) { this.hoverBgColor = col; return this; }
  Button setHoverForegroundColor(color col) { this.hoverFgColor = col; return this; }
  Button setHoverStrokeColor(color col) { this.hoverStrokeColor = col; return this; }
  Button setHoverColors(color bg, color fg, color stroke) {
    this.setHoverBackgroundColor(bg);
    this.setHoverForegroundColor(fg);
    this.setHoverStrokeColor(stroke);
    return this;
  }
  Button setActiveBackgroundColor(color col) { this.activeBgColor = col; return this; }
  Button setActiveForegroundColor(color col) { this.activeFgColor = col; return this; }
  Button setActiveStrokeColor(color col) { this.activeStrokeColor = col; return this; }
  Button setActiveColors(color bg, color fg, color stroke) {
    this.setActiveBackgroundColor(bg);
    this.setActiveForegroundColor(fg);
    this.setActiveStrokeColor(stroke);
    return this;
  }
  Button setBackgroundColors(color normal, color hover, color active) {
    this.setBackgroundColor(normal);
    this.setHoverBackgroundColor(hover);
    this.setActiveBackgroundColor(active);
    return this;
  }
  Button setForegroundColors(color normal, color hover, color active) {
    this.setForegroundColor(normal);
    this.setHoverForegroundColor(hover);
    this.setActiveForegroundColor(active);
    return this;
  }
  Button setStrokeColors(color normal, color hover, color active) {
    this.setStrokeColor(normal);
    this.setHoverStrokeColor(hover);
    this.setActiveStrokeColor(active);
    return this;
  }
  Button setAllColors(color col) {
    this.setColors(col, col, col);
    this.setHoverColors(col, col, col);
    this.setActiveColors(col, col, col);
    return this;
  }
  Button setBorderRadius(float radius) { this.borderRadius = radius; return this; }
  Button setStrokeWidth(float strokeWidth) { this.strokeWidth = strokeWidth; return this; }
  Button setText(String text) {this.text = text; return this; }
  Button setTextSize(int textSize) {this.textSize = textSize; return this; }
  Button setHorizontalTextAlign(int textAlign) { this.horizontalTextAlign = textAlign; return this; }
  Button setVerticalTextAlign(int textAlign) { this.verticalTextAlign = textAlign; return this; }
  Button centerText() {
    this.setHorizontalTextAlign(CENTER);
    this.setVerticalTextAlign(CENTER);
    return this;
  }
  Button setRelativeTextPosition(PVector relTextPos) { this.relTextPos = relTextPos; return this; }
  Button setCommand(Command command) { this.command = command; return this; }
  void setHover(boolean hover) { this.hover = hover; }
  void setActive(boolean active) { this.active = active; }
  Button setVisible(boolean visible) { this.visible = visible; return this; }
  Button setActivated(boolean activated) { this.activated = activated; return this; }
}

// --------------------------------------------------------------------

class CircleButton extends Button implements ShapeButton {
  float radius;
  
  CircleButton(PVector pos, float radius) {
    super();
    this.pos = pos;
    this.radius = radius;
  }
  
  void drawForm() {
    fill(active ? activeBgColor : hover ? hoverBgColor : bgColor);
    stroke(active ? activeStrokeColor : hover ? hoverStrokeColor : strokeColor);
    strokeWeight(strokeWidth);
    ellipse(pos.x, pos.y, radius*2, radius*2);
  }
  
  boolean mouseOver() {
    return PVector.dist(mouse, this.pos) <= radius;
  }
}

// =======================================================================

class Label extends Button {
  Label(String text, PVector pos, PVector size) {
    super(pos, size);
    this.text = text;
    this.pos = pos;
    this.size = size;
    this.setAllColors(BG_COLOR);
    this.setColor(color(0));
    this.setActivated(false);
  }
  
  Label setColor(color col) { this.setForegroundColors(col, col, col); return this; }
  Label setAllBackgroundColors(color col) { this.setBackgroundColors(col, col, col); return this; }
  Label setAllStrokeColors(color col) { this.setStrokeColors(col, col, col); return this; }
}
