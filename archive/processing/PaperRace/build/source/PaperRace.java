import processing.core.*; 
import processing.data.*; 
import processing.event.*; 
import processing.opengl.*; 

import java.util.HashMap; 
import java.util.ArrayList; 
import java.io.File; 
import java.io.BufferedReader; 
import java.io.PrintWriter; 
import java.io.InputStream; 
import java.io.OutputStream; 
import java.io.IOException; 

public class PaperRace extends PApplet {


Button test = new Button(new PVector(100,100), new PVector(100,100), "navi")
                  .setFillColor(color(0))
                  .setActiveFillColor(color(random(255), random(255), random(255)))
                  .setStrokeWeight(0);
Handler handler = new Handler();

ArrayList<Button> exe = new ArrayList<Button>();
ArrayList<Button> toexe = new ArrayList<Button>();

public void setup(){
  //fullScreen();
  
  handler.toexe(test);
  rectMode(CENTER);
}

public void draw(){
  background(255);
  handler.runall();
}

public void mouseReleased(){
  for (Button b: exe)
    if (b.mouseOver) b.press();
}

class AnimationHandler {
  AnimationHandler () {
    
  }
  
  public void run(){
  
  }
};

class Animation {
  Button master;
  String type;
  MovementHandler moha;
  
  Animation(Button button, String type){
    this.master=button;
    moha = new MovementHandler(this.master);
    this.type=type;
    check(type);
  }
  
  public void check (String type) {
    if (type == "popup") popup();
  }
  
  public void popup(){
    moha.add("setsize", "popset-1").setSize(PVector.mult(master.size, 2));
  }
};
class Button {
  MovementHandler moha = new MovementHandler(this);
  AnimationHandler aniha = new AnimationHandler();
  
  PVector pos = new PVector(width/2, width/2),
          size = new PVector(width/5, width/5, 5);
  boolean pressed=false, visible=true, active=true, empty=false, mouseOver=false;
  String type = "basic", shape = "rect";
  
  float rectEdge=size.x/5;
  
  int scolor=color(0), fcolor=color(200), ascolor=color(50), afcolor=color(255); //stroke & fill color, activated stroke & fill color
  float alpha=255; // opacity of button
  
  ///////////////////////
  Button(){empty=true;}
  ////////////////////////////////////////////////
  Button(PVector pos, PVector size, String type){
    this.pos.set(pos);
    this.size.set(size);
    this.type=type;
  }
  ////////////////////////////////////////////////
  
  //==========================================================================================
  public Button setType (String type) { this.type = type; return this; }
  public Button setPosition (float x, float y) { this.pos.set(x, y); return this; }
  public Button setSize (float w, float h) { this.size.x = w; this.size.y = h; return this; }
  public Button setStrokeWeight (float d) { this.size.z = d; return this; }
  public Button setRectEdge (float e) { this.rectEdge = e; return this; }
  public Button setShape (String shape) { this.shape = shape; return this; }
  
  public Button setActiveFillColor (int afcolor) { this.afcolor = afcolor; return this; }
  public Button setFillColor (int fcolor) { this.fcolor = fcolor; return this; }
  public Button setActiveStrokeColor (int ascolor) { this.ascolor = ascolor; return this; }
  public Button setStrokeColor (int scolor) { this.scolor = scolor; return this; }
  public Button setColors (int fcolor, int afcolor, int scolor, int ascolor) { this.fcolor = fcolor; this.scolor = scolor; this.afcolor = afcolor; this.ascolor = ascolor; return this; }
  public Button setNormalColors (int fcolor, int scolor) { this.fcolor = fcolor; this.scolor = scolor; return this; }
  public Button setActiveColors (int afcolor, int ascolor) { this.afcolor = afcolor; this.ascolor = ascolor; return this; }
  public Button setAlpha (int alpha) { this.alpha = alpha; return this; }
  //=========================================================================================
  
  public void show () {
    moha.run();
    aniha.run();
    
    mouseOver = isOver();
    if (alpha>0){
      if (mouseOver)fill(red(afcolor), green(afcolor), blue(afcolor), alpha(afcolor)*alpha/255);
      else fill(red(fcolor), green(fcolor), blue(fcolor), alpha(fcolor)*alpha/255);
    }
    else noFill();
    
    if (size.z>0){
      strokeWeight(size.z);
      if (mouseOver) stroke(red(ascolor), green(ascolor), blue(ascolor), alpha(ascolor)*alpha/255);
      else stroke(red(scolor), green(scolor), blue(scolor), alpha(scolor)*alpha/255);
    }
    else noStroke();
    
    rect(pos.x, pos.y, size.x, size.y, rectEdge);
  }
  //------------------------------------------------------------------------------------------
  public void press () { this.pressed=true; }
  //------------------------------------------------------------------------------------------------------------------
  
