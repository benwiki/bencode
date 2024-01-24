class ButtonManager {
  ArrayList<Button> buttons = new ArrayList<Button>(); 
  
  ButtonManager() {}
  
  void add(Button button) {
    buttons.add(button);
  }
  
  void run() {
    for (Button button: buttons) {
      drawButton(button);
    }
  }
  
  void drawButton(Button button) {
    boolean mouseOverButton = button.mouseOver();
    button.setHover(mouseOverButton);
    button.setActive(mouseOverButton && mousePressed);
    if (button.visible) button.draw();
  }
  
  void pressButton() {
    for (Button button: buttons)
      if (button.active && button.activated) {
        if (button.command != null) button.command.run();
        return;
      }
  }
}
