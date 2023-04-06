int up = 0, down = 0;
String word = "";
color colorb=255;

void keyPressed(){
  transmitting=true;
  switch (keyCode) {
    case KeyEvent.KEYCODE_VOLUME_UP:
      up = millis();
      colorb=color(255,0,0);
      break;
    case KeyEvent.KEYCODE_VOLUME_DOWN:
      colorb=color(0,0,255);
      down = millis();
      break;
  }
  spacetime=0;
  go=wordgo=true;
}

void keyReleased(){
  transmitting=false;
  switch (keyCode) {
    case KeyEvent.KEYCODE_VOLUME_UP:
      word += dotdash(millis()-up);
      colorb=color(255,100,100);
      break;
    case KeyEvent.KEYCODE_VOLUME_DOWN:
      word += dotdash(millis()-down);
      colorb=color(100,100,255);
      break;
  }
}
