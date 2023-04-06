class Gates{

  PVector[] pos;
  ArrayList<PVector> visited1, visited2;
  boolean already = false;
  
  //--------------------
  
  Gates(int num){
    readpos("/Tracks/gates"+str(num)+".csv");
    visited1 = new ArrayList<PVector>();
    visited2 = new ArrayList<PVector>();
    show();
  }
 
  //-----------------------------------------------------------------
 
  String x = "";
  String y = "";
  
  void readpos(String filename){
    String[] lines = loadStrings(filename);
    pos = new PVector[lines.length];
    for(int i = 0; i < pos.length; ++i){
      boolean comma = false;
      for(int j = 0; j < lines[i].length(); ++j){
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
    for(int i = 0; i < pos.length-1; i += 2)
      line(pos[i].x, pos[i].y, pos[i+1].x, pos[i+1].y);
  }

  //----------------------------------------------------------------------------------------------------------------------
  
  boolean collision(float x1, float y1, float x2, float y2){
    /*stroke(0,0);
    fill(255,0,0);
    beginShape();
    for (int i=0; i<visited1.size(); ++i)
      vertex(visited1.get(i).x, visited1.get(i).y);
    for (int i=0; i<visited1.size(); ++i)
      vertex(visited2.get(i).x, visited2.get(i).y);
    endShape();
    fill(0);
    stroke(0);*/

    for(int i = 0; i < pos.length - 1; i += 2)
      if(track.lineline(x1, y1, x2, y2, pos[i].x, pos[i].y, pos[i+1].x, pos[i+1].y)){
        /*already = false;
        for (int j=0; j<visited1.size(); ++j) if (visited1.get(j)==pos[i]) already = true;
        if (!already) visited1.add(pos[i]);
        already = false;
        for (int j=0; j<visited2.size(); ++j) if (visited2.get(j)==pos[i+1]) already = true;
        if (!already) visited2.add(0, pos[i+1]);*/
        return true;
      }
    return false;
  }
  
  //------------------------------------------------------------------------------------------------------------------

}
