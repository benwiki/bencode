
class Button{
  
  PVector pos = new PVector(0, 0); // position
  PVector fpos = new PVector(0, 0); // fixed position (because of sliding), 
  PVector ffpos = new PVector(0, 0); // fucking fixed position (because of bounding)
  PVector rpos = new PVector(0, 0); // relative position
  
  ArrayList<Button> bound = new ArrayList<Button>();; // bound buttons
  boolean bound_pos = false;
  
  float w, h, d; // w, h: width, height | d: strokeWeight
  
  color scolor, fcolor, ascolor, afcolor; //stroke & fill color, activated stroke & fill color
  float alpha; // opacity of button
  int arrowDir = -1;
  
  String shape="", type="";
  ArrayList<Sign> signs = new ArrayList<Sign>();
  
  boolean visible = false, activated = false, mouseOver = false, pressed = false, empty = false;
  
  Button safterwho;
  boolean sliding = false, aas=false, has=false, pas = false, sizechange = false, sasc = false, safter = false; 
  // do we slide?, activate after slide, hide after slide, place after slide, do we change size?, suicide after sizechange, suicide after someone's suicide
  int sascas = -1;
  int stime = 0, fix, curtime, sizetime = 0, sizefix, cursizetime; // slidetime, fixed time, current time
  float fixw, fixh, scw, sch; // fix width, height; sizechange width, height
  ArrayList<PVector> slide_backlog = new ArrayList<PVector>();
  
  PVector dest = new PVector(0, 0);
  PVector acc = new PVector(0, 0);
  PVector diff = new PVector(0, 0);
  PVector vel = new PVector(0, 0); // slide destination, acceleration, velocity, and the difference between position, and desination.
  String mode;
  
  Player pmaster = emptyPlayer;
  Disk dmaster = emptyDisk;
  Aim amaster = emptyAim;
  
  PImage disk;
  
  //========
  Button(){
    empty = true;
  }
  //========
  
  Button(String type, float x, float y, float w, float h, float d, color scolor, color fcolor, color ascolor, color afcolor, float alpha, String shape){
    
    this.type = type;
    
    pos.set(x, y);
    fpos.set(x, y);
    ffpos.set(x, y);
    
    this.w = w;
    this.h = h;
    this.d = d;
    this.scolor = scolor;
    this.ascolor = ascolor;
    this.fcolor = fcolor;
    this.afcolor = afcolor;
    this.alpha = alpha;
    this.shape = shape.toLowerCase();
    
    if(shape=="disk" && gamemode == "desktop"){
      if (fcolor == 3) disk = loadImage("gold_disk.png");
      else if (fcolor == 2) disk = loadImage("silver_disk.png");
      else disk = loadImage("gray_disk.png");
      disk.resize(board.cs, board.cs);
    }
    pmaster = emptyPlayer;
    dmaster = emptyDisk;
    amaster = emptyAim;
    safterwho = emptyButton;
  }
  
  //-----------------------------------------------------------------
  
  void show(){
    //---------------------------------------------------------------
    if (bound_pos) rpos.set(pos);
    //===============================================================
    if (sliding) do_slide();
    else if (slide_backlog.size()>0){
      if (slide_backlog.get(0).z < 0) // if "z" is negative, it is "half" slide. Not the best, I know... I will create a "slide" class as well.
        slide(slide_backlog.get(0).x, slide_backlog.get(0).y, abs(int(slide_backlog.get(0).z)), "half");
      else 
        slide(slide_backlog.get(0).x, slide_backlog.get(0).y, int(slide_backlog.get(0).z), "whole");
      slide_backlog.remove(0);
    }
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
    else if(shape=="disk"){
      tint(255, alpha);
      if (gamemode=="desktop")
        image(disk, pos.x-w/2, pos.y-w/2, w, h);
      else {
        if (fcolor==3) fill(255,255,0);
        else if(fcolor==2) fill(230);
        else fill(110);
        ellipse(pos.x, pos.y, w, h);
      }
    }
    
    show_signs();
    
    if (safter && (!safterwho.visible || !safterwho.activated))
      removeFromExe.add(this);
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
  
  
  void add_sign(String sign){
    this.signs.add( new Sign( sign.toLowerCase(), this ) );
    if(sign=="plus"||
      sign=="dot"||
      sign=="arrow")
        signs.get(signs.size()-1).setColors(255, 255);
    else if(sign=="x")
        signs.get(signs.size()-1).setColors(color(255,150,150), color(255, 0, 0));
  }
  
  void add_sign(String sign, String text, PVector textvector){
    textFont(createFont("Century Gothic Félkövér", 20));
    this.signs.add( new Sign( sign.toLowerCase(), text, textvector, this ) );
    signs.get(signs.size()-1).setColors(color(255), color(255));
  }
  
  void add_sign(String sign, int dir){
    this.signs.add( new Sign( sign.toLowerCase(), this ) );
    signs.get(signs.size()-1).setColors(game.po_color, color(red(game.po_color), green(game.po_color), blue(game.po_color), maxalpha*0.7));
    this.arrowDir = dir;
  }
  //-----------------------------------------------------------------
  
  void show_signs(){
    if (signs.size() > 0)
      for (Sign sign: signs)
        sign.show();
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
      if (pas) {pmaster.placed = true;}
      if (pmaster.eliminated) {pmaster.do_suicide(); pmaster.deleted=true;}
      if (sascas==0) ++sascas;
      else if (sascas==1) removeFromExe.add(this);
    }
  }
  
  //----------------------------------------------------------------------
  void activate_after_slide(){aas = true;}
  //----------------------------------------------------------------------
  void hide_after_slide(){has = true;}
  //----------------------------------------------------------------------
  void suicide_after_sizechange(){sasc = true;}
  //----------------------------------------------------------------------
  void suicide_after_sizechange_and_slide(){sascas = 0;}
  //----------------------------------------------------------------------
  void suicide_after(Button b){safterwho = b; safter = true;}
  //----------------------------------------------------------------------
  void place_after_slide(){pas = true;}
  //----------------------------------------------------------------------
  
  void bind_pos(Button button){
    println(button, this);
    button.bound.add(this);
    button.bound_pos = true;
  }
  //----------------------------------------------------------------------
  
  void set_size(float new_w, float new_h, int milliseconds){
    if (this.w == new_w && this.h == new_h) return;
    sizechange = true;
    scw = new_w;
    sch = new_h;
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
      if (sasc) removeFromExe.add(this);
      if (sascas==0) ++sascas;
      else if (sascas==1) removeFromExe.add(this);
    }
  }
  //----------------------------------------------------------------------
  
  void change_color(color col){
    scolor = color(col);
    fcolor = color(col); 
    ascolor = color(col, 120);
    afcolor = color(col, 120);
  }
}
