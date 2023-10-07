class Button{
  PVector pos, fpos, ffpos; //position, fixed position (because of sliding), fucking fixed position (because of bounding)
  PVector rpos; // relative position
  ArrayList<Button> bound; // bound buttons
  
  float w, h, d; // w, h: width, height | d: strokeWeight
  
  color scolor, fcolor, ascolor, afcolor; //stroke & fill color, activated stroke & fill color
  float alpha; // opacity of button
  color sign_col, sign_acol; // sign color, sign color when button is activated 
  
  String shape="", sign="", type="";
  boolean visible = false, activated = false, mouseOver = false, pressed = false;
  boolean bound_sup_pos=false, bound_inf_pos=false, bound_pos;
  
  boolean sliding = false, aas=false, has=false, sizechange = false; // do we slide?, activate after slide, hide after slide
  int stime = 0, fix, curtime, sizetime = 0, sizefix, cursizetime; // slidetime, fixed time, current time
  float fixw, fixh, scw, sch; // fix width, height; sizechange width, height
  
  PVector dest, acc, vel, diff; // slide destination, acceleration, velocity, and the difference between position, and desination.
  String mode;
  
  Player pmaster = new Player();
  Disk dmaster = new Disk();
  Aim amaster = new Aim();
  PImage disk;
  
  //========
  Button(){}
  //========
  
  Button(String type, float x, float y, float w, float h, float d, color scolor, color fcolor, color ascolor, color afcolor, float alpha, String shape){
    this.type = type;
    
    pos = new PVector(x, y);
    fpos = new PVector(x, y);
    ffpos = new PVector(x, y);
    rpos = new PVector();
    
    dest = new PVector(0, 0);
    acc = new PVector(0, 0);
    diff = new PVector(0, 0);
    vel = new PVector(0, 0);
    
    this.w = w;
    this.h = h;
    this.d = d;
    this.scolor = scolor;
    this.fcolor = fcolor;
    this.afcolor = afcolor;
    this.ascolor = ascolor;
    this.alpha = alpha;
    this.shape = shape.toLowerCase();
    //if(shape=="disk") disk = new Disk(pos, board.cs/5, fcolor);
    if(shape=="disk"){
      /*
      if (fcolor == 3) disk = loadImage("gold_disk.png");
      else if (fcolor == 2) disk = loadImage("silver_disk.png");
      else disk = loadImage("gray_disk.png");
      disk.resize(board.cs, board.cs);*/
    }
    
    bound = new ArrayList<Button>();
  }
  
  //-----------------------------------------------------------------
  
  void show(){
    //---------------------------------------------------------------
    if (bound_pos) rpos.set(pos);
    //===============================================================
    if (sliding) do_slide();
    if (sizechange) change_size();
    //===============================================================
    if (bound_pos){
      for (Button button: bound){
        if (button.sliding) button.fpos.add(PVector.sub(pos, rpos));
        else button.pos.add(PVector.sub(pos, rpos));
      }
    }
    //---------------------------------------------------------------
    mouseOver = isOver();
    if (shape=="rect" || shape=="rectangle"){
      if (mouseOver) fill(afcolor, alpha);
      else fill(fcolor, alpha);
      if (mouseOver) stroke(ascolor, alpha);
      else stroke(scolor, alpha);
      strokeWeight(d);
      rectMode(CENTER);
      rect(pos.x, pos.y, w, h, w/5);
    }
    else if(shape=="circle"||
      shape=="oval"||
      shape=="ellipse"){
      if (mouseOver)fill(afcolor, alpha);
      else fill(fcolor, alpha);
      if (mouseOver) stroke(ascolor, alpha);
      else stroke(scolor, alpha);
      strokeWeight(d);
      ellipse(pos.x, pos.y, w, h);
    }
    else if(shape=="disk"){
      if (fcolor==3) fill(255,255,0);
      else if(fcolor==2) fill(230);
      else fill(110);
      ellipse(pos.x, pos.y, w, h);
      //image(disk, pos.x-w/2, pos.y-w/2, w, h);
    }
    show_sign(mouseOver);
  }
  
  //-----------------------------------------------------------------
  
  void activate(){
    this.activated = true;
  }
  void be_visible(){
    this.visible = true;
  }
  
  void deactivate(){
    this.activated = false;
    this.aas = false;
  }
  void hide(){
    this.visible = false;
  }
  
  //-----------------------------------------------------------------
  
  boolean isOver(){
    if(
      shape=="circle"||
      shape=="oval"||
      shape=="ellipse")
          return sqrt(pow(mouseX-pos.x,2)+pow(mouseY-pos.y,2))<=w/2;
    else 
          return mouseX > pos.x-w/2 && mouseX < pos.x+w/2 && mouseY > pos.y-h/2 && mouseY < pos.y+h/2;
  }
  
  //-----------------------------------------------------------------
  
  void add_sign(String sign){
    this.sign = sign.toLowerCase();
    if(
      sign=="plus"||
      sign=="dot"||
      sign=="arrow")
        sign_col = sign_acol = 255;
    else if(sign=="x")
        sign_col = color(255,150,150);
  }
  //-----------------------------------------------------------------
  
  void show_sign(boolean mouseOver){
    if (sign.length() > 0){
      if (mouseOver) {stroke(sign_acol); fill(sign_acol);}
      else {stroke(sign_col); fill(sign_col);}
      if(sign=="plus"){
          strokeWeight(d);
          line(pos.x-w/2+w/5, pos.y, pos.x+w/2-w/5, pos.y);
          line(pos.x, pos.y-h/2+h/5, pos.x, pos.y+h/2-h/5);
}
          
      if(sign=="dot"){
          strokeWeight(d);
          ellipse(pos.x, pos.y, h/5, h/5);
}
          
      if(sign=="arrow"){
          strokeWeight(d);
          line(pos.x-w/2+w/3, pos.y, pos.x+w/2-w/3, pos.y);
          line(pos.x, pos.y-h/4, pos.x+w/2-w/3, pos.y);
          line(pos.x, pos.y+h/4, pos.x+w/2-w/3, pos.y);
}
          
       if(sign=="x"){
          strokeWeight(d);
          line(pos.x+cos(135.0/360.0*TWO_PI)*w/2, pos.y+sin(135.0/360.0*TWO_PI)*w/2, pos.x+cos(-45.0/360.0*TWO_PI)*w/2, pos.y+sin(-45.0/360.0*TWO_PI)*w/2);
          line(pos.x+cos(45.0/360.0*TWO_PI)*w/2, pos.y+sin(45.0/360.0*TWO_PI)*w/2, pos.x+cos(-135.0/360.0*TWO_PI)*w/2, pos.y+sin(-135.0/360.0*TWO_PI)*w/2);
}
    }
  }
  //--------------------------------------------------------------
  
  void slide(float x, float y, int milliseconds, String mode){
    //=============
    dest.set(x, y);
    /////////////////////////////
    if (dest.equals(pos)) return;
    /////////////////////////////
    this.mode = mode.toLowerCase();
    sliding = true;
    stime = milliseconds;
    diff.set(PVector.sub(dest, pos));
    fpos.set(pos);
    ffpos.set(pos);
    
    if(mode=="half"){
        acc.set(2*diff.x/pow(stime, 2), 2*diff.y/pow(stime, 2));
        vel.set(acc.x*stime, acc.y*stime);
}
    if(mode=="whole"){
        acc.set(diff.x/pow(stime/2, 2), diff.y/pow(stime/2, 2));
        vel.set(acc.x*stime, acc.y*stime);
}
    if(mode=="normal")
        vel.set(diff.x/stime, diff.y/stime);
    fix = millis();
  }
  
  //-----------------------------------------------------------------------
  
  void do_slide(){
    if (millis()-fix < stime){
      curtime = millis()-fix;
      if(mode=="half"){
          pos.x = fpos.x + vel.x*curtime - acc.x/2*pow(curtime, 2);
          pos.y = fpos.y + vel.y*curtime - acc.y/2*pow(curtime, 2);
}
      if(mode=="whole"){
          if(curtime < stime/2){
            pos.x = fpos.x + acc.x/2*pow(curtime, 2);
            pos.y = fpos.y + acc.y/2*pow(curtime, 2); }
          else {
            pos.x = fpos.x + diff.x/2 + vel.x*(curtime-stime/2)/2 - acc.x/2*pow((curtime-stime/2), 2);
            pos.y = fpos.y + diff.y/2 + vel.y*(curtime-stime/2)/2 - acc.y/2*pow((curtime-stime/2), 2); }
}
      if(mode=="normal")
          pos.set(fpos.x + vel.x*curtime, fpos.y + vel.y*curtime);
    }
    else {
      pos.set(dest.add(PVector.sub(fpos, ffpos)));
      sliding = false;
      if (aas) {activate(); aas = false;}
      if (has) {hide(); has = false;}
      if (pmaster.eliminated) {pmaster.do_suicide(); pmaster.deleted=true;}
    }
  }
  
  //----------------------------------------------------------------------
  
  void activate_after_slide(){
    aas = true;
  }
  //----------------------------------------------------------------------
  
  void bind_pos(Button button){
    button.bound.add(this);
    button.bound_pos = true;
  }
  //----------------------------------------------------------------------
  
  void set_size(float rel_w, float rel_h, int milliseconds){
    sizechange = true;
    scw = rel_w;
    sch = rel_h;
    fixw = this.w;
    fixh = this.h;
    sizetime = milliseconds;
    sizefix = millis();
  }
  //----------------------------------------------------------------------
  
  void change_size(){
    /*if (millis()-sizefix < sizetime){
      cursizetime = millis()-sizefix;
      w = int(map(cursizetime, 0, sizetime, fixw, fixw*scw));
      h = int(map(cursizetime, 0, sizetime, fixh, fixw*sch));
    }
    else{
      sizechange = false;
      w = int(fixw*scw);
      h = int(fixh*sch);
    }*/
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
  
  void set_size_by_value(float new_w, float new_h, int milliseconds){
    sizechange = true;
    scw = new_w;
    sch = new_h;
    fixw = this.w;
    fixh = this.h;
    sizetime = milliseconds;
    sizefix = millis();
  }
  //----------------------------------------------------------------------
  
  void change_color(color col){
    scolor = color(col);
    fcolor = color(col); 
    ascolor = color(col, 120);
    afcolor = color(col, 120);
  }
}
