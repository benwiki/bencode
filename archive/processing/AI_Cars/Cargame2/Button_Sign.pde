
class SignsHandler {
  
  ArrayList<Sign> all;
  
  SignsHandler (){
    all = new ArrayList<Sign>();
  }
  //-----------------------------------
  
  Sign getByName(String name){
    for (Sign s: all)
      if (s.type == name)
        return s;
    
    println("No sign found by this name:", name);
    return new Sign();
  }
  //-----------------------------------------------
  
  void show(){
    if (all.size() > 0)
      for (Sign s: all)
        s.show();
  }
  //-----------------------------------------------------
  
  Sign addNew (Button master){
    all.add( new Sign(master) );
    return all.get(all.size()-1);
  }
  //-----------------------------------------------------
  
};

//=============================================================================================================================

class Sign {
  
  Button mr; // MASTER!
  Timer time = new Timer();
  
  String type="", name="", text="";
  int textSize=20, rotationTime = 10000, arrowDir=-1;
  float rotation=0;
  
  color normal_color=color(0), active_color=color(50);
  PVector textvector;
  boolean empty = false;
  
  Sign(){empty = true;}
  
  Sign (Button master) {
    this.mr = master;
  }
  
  Sign setType (String type) { this.type = type; return this; }
  Sign setName (String name) { this.name = name; return this; }
  
  Sign setText (String text, PVector textvector, int textSize){
    textFont(createFont("Century Gothic Félkövér", textSize));
    this.text = text;
    this.textvector = textvector.copy();
    this.textSize = textSize;
    return this;
  }
  
  Sign setColors(color normal, color active){
    normal_color = normal;
    active_color = active;
    return this;
  }
  
  void show(){
    if (mr.mouseOver) {stroke(active_color); fill(active_color);}
    else              {stroke(normal_color); fill(normal_color);}
    
    if(type=="plus"){
      strokeWeight(mr.d);
      line(mr.pos.x-mr.w/2+mr.w/5, mr.pos.y, mr.pos.x+mr.w/2-mr.w/5, mr.pos.y);
      line(mr.pos.x, mr.pos.y-mr.h/2+mr.h/5, mr.pos.x, mr.pos.y+mr.h/2-mr.h/5);
    } 
    else if(type=="dot"){
      strokeWeight(mr.d);
      ellipse(mr.pos.x, mr.pos.y, mr.h/5, mr.h/5);
    }
    else if(type=="arrow"){
      strokeWeight(mr.d);
      line(mr.pos.x-mr.w/2+mr.w/3, mr.pos.y, mr.pos.x+mr.w/2-mr.w/3, mr.pos.y);
      line(mr.pos.x, mr.pos.y-mr.h/4, mr.pos.x+mr.w/2-mr.w/3, mr.pos.y);
      line(mr.pos.x, mr.pos.y+mr.h/4, mr.pos.x+mr.w/2-mr.w/3, mr.pos.y);
    }
    else if(type=="x"){
      strokeWeight(mr.d);
      line(mr.pos.x+cos(radians(135.0))*mr.w/2, mr.pos.y+sin(radians(135.0))*mr.w/2, mr.pos.x+cos( radians(-45.0))*mr.w/2, mr.pos.y+sin( radians(-45.0))*mr.w/2);
      line(mr.pos.x+cos( radians(45.0))*mr.w/2, mr.pos.y+sin( radians(45.0))*mr.w/2, mr.pos.x+cos(radians(-135.0))*mr.w/2, mr.pos.y+sin(radians(-135.0))*mr.w/2);
    }
    else if(type=="text"){
      textSize(textSize);
      fill(255);
      textAlign(CENTER, CENTER);
      text(text, mr.pos.x + textvector.x, 
                 mr.pos.y + textvector.y);
    }
    else if(type=="poarrow"){
      if (arrowDir == -1){
        println("something's fudged up");
        return;
      }
      strokeWeight(mr.d);
      line(mr.pos.x+cos(radians(arrowDir*45))*mr.w/2, mr.pos.y+sin(radians(arrowDir*45))*mr.w/2, mr.pos.x+cos(radians(arrowDir*45+180))*mr.w/2, mr.pos.y+sin(radians(arrowDir*45+180))*mr.w/2);
      line(mr.pos.x+cos(radians(arrowDir*45))*mr.w/2, mr.pos.y+sin(radians(arrowDir*45))*mr.w/2, mr.pos.x+cos(radians(arrowDir*45-90))*mr.w/4, mr.pos.y+sin(radians(arrowDir*45-90))*mr.w/4);
      line(mr.pos.x+cos(radians(arrowDir*45))*mr.w/2, mr.pos.y+sin(radians(arrowDir*45))*mr.w/2, mr.pos.x+cos(radians(arrowDir*45+90))*mr.w/4, mr.pos.y+sin(radians(arrowDir*45+90))*mr.w/4);
    }
    else if (type == "startingpoint"){
      if (!time.started) time.start();
      rotation = map(time.state()%rotationTime, 0, rotationTime, 0, 2*PI); 
      strokeWeight(mr.d);
      //strokeCap(ROUND);
      line(mr.pos.x - mr.w*7/20*cos(rotation), mr.pos.y - mr.w*7/20*sin(rotation), mr.pos.x - mr.w*3/20*cos(rotation), mr.pos.y - mr.w*3/20*sin(rotation));
      line(mr.pos.x + mr.w*7/20*cos(rotation), mr.pos.y + mr.w*7/20*sin(rotation), mr.pos.x + mr.w*3/20*cos(rotation), mr.pos.y + mr.w*3/20*sin(rotation));
      ellipse(mr.pos.x, mr.pos.y, mr.d*2, mr.d*2);
    }
    else if (type == "play"){
      strokeWeight(mr.d);
      strokeJoin(ROUND);
      noFill();
      triangle(mr.pos.x-mr.w/6, mr.pos.y-mr.h/4, 
               mr.pos.x-mr.w/6, mr.pos.y+mr.h/4, 
               mr.pos.x+mr.w*3/12, mr.pos.y);
    }
    else if (type == "pause"){
      strokeWeight(mr.d);
      line(mr.pos.x-mr.w/6, mr.pos.y-mr.h/4, mr.pos.x-mr.w/6, mr.pos.y+mr.h/4);
      line(mr.pos.x+mr.w/6, mr.pos.y-mr.h/4, mr.pos.x+mr.w/6, mr.pos.y+mr.h/4);
    }
    else if (type == "stop"){
      strokeWeight(mr.d);
      strokeJoin(MITER);
      rectMode(CORNERS);
      noFill();
      rect(mr.pos.x-mr.w/4, mr.pos.y-mr.h/4, mr.pos.x+mr.w/4, mr.pos.y+mr.h/4);
    }
  }
  
};
