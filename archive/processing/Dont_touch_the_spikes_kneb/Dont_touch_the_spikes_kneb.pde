float madarX = 250;
float madarY = 300;
int szamlalo = 0;
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
int[] randomHelyek = new int[6];
int[] szintek = {0, 1, 2, 5, 11, 31};
int db=0;

float haromszogOldalt;
float randomAjandek;

void setup() {
  size(500, 700);
  madar = new Madar();
  /*
  for (int i=0; i<randomHelyek.length; ++i)
        do {
          elfer = true;
          randomHelyek[i] = (int)random(fuggolegesSavFent+haromszogMagassag, height-(fuggolegesSavLent+haromszogMagassag));
          for (int j=0; j<i; ++j)
            if (i!=j && abs(randomHelyek[j]-randomHelyek[i])<haromszogSzelesseg) elfer=false;
        } while (!elfer);*/
}

boolean bent(float x, float y, float hsz_y){
  return haromszogSzelesseg/2-abs(y-hsz_y) >= haromszogSzelesseg/2/haromszogMagassag*x;
}

void draw() {
  background(40);
  alap();
  haromszog_mutat();
  
  madar.mutat();
  if(!gameOver && mozgas) madar.mozgas();
  /*push();
  fill(255,0,0);
  noStroke();
  ellipse(mouseX, mouseY, 5, 5);
  pop();
  
  for (int i=0; i<db; ++i)
  if (((mouseX <= vizszintesSav+haromszogMagassag      &&    bent( mouseY,                       mouseY, randomHelyek[i]  )) ||
           (mouseX >= width-(vizszintesSav+haromszogMagassag) && bent( width-vizszintesSav-(mouseX), mouseY, randomHelyek[i]  )))
          && !(szamlalo%2==1 && mouseX>width/2) && !(szamlalo%2==0 && mouseX<width/2)){
     push();
     fill(255,0,0);
     noStroke();
     ellipse(100, 100, 30, 30);
     pop();
  }*/
  /*
  for (int i=0; i<db; ++i){
    haromszog_oldalt(randomHelyek[i]);
    println(i, abs(mouseY-randomHelyek[i]) < haromszogSzelesseg/2-
                                            (width-vizszintesSav-mouseX)
                                             / tan(
                                                 asin( haromszogMagassag / sqrt(
                                                                             pow(haromszogSzelesseg/2, 2)
                                                                             + pow(haromszogMagassag, 2)))));
  }
  println(' ');
  push();
  fill(255, 0, 0);
  noStroke();
  ellipse(mouseX, mouseY, 5, 5);
  pop();*/
}

void keyPressed(){
  if (key == ' '){
    mozgas = true;
    madar.ugras();
  }
}
