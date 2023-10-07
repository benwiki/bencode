
class Button{
  
  PVector pos = new PVector(0, 0); // position
  
  float w, h, d=5; // w, h: width, height | d: strokeWeight
  
  color scolor=color(0), fcolor=color(200), ascolor=color(50), afcolor=color(255); //stroke & fill color, activated stroke & fill color
  float alpha=maxalpha; // opacity of button
  int arrowDir = -1;
  
  String shape="rect", type="";
  SignsHandler signs = new SignsHandler();
  Movements movements = new Movements();
  
  boolean visible = true, activated = true, mouseOver = false, pressed = false, empty = false;
  
  Button safterwho;
  boolean sliding = false, sizechange = false;
  int sizetime = 0, sizefix, cursizetime; // slidetime, fixed time, current time
  float fixw, fixh, scw, sch; // fix width, height; sizechange width, height
  ArrayList<PVector> slide_backlog = new ArrayList<PVector>();
  
   // slide destination, acceleration, velocity, and the difference between position, and desination.
  String mode;
  
  PImage disk;
  
  //========
  Button(){
    empty = true;
  }
  //====================================
  
  Button(String type, float x, float y, float w, float h){
    
    pos.set(x, y);
    
    this.type = type;
    this.w = w;
    this.h = h;
    this.shape = shape.toLowerCase();
  }
  
  //=====================================
  
  Button setStrokeWeight (int d) { this.d = d; return this; }
  Button setActiveFillColor (color afcolor) { this.afcolor = afcolor; return this; }
  Button setFillColor (color fcolor) { this.fcolor = fcolor; return this; }
  Button setActiveStrokeColor (color ascolor) { this.ascolor = ascolor; return this; }
  Button setStrokeColor (color scolor) { this.scolor = scolor; return this; }
  Button setColors (color fcolor, color afcolor, color scolor, color ascolor) {
    this.fcolor = fcolor;
    this.scolor = scolor; 
    this.afcolor = afcolor;
    this.ascolor = ascolor;
    return this;
  }
  Button setNormalColors (color fcolor, color scolor) {
    this.fcolor = fcolor;
    this.scolor = scolor; 
    return this;
  }
  Button setActiveColors (color afcolor, color ascolor) {
    this.afcolor = afcolor;
    this.ascolor = ascolor;
    return this;
  }
  Button setAlpha (int alpha) { this.alpha = alpha; return this; }
  Button setShape (String shape) { this.shape = shape; return this; }
  
  //-----------------------------------------------------------------
  
  void show(){
    push();
    //===============================================================
    /*if (sliding) do_slide();
    else if (slide_backlog.size()>0){
      if (slide_backlog.get(0).z < 0) // if "z" is negative, it is "half" slide. Not the best, I know... I will create a "slide" class as well.
        slide(slide_backlog.get(0).x, slide_backlog.get(0).y, abs(int(slide_backlog.get(0).z)), "half");
      else 
        slide(slide_backlog.get(0).x, slide_backlog.get(0).y, int(slide_backlog.get(0).z), "whole");
      slide_backlog.remove(0);
    }
    if (sizechange) change_size();*/
    if (movements.isMoving()) movements.runAll();
    //---------------------------------------------------------------
    mouseOver = isOver();
    if (mouseOver)fill(red(afcolor), green(afcolor), blue(afcolor), alpha(afcolor)*alpha/255);
    else fill(red(fcolor), green(fcolor), blue(fcolor), alpha(fcolor)*alpha/255);
    if (mouseOver) stroke(red(ascolor), green(ascolor), blue(ascolor), alpha(ascolor)*alpha/255);
    else stroke(red(scolor), green(scolor), blue(scolor), alpha(scolor)*alpha/255);
    strokeWeight(d);
    
    if (shape=="rect" || shape=="rectangle"){
      rectMode(CENTER);
      rect(pos.x, pos.y, w, h, w/5);
    }
    else if(shape=="circle"||
      shape=="oval"||
      shape=="ellipse"){
      ellipse(pos.x, pos.y, w, h);
    }
    
    showSigns();
    pop();
  }
  
  //-----------------------------------------------------------------
  
  Button jump (int x, int y) {
    this.pos.set(x, y);
    return this;
  }
  //----------------------------------------
  
  Button activate(){
    this.activated = true;
    return this;
  }
  Button be_visible(){
    this.visible = true;
    return this;
  }
  
  Button deactivate(){
    this.activated = false;
    return this;
  }
  Button hide(){
    this.visible = false;
    return this;
  }
  
  //-----------------------------------------------------------------
  
  boolean isOver(){
    if (empty) return false;
    //if (mouseBlock) return false;
    if(shape=="circle"||
      shape=="oval"||
      shape=="ellipse")
      return sqrt(pow(mouseX-pos.x,2)+pow(mouseY-pos.y,2))<=w/2;
    else 
      return mouseX > pos.x-w/2 && mouseX < pos.x+w/2 && mouseY > pos.y-h/2 && mouseY < pos.y+h/2;
  }
  
  //-----------------------------------------------------------------
  
  
  Sign addSign(String signType, String signName){
    return signs.addNew( this ).setType(signType).setName(signName);
  }
  
  Sign addSign(){
    return signs.addNew( this );
  }
  
  Sign getSignByName (String name) {
    return signs.getByName(name);
  }

  void showSigns(){
    signs.show();
  }
  //--------------------------------------------------------------
  
  Slide slide(){
    return movements.newSlide(this);
  }
  
  //----------------------------------------------------------------------
  
  Button setSize(float new_w, float new_h, int milliseconds){
    if (this.w == new_w && this.h == new_h) return this;
    sizechange = true;
    scw = new_w;
    sch = new_h;
    fixw = this.w;
    fixh = this.h;
    sizetime = milliseconds;
    sizefix = millis();
    return this;
  }
  //----------------------------------------------------------------------
  
  void change_size(){
    if (millis()-sizefix < sizetime){
      cursizetime = millis()-sizefix;
      w = int(map(cursizetime, 0, sizetime, fixw, scw));
      h = int(map(cursizetime, 0, sizetime, fixh, sch));
    }
    else{
      sizechange = false;
      w = int(scw);
      h = int(sch);
    }
  }
  //----------------------------------------------------------------------
  
}
