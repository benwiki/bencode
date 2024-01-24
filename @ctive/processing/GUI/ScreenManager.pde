
abstract class Screen {
  ButtonManager buttonManager = new ButtonManager();
  
  Screen() {}
  
  abstract void run();

  void pressButton() { this.buttonManager.pressButton(); }
}
// ===================================================================7

class ScreenManager {
  ArrayList<Screen> screens = new ArrayList<Screen>();
  Screen activeScreen;

  ScreenManager() {}
  
  void add(Screen screen) {
    if (screens.size() == 0) this.activeScreen = screen;
    screens.add(screen);
  }
  
  void runActiveScreen() {
    this.activeScreen.run();
  }
  
  void pressButton() {
    activeScreen.pressButton();
  }
}
