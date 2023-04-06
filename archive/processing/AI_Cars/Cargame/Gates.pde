class Gates{

  PVector[] pos;
  
  //--------------------
  
  Gates(){
   readpos("gates2.csv");
   show();
 }
 
 //-----------------------------------------------------------------
 
 String x = "";
 String y = "";
  
   void readpos(String filename){
    String[] lines = loadStrings(filename);
    pos = new PVector[lines.length];
    for(int i = 0; i < pos.length; i++){
      boolean comma = false;
        for(int j = 0; j < lines[i].length(); j++){
          if(comma) y += lines[i].charAt(j);
          else if(lines[i].charAt(j) == ';') comma = true;
          else x += lines[i].charAt(j);
        }
        pos[i] = new PVector(float(x), float(y));
        x = "";
        y = "";
    }
  }
  
  //--------------------------------------------------------------------
  
   void show(){
    
     for(int i = 0; i < pos.length; i += 2){
    if(i <pos.length - 1)line(pos[i].x, pos[i].y, pos[i+1].x, pos[i+1].y);
    }
  }
  
 //------------------------------------------------------------------------------------------------------------------
  
    float D;
  
  boolean lineline(float x1, float y1, float x2, float y2, float x3, float y3, float x4, float y4) {

  float uA = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1));
  float uB = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1));

  if (uA >= 0 && uA <= 1 && uB >= 0 && uB <= 1){
   
    D =sqrt(((uA * (y2-y1))) * ((uA * (y2-y1))) + ((uA * (x2-x1))) * ((uA * (x2-x1))));
    //stroke(204, 102, 0);
    
    //ellipse(x1 + uA * (x2-x1), y1 + uA * (y2-y1), 4, 4);
    //line(x3, y3, x4, y4);
    //line(x1, y1, x2, y2);
    
    //stroke(0);
    
    return true;
  }  
   else return false;
  }

//----------------------------------------------------------------------------------------------------------------------
  
  boolean collision(float x1, float y1, float x2, float y2){
    
  for(int i = 0; i < pos.length - 1; i += 2){
   if(lineline(x1, y1, x2, y2, pos[i].x, pos[i].y, pos[i+1].x, pos[i+1].y)) return true;
    }
    return false;
  }
  
  //------------------------------------------------------------------------------------------------------------------

}
