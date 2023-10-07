class Button {
  MovementHandler moha = new MovementHandler(this);
  AnimationHandler aniha = new AnimationHandler();
  
  PVector pos = new PVector(width/2, width/2),
          size = new PVector(width/5, width/5, 5);
  boolean pressed=false, visible=true, active=true, empty=false, mouseOver=false;
  String type = "basic", shape = "rect";
  
  float rectEdge=size.x/5;
  
  color scolor=color(0), fcolor=color(200), ascolor=color(50), afcolor=color(255); //stroke & fill color, activated stroke & fill color
  float alpha=255; // opacity of button
  
  ///////////////////////
  Button(){}
  ////////////////////////////////////////////////
  Button(PVector pos, PVector size, String type){
    this.pos.set(pos);
    this.size.set(size);
    this.type=type;
  }
  ////////////////////////////////////////////////
  
  //==========================================================================================
  Button setType (String type) { this.type = type; return this; }
  Button setPosition (float x, float y) { this.pos.set(x, y); return this; }
  Button setSize (float w, float h) { this.size.x = w; this.size.y = h; return this; }
  Button setStrokeWeight (float d) { this.size.z = d; return this; }
  Button setRectEdge (float e) { this.rectEdge = e; return this; }
  Button setShape (String shape) { this.shape = shape; return this; }
  
  Button setActiveFillColor (color afcolor) { this.afcolor = afcolor; return this; }
  Button setFillColor (color fcolor) { this.fcolor = fcolor; return this; }
  Button setActiveStrokeColor (color ascolor) { this.ascolor = ascolor; return this; }
  Button setStrokeColor (color scolor) { this.scolor = scolor; return this; }
  Button setColors (color fcolor, color afcolor, color scolor, color ascolor) { this.fcolor = fcolor; this.scolor = scolor; this.afcolor = afcolor; this.ascolor = ascolor; return this; }
  Button setNormalColors (color fcolor, color scolor) { this.fcolor = fcolor; this.scolor = scolor; return this; }
  Button setActiveColors (color afcolor, color ascolor) { this.afcolor = afcolor; this.ascolor = ascolor; return this; }
  Button setAlpha (int alpha) { this.alpha = alpha; return this; }
  //=========================================================================================
  
  void show () {
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
  void press () { this.pressed=true; }
  //------------------------------------------------------------------------------------------------------------------
  
  boolean isOver(){
    if (mouseX>pos.x-size.x/2 && mouseX<pos.x+size.x/2 && mouseY>pos.y-size.y/2 && mouseY<pos.y+size.y/2) return true;
    else return false;
  }
  //------------------------------------------------------------------------------------------------------------------
  
  Button setSize(PVector change){
    moha.add("setsize", "popup").setSize(change);
    return this;
  }
  Button setSize(PVector change, float time){
    change.z = time;
    return setSize(change);
  }
  //-----------------------------------------------------
}
