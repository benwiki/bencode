
float ajandekX= -10;
float ajandekY= -10;
float ajandekSugar = width/12;
int ajandekSzamlalo = 0;
int szamlalo = 0;
int pont;
int haromszogSzelesseg= 34;
int haromszogMagassag= 25;
int haromszogTavolsag = 45;
int madarSzelesseg=28;
int madarMagassag=18;
int vizszintesSav = 25;
int fuggolegesSavFent=25;
int fuggolegesSavLent=125;
Madar madar;
boolean gameOver = false;
boolean mozgas = false;

int [] randomHelyek = new int[6]; 
int db=0;
boolean jobb_oldal;
boolean ajandek_felvesz=false;

float haromszogOldalt;

int replayX;
int replayY;
int replayWidth;
int replayHeight;
color replayColor = #4a090b;
color replayColorOver = #93090b;
boolean replayOver = false;

int exitX;
int exitY;
int exitWidth;
int exitHeight;
color exitColor = #030d48;
color exitColorOver= #030dab;
boolean exitOver = false;



void setup() {
  size(500, 700);
  
  replayX = width/4;
  replayY = height-height/10;
  replayWidth = width/4;
  replayHeight = height/12;
  
  exitX = 3*(width/4); //375
  exitY = height-height/10;  //630
  exitWidth = width/4;     //125
  exitHeight = height/12;  //58.333
  println(randomHelyek[0]);
  
  madar = new Madar();
}

void draw() {
  background(40);
  alap();
  haromszog_mutat();
  
  madar.mutat();
  if(!gameOver && mozgas){
    madar.mozgas();
    ajandek_mutat();
  }
  
  beforeGame();
  afterGame();
}

void keyPressed(){
  if (key == ' '){
    mozgas = true;
    madar.ugras();
  }
}
