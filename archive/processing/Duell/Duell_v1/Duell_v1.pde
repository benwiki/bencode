
byte[] b; int[][][] gettop, getfw;
int[] starting_sides = {5, 1, 2, 6, 0, 6, 2, 1, 5};
boolean RED = true, VANILLA = false;
int KING = -5, missingfile=0;
Board board; //Handler handler;
//--------------------------------------------------
color redcolor = #6C031F, vanillacolor = #F2EACB;
float cs, curveRate = 1, curveWidthRate = 1,//0.65, 
      innerRate = 0.8,
      brate=0.9, // board rate!!
      dotrate=0.18, sdotrate = 0.10, r, w, h;
String cubedesign = "Simple"; // Aron, Cool, Simple
boolean bottomplayer = RED;

void setup(){
  size(900, 700);
  //fullScreen();
  w = width; h = height;
  surface.setResizable(true);
  surface.setTitle("DUELL");
  board = new Board();
  preparations();
  textSize(width/10);
  textAlign(CENTER, CENTER);
}

void draw(){
  background(0);
  if (missingfile>0){
    text(str(missingfile)+" missing file(s)", width/2, height/2);
    return;
  }
  if (width!=w || height!=h) {
    w = width; h = height;
    board.resize();
  }
  board.show();
}


void preparations(){
  b = loadBytes("gettop.txt");
  if (b==null) ++missingfile;
  else {
    gettop = new int[4][6][6];
    for (int i=0; i<b.length; ++i)
      gettop[floor(i/36)][floor(i/6)-floor(i/36)*6][i%6] = int(b[i])-48;
  }
  b = loadBytes("getfw.txt");
  if (b==null) ++missingfile;
  else {
    getfw = new int[4][6][6];
    for (int i=0; i<b.length; ++i)
      getfw[floor(i/36)][floor(i/6)-floor(i/36)*6][i%6] = int(b[i])-48;
  }
}
