class GongScreen extends Screen {  
  int gongSeconds = 10, gongTime = -10000;
  Button gongSecondsLabel, controlGongButton;
  boolean gongPlaying = false;
  SoundFile gong;

  GongScreen() {
    super();
    this.setup();
  }
  
  void setup() {
    gong = new SoundFile(app, "gong_short.wav");

    float buttonRadius = width / 16;
  
    buttonManager.add(new Label("Verneigung",
      new PVector(width/2, height/15), new PVector(0, 0))
      .setTextSize(width / 10));
    
    buttonManager.add(new Label("Gong-Intervall:",
      new PVector(width/4, height/5), new PVector(width*2/5, buttonRadius))
      //.setHorizontalTextAlign(RIGHT)
      .setTextSize(width / 20));
    buttonManager.add(new Label("Sek.",
      new PVector(width/2, height*19/80), new PVector(width*2/5, buttonRadius)));
    
    gongSecondsLabel = new Label(str(gongSeconds),
      new PVector(width/2, height/5), new PVector(width/2, buttonRadius))
      .setAllBackgroundColors(color(0, 1))
      .setAllStrokeColors(color(0, 1))
      .setTextSize(width / 10);
    buttonManager.add(gongSecondsLabel);
  
    buttonManager.add(new CircleButton(new PVector(width*4/6, height/5), buttonRadius)
      .setText("+").setCommand(new Increment(gongSecondsLabel)).setTextSize(width/10));
  
    buttonManager.add(new CircleButton(new PVector(width*5/6, height/5), buttonRadius)
      .setText("-").setCommand(new Decrement(gongSecondsLabel)).setTextSize(width/8)
      .setRelativeTextPosition(new PVector(0, -8)));
    
    controlGongButton = new Button(new PVector(width/2, height*3/10), new PVector(width/2, buttonRadius*1.5))
      .setText("Start Gong").setBorderRadius(width / 30).setTextSize(width / 20);
    controlGongButton.setCommand(new ControlGong(this, controlGongButton));
    buttonManager.add(controlGongButton);
  }
  
  void run() {
    buttonManager.run();
    
    if (gongPlaying && millis() - gongTime >= int(gongSecondsLabel.text) * 1000) {
      gong.play();
      gongTime = millis();
    }
  }
  
  void setGong(boolean playing) { this.gongPlaying = playing; }
}

class Increment extends Command {
  Increment(Button button) { this.buttonToChange = button; }
  
  void run() {
    if (int(buttonToChange.text) >= 99) return;
    buttonToChange.setText(str(int(buttonToChange.text) + 1));
  }
}

class Decrement extends Command {
  Decrement(Button button) { this.buttonToChange = button; }
  
  void run() {
    if (int(buttonToChange.text) <= 1) return;
    buttonToChange.setText(str(int(buttonToChange.text) - 1));
  }
}

class ControlGong extends Command {
  GongScreen screenToChange;
  ControlGong(GongScreen screen, Button button) {
    this.screenToChange = screen;
    this.buttonToChange = button;
  }
  
  void run() {
    if (buttonToChange.text == "Start Gong") {
      buttonToChange.setText("STOP Gong");
      screenToChange.setGong(true);
    } else {
      buttonToChange.setText("Start Gong");
      screenToChange.setGong(false);
    }
  }
}
