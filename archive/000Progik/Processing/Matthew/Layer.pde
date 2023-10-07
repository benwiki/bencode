class Layer{
  color col;
  float csx=0, csy=0;
  int x, y; //cell size x y
  boolean[][] pieces;
  boolean deleted=false;
  int missing;
  
  Layer(){}
  
  Layer(color c, int x, int y){
    col=c;
    csx=width/float(x);
    csy=height/float(y);
    this.x=x;
    this.y=y;
    missing=x*y;
    pieces=new boolean[x][y];
    for (int i=0; i<x; ++i)
      for (int j=0; j<y; ++j)
        pieces[i][j]=true;
  }
  
  void show(){
    if (deleted){
      deleted=false;
      if (--missing==0){
        if (++empty==layernum) newLayers();
        layers.remove(this);
      }
    }
    fill(col);
    for (int i=0; i<x; ++i)
      for (int j=0; j<y; ++j)
        if (pieces[i][j])
          rect(i*csx, j*csy, csx, csy);
  }
  
  boolean over (){
    if (pieces[floor(mouseX/csx)][floor(mouseY/csy)]){
      pieces[floor(mouseX/csx)][floor(mouseY/csy)]=false;
      deleted=true;
      return true;
    }
    return false;
  }
};