  public boolean isOver(){
    if (mouseX>pos.x-size.x/2 && mouseX<pos.x+size.x/2 && mouseY>pos.y-size.y/2 && mouseY<pos.y+size.y/2) return true;
    else return false;
  }
  //------------------------------------------------------------------------------------------------------------------
  
  public Button setSize(PVector change){
    moha.add("setsize", "popup").setSize(change);
    return this;
  }
  public Button setSize(PVector change, float time){
    change.z = time;
    return setSize(change);
  }
  //-----------------------------------------------------
}
class Handler{
  ////////////
  Handler(){}
  ////////////
  //----------------------------------------------------------
  
  public void runall(){
    for (Button b: toexe) exe.add(b); toexe.clear();
    for (Button button: exe){
      if (button.visible) button.show();
      if (button.pressed && button.active) command(button);
    } 
  }
  //--------------------------------------------------------------------------------------
  public void toexe (Button button) { toexe.add(button); }
  //--------------------------------------------------------------------------------------
  
  public void command(Button button){
    button.pressed=false;
    if (button.type.equals("navi")) navi();
  }
  // . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  public void navi () {
    println(exe.size());
    toexe( new Button(new PVector(random(0, width), random(0,height)), new PVector(0, 0), "navi")
               .setSize(new PVector(random(100, 200), random(100, 200), 300))
               .setFillColor(color(0))
               .setActiveFillColor(color(random(255), random(255), random(255)))
               .setStrokeWeight(0) );
  }
  // . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
}

class MovementHandler{
  //==========================================================
  ArrayList<Movement> movements = new ArrayList<Movement>();
  ArrayList<Movement> remove = new ArrayList<Movement>();
  Button master;
  ////////////////////
  MovementHandler (Button master) { this.master = master; }
  ////////////////////
  //--------------------------------------------------------------

  public Movement add (String type, String name) {
    movements.add(new Movement(this, type, name));
    return movements.get(movements.size()-1);
  }
  //-----------------------------------------------------------------

  public void run () {
    for (Movement r: remove) movements.remove(r); remove.clear();
    for (Movement m: movements) m.run();
  }
  //-----------------------------------------------------------------

  public Movement getByName (String name) {
    for (Movement m: movements)
      if (m.name.equals(name))
        return m;

    print("Nem található!!! Üres Movement-et adok.");
    return new Movement();
  }
  //-----------------------------------

  public void KILLME (Movement m) {
    remove.add(m);
  }
  //-----------------------------------
};

//#######################################################################################################

class Movement {
  MovementHandler moha;
  String type, name;
  float wholetime=0, pasttime=0;
  boolean firstrun=true, DONE=false, empty=false;

  PVector from = new PVector();
  ArrayList<PVector> to = new ArrayList<PVector>();
  int next=0;

  Timer timer = new Timer();
  Button master = new Button();
  //////////////////////////////////////////////////////////
  Movement(){empty=true;}
  //////////////////////////////////////////////////////////
  Movement (MovementHandler moha, String type, String name) {
    this.moha = moha;
    this.master = moha.master;
    this.type = type;
    this.name = name;
  }
  ///////////////////////////////////////////////////////////
  //-----------------------------------------------------------------------

  public Movement setDestination () {
    return this;
  }
  //-----------------------------------------------------------------------

  public Movement setSize(PVector resize){
    from.set(master.size);
    to.add(resize.copy());
    wholetime += resize.z;
    return this;
  }
  public Movement setSize(PVector resize, float time){
    resize.z = time;
    return setSize(resize);
  }
  //---------------------------------------------------------------------------------------------

  public void run () {
    if (firstrun) {timer.start(); firstrun=false;}
    else if (timer.get() >= wholetime) {timer.stop(); DONE=true; moha.KILLME(this);}
    else if (timer.get() >= pasttime+to.get(next).z) pasttime += to.get(next++).z;
    // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if (type=="setsize") runSetSize();
  }
  //.............................................................................................

  public void runSetSize () {
    if (!DONE) master.size.set(map( timer.get(), 0,to.get(next).z, from.x,to.get(next).x ),
                               map( timer.get(), 0,to.get(next).z, from.y,to.get(next).y ));
    else master.size.set(to.get(to.size()-1).x, to.get(to.size()-1).y);
  }
};

class Timer {
  float time;
  Timer(){}
  public void start(){
    time = millis();
  }
  public float get(){
    return millis()-time;
  }
  public void stop(){
    time=0;
  }
};
  public void settings() {  size(700, 1000); }
  static public void main(String[] passedArgs) {
    String[] appletArgs = new String[] { "PaperRace" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}
