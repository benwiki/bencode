
float buttonRadius;
Slider cyanSlider, magentaSlider, yellowSlider;
PVector mouse = new PVector();
InputHandler inputHandler = new InputHandler();
int colorFieldHeight;

void setup() {
  fullScreen();
  textSize(50);
  textAlign(CENTER, CENTER);
  
  colorFieldHeight = height * 3/4 / 2;
  
  buttonRadius = width / 10;
  cyanSlider = new Slider(height * 3/4 + height/4/4, width * 0.8)
    .setColor(color(0, 255, 255))
    .setRadius(buttonRadius);
  magentaSlider = new Slider(height * 3/4 + height/4/4 * 2, width * 0.8)
    .setColor(color(255, 0, 255))
    .setRadius(buttonRadius);
  yellowSlider = new Slider(height * 3/4 + height/4/4 * 3, width * 0.8)
    .setColor(color(255, 255, 0))
    .setRadius(buttonRadius);
    
  inputHandler.addSlider(cyanSlider);
  inputHandler.addSlider(magentaSlider);
  inputHandler.addSlider(yellowSlider);
}

void draw() {
  mouse.set(mouseX, mouseY);
  
  background(30);
  
  rectMode(CORNER);
  fill(cyanSlider.get(), magentaSlider.get(), yellowSlider.get());
  rect(0, 0, width, colorFieldHeight);
  fill(255 - cyanSlider.get(), 255 - magentaSlider.get(), 255 - yellowSlider.get());
  rect(0, colorFieldHeight, width, colorFieldHeight);
  
  cyanSlider.draw();
  magentaSlider.draw();
  yellowSlider.draw();
  
  inputHandler.handleMouse();
  inputHandler.updateSlider();
}