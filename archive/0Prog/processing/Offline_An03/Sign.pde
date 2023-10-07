
class Sign {
  
  Button mr; // MASTER!
  
  String name;
  color normal_color, active_color;
  String text="";
  PVector textvector;
  
  Sign (String name, String text, PVector textvector, Button master){
    this.name = name;
    this.text = text;
    this.mr = master;
    this.textvector = new PVector();
    this.textvector.set(textvector);
  }
  
  Sign (String name, Button master){
    this.name = name;
    this.mr = master;
  }
  
  void setColors(color normal, color active){
    normal_color = normal;
    active_color = active;
  }
  
  void show(){
    if (mr.mouseOver) {stroke(active_color); fill(active_color);}
    else              {stroke(normal_color); fill(normal_color);}
    
    if(name=="plus"){
      strokeWeight(mr.d);
      line(mr.pos.x-mr.w/2+mr.w/5, mr.pos.y, mr.pos.x+mr.w/2-mr.w/5, mr.pos.y);
      line(mr.pos.x, mr.pos.y-mr.h/2+mr.h/5, mr.pos.x, mr.pos.y+mr.h/2-mr.h/5);
    } 
    else if(name=="dot"){
      strokeWeight(mr.d);
      ellipse(mr.pos.x, mr.pos.y, mr.h/5, mr.h/5);
    }
    else if(name=="arrow"){
      strokeWeight(mr.d);
      line(mr.pos.x-mr.w/2+mr.w/3, mr.pos.y, mr.pos.x+mr.w/2-mr.w/3, mr.pos.y);
      line(mr.pos.x, mr.pos.y-mr.h/4, mr.pos.x+mr.w/2-mr.w/3, mr.pos.y);
      line(mr.pos.x, mr.pos.y+mr.h/4, mr.pos.x+mr.w/2-mr.w/3, mr.pos.y);
    }
    else if(name=="x"){
      strokeWeight(mr.d);
      line(mr.pos.x+cos(radians(135.0))*mr.w/2, mr.pos.y+sin(radians(135.0))*mr.w/2, mr.pos.x+cos( radians(-45.0))*mr.w/2, mr.pos.y+sin( radians(-45.0))*mr.w/2);
      line(mr.pos.x+cos( radians(45.0))*mr.w/2, mr.pos.y+sin( radians(45.0))*mr.w/2, mr.pos.x+cos(radians(-135.0))*mr.w/2, mr.pos.y+sin(radians(-135.0))*mr.w/2);
    }
    else if(name=="text"){
      textSize(board.cs/3.3);
      fill(255);
      text(text, mr.pos.x + textvector.x, 
                 mr.pos.y + textvector.y);
    }
    else if(name=="poarrow"){
      if (mr.arrowDir == -1){
        println("something's fudged up");
        return;
      }
      strokeWeight(mr.d);
      line(mr.pos.x+cos(radians(mr.arrowDir*45))*mr.w/2, mr.pos.y+sin(radians(mr.arrowDir*45))*mr.w/2, mr.pos.x+cos(radians(mr.arrowDir*45+180))*mr.w/2, mr.pos.y+sin(radians(mr.arrowDir*45+180))*mr.w/2);
      line(mr.pos.x+cos(radians(mr.arrowDir*45))*mr.w/2, mr.pos.y+sin(radians(mr.arrowDir*45))*mr.w/2, mr.pos.x+cos(radians(mr.arrowDir*45-90))*mr.w/4, mr.pos.y+sin(radians(mr.arrowDir*45-90))*mr.w/4);
      line(mr.pos.x+cos(radians(mr.arrowDir*45))*mr.w/2, mr.pos.y+sin(radians(mr.arrowDir*45))*mr.w/2, mr.pos.x+cos(radians(mr.arrowDir*45+90))*mr.w/4, mr.pos.y+sin(radians(mr.arrowDir*45+90))*mr.w/4);
    }
    else if(name == "stroke") {
      strokeWeight(mr.d);
      fill(mr.scolor);
      stroke(mr.scolor);
      line(mr.pos.x-mr.w/2, mr.pos.y-mr.h/2, mr.pos.x+mr.w/2, mr.pos.y+mr.h/2);
    }
  }
  
  void addToText(int val) {
    text = str(int(text)+val);
  }
  
};
