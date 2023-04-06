class Layer{
  color col;
  float csx=0, csy=0;
  int x, y; //cell size x y
  boolean[][] pieces;
  //ArrayList<PVector> pcslist = new ArrayList<PVector>();
  boolean deleted=false;
  int got=0;
  float cornersize;
  PVector bry = new PVector(); //boundary
  
  Layer(){}
  
  Layer(color c, int x, int y){
    col=c;
    csx=width/float(x);
    csy=height/float(y);
    cornersize=csx/4;
    this.x=x;
    this.y=y;
    got=x*y;
    pieces=new boolean[x][y];
    for (int i=0; i<x; ++i)
      for (int j=0; j<y; ++j)
        pieces[i][j]=true;
    //print(6
  }
  
  void show(){

    fill(col);
    for (byte i=0; i<x; ++i)
      for (byte j=0; j<y; ++j)
        if (pieces[i][j])
          rect(i*csx, j*csy, csx, csy, 
          corner(i,j,byte(0)), corner(i,j,byte(2)), 
          corner(i,j,byte(3)), corner(i,j,byte(1)));
    if (deleted) {
      checkLayer();
      overlay();
    }
  }
  
  private void checkLayer(){
    deleted=false;
    /*if (layers.indexOf(this)==layers.size()-1) 
      layers.add(new Layer(randomColor(),++next*4, next*4));
    if (next>=layernum) next=0;*/
    if (--got==0){
      if (++empty==layernum) newLayers();
      layers.remove(this);
    }
  }
  
  private float corner (byte i, byte j, byte c) {
    if     (c==0 && i>0 && j>0)                                return getcorner(pieces[i-1][j-1], pieces[i-1][j], pieces[i][j-1]);
    else if(c==2 && j>0 && i<pieces.length-1)                  return getcorner(pieces[i+1][j-1], pieces[i+1][j], pieces[i][j-1]);
    else if(c==3 && j<pieces[0].length-1 && i<pieces.length-1) return getcorner(pieces[i+1][j+1], pieces[i+1][j], pieces[i][j+1]);
    else if(c==1 && j<pieces.length-1 && i>0)                  return getcorner(pieces[i-1][j+1], pieces[i-1][j], pieces[i][j+1]);
    else return 0;
  }
  
  private float getcorner(boolean a, boolean b, boolean c){
    if (!a&&b&&c) return -cornersize;
    else if (!(b||c)) return cornersize;
    else return 0;
  }

  
  private void overlay(){
    
  }
  
  boolean checkpt (){
    if (pieces[floor(mouseX/csx)][floor(mouseY/csy)] && !over(deletepoint)){
      pieces[floor(mouseX/csx)][floor(mouseY/csy)]=false;
      deleted=true;
      //released=false;
      deletepoint.set(mouseX, mouseY);
      return true;
    }
    return false;
  }
  
  boolean over (PVector pt) {
    bry.set(pt.x-pt.x%csx, pt.y-pt.y%csy);
    if (released) return false;
    return pt.x>0 && pt.y>0 && mouseX>=bry.x && mouseX<=bry.x+csx && mouseY>=bry.y && mouseY<=bry.y+csy;
  }
};
