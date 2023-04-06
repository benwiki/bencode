
class Track{
 PVector[] posout;
 PVector[] posin;
 
 
  Track(String out, String in){
    readposout(out+".csv");
    readposin(in+".csv");
    show();
  }
  
  //--------------------------------------------------------------------------------------------------------------
  
  
  String x = "";
  String y = "";
  
  void readposout(String filename){
    String[] lines = loadStrings(filename);
    posout = new PVector[lines.length];
    for(int i = 0; i < posout.length; ++i){
      boolean comma = false;
        for(int j = 0; j < lines[i].length(); ++j){
          if(comma) y += lines[i].charAt(j);
          else if(lines[i].charAt(j) == ';') comma = true;
          else x += lines[i].charAt(j);
        }
        posout[i] = new PVector(float(x), float(y));
        x = "";
        y = "";
    }
  }
  
  //----------------------------------------------------------------------------------------------------------------
  
  void readposin(String filename){
    
    String[] lines = loadStrings(filename);
    posin = new PVector[lines.length];
    
    for(int i = 0; i < posin.length; ++i){
      boolean comma = false;
      for(int j = 0; j < lines[i].length(); ++j){
        if(comma) y += lines[i].charAt(j);
        else if(lines[i].charAt(j) == ';') comma = true;
        else x += lines[i].charAt(j);
      }
      posin[i] = new PVector(float(x), float(y));
      x = "";
      y = "";
    }
  }
  
  //-------------------------------------------------------------------------------------------------------------------
  
  void show(){
    
     for(int i = 0; i < posout.length; ++i){
    if(i <posout.length - 1)line(posout[i].x, posout[i].y, posout[i+1].x, posout[i+1].y);
    else line(posout[i].x, posout[i].y, posout[0].x, posout[0].y);  
    }
     for(int i = 0; i < posin.length; ++i){
    if(i <posin.length - 1)line(posin[i].x, posin[i].y, posin[i+1].x, posin[i+1].y);
    else line(posin[i].x, posin[i].y, posin[0].x, posin[0].y);  
    }
    
  }
  
  //-----------------------------------------------------------------------------------------------------------------
  
  boolean collision(float x1, float y1, float x2, float y2){
    
  for(int i = 0; i < posout.length; ++i){
    
    if(i <posout.length - 1){ 
      if(lineline(x1, y1, x2, y2, posout[i].x, posout[i].y, posout[i+1].x, posout[i+1].y)) return true;
    }
    
    else if(lineline(x1, y1, x2, y2, posout[i].x, posout[i].y, posout[0].x, posout[0].y)) return true;  
    
  }
    
     for(int i = 0; i < posin.length; ++i){
    if(i <posin.length - 1){
      if(lineline(x1, y1, x2, y2, posin[i].x, posin[i].y, posin[i+1].x, posin[i+1].y)) return true;
    }
    else if(lineline(x1, y1, x2, y2, posin[i].x, posin[i].y, posin[0].x, posin[0].y)) return true; 
    
     }
    return false;
  }
  
  //------------------------------------------------------------------------------------------------------------------
  
    float D;
  
  boolean lineline(float x1, float y1, float x2, float y2, float x3, float y3, float x4, float y4) {

  float uA = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1));
  float uB = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1));

  if (uA >= 0 && uA <= 1 && uB >= 0 && uB <= 1){
   
    D =sqrt(((uA * (y2-y1))) * ((uA * (y2-y1))) + ((uA * (x2-x1))) * ((uA * (x2-x1))));
    
    /*stroke(204, 102, 0);
    ellipse(x1 + uA * (x2-x1), y1 + uA * (y2-y1), 4, 4);
    line(x3, y3, x4, y4);
    line(x1, y1, x2, y2);
    stroke(0);*/
    
    return true;
  }  
   else return false;
  }

//----------------------------------------------------------------------------------------------------------------------

float[] distances;

float distance(float x1, float y1, float x2, float y2){
  
  distances = new float[posout.length + posin.length];
  

    
     for(int i = 0; i < posin.length; ++i){
    if(i < posin.length - 1){ 
      if(lineline(x1, y1, x2, y2, posin[i].x, posin[i].y, posin[i+1].x, posin[i+1].y)) distances[i + posout.length] = D;
      else distances[i] = 200;
    }
    else if(lineline(x1, y1, x2, y2, posin[i].x, posin[i].y, posin[0].x, posin[0].y)) distances[i + posout.length] = D;
    else distances[i + posout.length] = 200;
    } 
    
    for(int i = 0; i < posout.length; ++i){
    if(i < posout.length - 1){ 
      if(lineline(x1, y1, x2, y2, posout[i].x, posout[i].y, posout[i+1].x, posout[i+1].y)) distances[i] = D;
      else distances[i] = 200;
    }
    else if(lineline(x1, y1, x2, y2, posout[i].x, posout[i].y, posout[0].x, posout[0].y)) distances[i] = D;
    else distances[i] = 200;
    }
    for(int i = 0; i < distances.length; ++i) if(distances[i] == 0) distances[i] = 200;
    return min(distances);

  }
  
  //-----------------------------------------------------------------------------------------------------------------------
  
}
