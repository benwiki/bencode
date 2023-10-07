
class Button {
  
  PVector pos = new PVector(width/2, height/2); // position
  
  float w=width/5, h=height/5, d=5;
  float rectEdge=w/5; // w, h: width, height | d: strokeWeight
  
  color scolor=color(0), fcolor=color(200), ascolor=color(50), afcolor=color(255); //stroke & fill color, activated stroke & fill color
  float alpha=maxalpha; // opacity of button
  
  String shape="rect", type="basic";
  
  SignsHandler signs = new SignsHandler();
  Movements movements = new Movements();
  
  boolean visible = true, activated = true, mouseOver = false, empty = false;
  
  boolean sizechange = false;
  int sizetime = 0, sizefix, cursizetime; // slidetime, fixed time, current time
  float fixw, fixh, scw, sch; // fix width, height; sizechange width, height
  
  //===================================================================================================
  
  Button () {
    empty = true;
  }
  
  //===================================================================================================
  
  Button (String type, float x, float y, float w, float h) {
    
    pos.set(x, y);
    
    this.type = type;
    this.w = w;
    this.h = h;
    rectEdge = w/5;
  }
  
  //===================================================================================================
  
  Button setType (String type) { this.type = type; return this; }
  Button setPosition (float x, float y) { this.pos.set(x, y); return this; }
  Button setSize (float w, float h) { this.w = w; this.h = h; rectEdge = w/5; return this; }
  Button setStrokeWeight (float d) { this.d = d; return this; }
  Button setRectEdge (float e) { this.rectEdge = e; return this; }
  Button setShape (String shape) { this.shape = shape; return this; }
  
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
  
  //-----------------------------------------------------------------
  
  void show(){
    movements.run();
    //---------------------------------------------------------------
    mouseOver = isOver();
    if (mouseOver)fill(red(afcolor), green(afcolor), blue(afcolor), alpha(afcolor)*alpha/255);
    else fill(red(fcolor), green(fcolor), blue(fcolor), alpha(fcolor)*alpha/255);
    if (mouseOver) stroke(red(ascolor), green(ascolor), blue(ascolor), alpha(ascolor)*alpha/255);
    else stroke(red(scolor), green(scolor), blue(scolor), alpha(scolor)*alpha/255);
    strokeWeight(d);
    
    if (shape=="rect" || shape=="rectangle"){
      rectMode(CENTER);
      rect(pos.x, pos.y, w, h, rectEdge);
    }
    else if(shape=="circle"||
      shape=="oval"||
      shape=="ellipse"){
      ellipse(pos.x, pos.y, w, h);
    }
    ///////////////////////
    signs.show();
    ///////////////////////
  }
  
  //-----------------------------------------------------------------
  
  Button jump (float x, float y) {
    this.pos.set(x, y);
    return this;
  }
  //-----------------------------------------------------------------
  
  Button activate () { this.activated = true; return this; }
  Button be_visible () { this.visible = true; return this; }
  
  Button deactivate () { this.activated = false; return this; }
  Button hide () { this.visible = false; return this; }
  
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
  
  //--------------------------------------------------------------
  
  Slide slide(){
    return movements.newSlide( this );
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
