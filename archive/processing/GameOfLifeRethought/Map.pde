
class Map{
  float cs; //cell size
  int x=0, y=0;
  
  ArrayList<PVector> cells, bring_alive;
  int counter = 0;
  
  //--------------------------------------------------
  //((((((((((((((((((((((((((((((((((((((((((((((((((
  
  Map(int squares){
    this.cs = height/squares;
    cells = new ArrayList<PVector>();
    bring_alive = new ArrayList<PVector>();
  }
  //))))))))))))))))))))))))))))))))))))))))))))))))))
  //--------------------------------------------------
  
  void show(){
    stroke(0);
     for (int i=1; i<height/cs; ++i)
       line(0, i*cs, width, i*cs);
     for (int i=1; i<width/cs; ++i)
       line(i*cs, 0, i*cs, height);
       
     fill(0);
     rectMode(CORNERS);
     for (PVector cell: cells)
       rect(x*cs + cell.x*cs, 
            y*cs + cell.y*cs, 
            x*cs +(cell.x+1)*cs, 
            y*cs +(cell.y+1)*cs);
  }
  //----------------------------------------------------------------
  
  PVector track(){
    return new PVector(floor(mouseX/cs-x), floor(mouseY/cs-y));
  }
  //----------------------------------------------------------------
  
  void set_cell(PVector new_cell){
    if (!exists(new_cell, cells))
      cells.add(new_cell);
    else
      cells.remove(new_cell);
  }
  //-------------------------------------------------------------
  
  boolean exists(PVector cell, ArrayList<PVector> in){
    for (PVector c: in)
      if (same(c, cell)) return true;
    return false;
  }
  //------------------------------------------------------------
  
  boolean same(PVector pos, PVector pos2){
    if (pos.x==pos2.x && pos.y==pos2.y) return true;
    else return false;
  }
  //-----------------------------------------------------------------------------------------
  
  void turn(){
    ++turn_counter;
    for (PVector cell: cells){
      cell.z = 0;
      for (float n = cell.x-1; n <= cell.x+1; ++n)
        for (float m = cell.y-1; m <= cell.y+1; ++m){
          if (!(n==cell.x && m==cell.y)){
            if(exists(new PVector(n, m), cells)) ++cell.z;
            else {
              counter = 0;
              for (float a = n-1; a <= n+1; ++a)
                for (float b = m-1; b <= m+1; ++b)
                  if (!(a==n && b==m) && exists(new PVector(a, b), cells)) ++counter;
              if (counter==3 && !exists(new PVector(n, m), bring_alive)) bring_alive.add(new PVector(n, m));
            }
          }
        }
    }
    for (int i=cells.size()-1; i>=0; --i)
      if (cells.get(i).z<2 || cells.get(i).z>3) 
        cells.remove(i);
    
    for (PVector cell: bring_alive)
      cells.add(cell);
      
    bring_alive.clear();
  }
  //--------------------------------------------------------------------------------------------------
  
  void erase(){
    cells.clear();
    turn_counter = 0;
  }
  
  //------------------------------------------------------------------
};
