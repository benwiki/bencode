import android.view.KeyEvent;

boolean transmitting = false, go=false, wordgo=false;
int spacetime=0;
String realword="";

void setup(){
  fullScreen();
  textAlign(CENTER, CENTER);
}

void draw(){
  if (realword.length()>0) textFont(createFont("Sans Helvetica", width/realword.length()));
  else textFont(createFont("Sans Helvetica", width));
  if (!transmitting) {
    if (spacetime==0) spacetime=millis();
    else if (go && millis()-spacetime > space && millis()-spacetime <= wordspace){
      go=false;
      realword+=letter(word);
      word="";
    }
    else if (wordgo && millis()-spacetime > wordspace){
      wordgo=false;
      realword+=" ";
      spacetime=-1;
    }
  }
  background(colorb);
  fill(0);
  text(word, width/2, height/4);
  text(realword, width/2, height/2);
}
