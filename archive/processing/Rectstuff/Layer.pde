class Layer{
  color col;
  float csx=0, csy=0;
  int x, y; //cell size x y
  boolean[][] pieces;
  //ArrayList<PVector> pcslist = new ArrayList<PVector>();
  boolean deleted=false;
  int got=0;
  float cornersize;

  Layer(){}

  Layer(color c, int x, int y){
    col=c;
    csx=width/float(x);
    csy=height/float(y);
    cornersize=csy/4;
    this.x=x;
    this.y=y;
    got=x*y;
    pieces=new boolean[x][y];
    for (int i=0; i<x; ++i)
      for (int j=0; j<y; ++j)
        pieces[i][j]=true;
  }

  void show(){
    if (deleted) {
      checkLayer();
      overlay();
    }
    fill(col);
    for (byte i=0; i<x; ++i)
      for (byte j=0; j<y; ++j)
        if (pieces[i][j])
          rect(i*csx, j*csy, csx, csy,
          corner(i,j,byte(0)), corner(i,j,byte(2)),
          corner(i,j,byte(3)), corner(i,j,byte(1)));

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

  private void overlay(){

  }

  private float corner (byte i, byte j, byte c) {
    if     (c==0 && i>0 && j>0)                                return getcorner(pieces[i-1][j-1], pieces[i-1][j], pieces[i][j-1]);
    else if(c==2 && j>0 && i<pieces.length-1)                  return getcorner(pieces[i+1][j-1], pieces[i+1][j], pieces[i][j-1]);
    else if(c==3 && j<pieces[0].length-1 && i<pieces.length-1) return getcorner(pieces[i+1][j+1], pieces[i+1][j], pieces[i][j+1]);
    else if(c==1 && j<pieces.length-1 && i>0)                  return getcorner(pieces[i-1][j+1], pieces[i-1][j], pieces[i][j+1]);
    else return 0;
  }

  private float getcorner(boolean a, boolean b, boolean c){
    if (!b&&!c) return cornersize;
    else if(b^c) {
      if (a) return -cornersize;
      else return 0;
    }
    else if (a) return 0;
    else return -cornersize;
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
