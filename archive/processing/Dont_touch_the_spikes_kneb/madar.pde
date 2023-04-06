
class Madar {
  PVector helyzet;
  PVector sebesseg;
  PVector gyorsulas;
  PVector[] kritikus_pontok;
  
  Madar() {
    helyzet = new PVector(250, 300) ;
    sebesseg = new PVector(4, 2);
    gyorsulas = new PVector(0, 0.4);
    
    kritikus_pontok = new PVector[6];
    for (int i=0; i<6; ++i)
      kritikus_pontok[i] = new PVector();
  }

  void mozgas() {
    
    kritikus_pontok[0].set(helyzet.x+madarSzelesseg, helyzet.y);
    kritikus_pontok[1].set(helyzet.x-madarSzelesseg, helyzet.y);
    kritikus_pontok[2].set(helyzet.x+madarSzelesseg, helyzet.y+madarMagassag);
    kritikus_pontok[3].set(helyzet.x+madarSzelesseg, helyzet.y-madarMagassag);
    kritikus_pontok[4].set(helyzet.x-madarSzelesseg, helyzet.y+madarMagassag);
    kritikus_pontok[5].set(helyzet.x-madarSzelesseg, helyzet.y-madarMagassag);
    
    this.utkozes();
    helyzet.add(sebesseg);
    sebesseg.add(gyorsulas);
  }

  void utkozes() {
    if (helyzet.x > width-(vizszintesSav+madarSzelesseg) || helyzet.x < vizszintesSav+madarSzelesseg) {
      if (db < 6 && szintek[db] == szamlalo) ++db;
      sebesseg.x = sebesseg.x * -1;
      szamlalo += 1;
      
      for (int i=0; i<db;i++){
        randomHelyek[i] = int(random(fuggolegesSavFent+haromszogMagassag+haromszogSzelesseg/2, height-(fuggolegesSavLent+haromszogMagassag+haromszogSzelesseg/2)));
        for(int n=0;n<i;n++)
          if(randomHelyek[i]+haromszogSzelesseg > randomHelyek[n] && randomHelyek[i]-haromszogSzelesseg < randomHelyek[n])
            i-=1;
      }
    }

    if (helyzet.y > height-(fuggolegesSavLent+haromszogMagassag+madarMagassag) || 
        helyzet.y <fuggolegesSavFent+haromszogMagassag+madarMagassag) {
      gameOver = true;
      return;
    }
    
    for (int i=0; i<db; ++i)
      for (int j=0; j<6; ++j)
        if ((kritikus_pontok[j].x <= vizszintesSav+haromszogMagassag*3/4 || kritikus_pontok[j].x >= width-(vizszintesSav+haromszogMagassag*3/4))
            && abs(kritikus_pontok[j].y-randomHelyek[i]) < haromszogSzelesseg/2-
                                            (width-vizszintesSav-kritikus_pontok[j].x)
                                             / tan(
                                                 asin( haromszogMagassag / sqrt(
                                                                             pow(haromszogSzelesseg/2, 2)
                                                                             + pow(haromszogMagassag, 2))))
            && !(szamlalo%2==1 && helyzet.x>width/2) && !(szamlalo%2==0 && helyzet.x<width/2)){
          gameOver = true;
          return;
        }
    /*for (int i=0; i<db; ++i)
      if (((helyzet.x-madarSzelesseg <= vizszintesSav+haromszogMagassag      &&    bent( helyzet.x-madarSzelesseg,                       helyzet.y, randomHelyek[i]  )) ||
           (helyzet.x+madarSzelesseg >= width-(vizszintesSav+haromszogMagassag) && bent( width-vizszintesSav-(helyzet.x+madarSzelesseg), helyzet.y, randomHelyek[i]  )))
          && !(szamlalo%2==1 && helyzet.x>width/2) && !(szamlalo%2==0 && helyzet.x<width/2)){
        gameOver = true;
        return;
      }*/
  }
  
  /*boolean bent(float x, float y, float hsz_y){
    return haromszogSzelesseg/2-abs(y-hsz_y) >= haromszogSzelesseg/2/haromszogMagassag*x;
  }*/ 

  void mutat() {
    if (gameOver) madar_halott(helyzet.x, helyzet.y);
    else if (szamlalo%2==0) madar_jobbra(helyzet.x, helyzet.y);
    else madar_balra(helyzet.x, helyzet.y);
  }

  void ugras() {
    sebesseg.y = -9;
  }
};
