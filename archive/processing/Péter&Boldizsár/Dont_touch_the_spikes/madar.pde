

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
    
    helyzet.add(sebesseg);
    sebesseg.add(gyorsulas);
    this.utkozes();
  }

  void utkozes() {
    if (helyzet.x > width-(vizszintesSav+madarSzelesseg) || helyzet.x < vizszintesSav+madarSzelesseg) {
      sebesseg.x = sebesseg.x * -1;
      szamlalo += 1;
      
      ajandekX = int(random(vizszintesSav+haromszogMagassag+width*0.05,width-(vizszintesSav+haromszogMagassag+width*0.05)));
      ajandekY = int(random(fuggolegesSavFent+haromszogMagassag+height*0.05,height-(fuggolegesSavLent+haromszogMagassag+height*0.05)));
      ajandek_felvesz = true;
      
      if (szamlalo%2==0) {
          jobb_oldal=true;   
        } else {
          jobb_oldal=false;
        }

      if (szamlalo==0) db=0; 
      else if (szamlalo==1) db=2;
      else if (szamlalo<6)  db=3;  
      else if (szamlalo<12) db=4;
      else if (szamlalo<32) db=5;  
      else db=6;
    
      for (int i=0; i<db;i++){
        randomHelyek[i] = int(random(fuggolegesSavFent+haromszogMagassag+haromszogSzelesseg/2, height-(fuggolegesSavLent+haromszogMagassag+haromszogSzelesseg/2)));
        for(int n=0;n<i;n++){
          if(randomHelyek[i]+haromszogSzelesseg > randomHelyek[n] && randomHelyek[i]-haromszogSzelesseg < randomHelyek[n]){
            i-=1;
          }        
        }
      }
    }
    
    if (helyzet.y > height-(fuggolegesSavLent+haromszogMagassag+madarMagassag) || helyzet.y <fuggolegesSavFent+haromszogMagassag+madarMagassag) {
      gameOver = true;
    }
    
    /*for(int i=0;i<db;i++){
      if(utkozesOldalt(randomHelyek[i],helyzet.x,helyzet.y)) gameOver=true;
    }*/
    
    /*for (int i=0; i<db; ++i)
      if ((helyzet.x-madarSzelesseg <= vizszintesSav+haromszogMagassag ||
          helyzet.x+madarSzelesseg >= width-(vizszintesSav+haromszogMagassag)) &&
          abs(helyzet.y-randomHelyek[i]) < haromszogSzelesseg/2-
                                           (width-vizszintesSav-helyzet.x-madarSzelesseg)
                                           / tan(
                                                 asin( haromszogMagassag / sqrt(
                                                                            pow(haromszogSzelesseg/2, 2)
                                                                          + pow(haromszogMagassag, 2))))
             && (szamlalo%2!=1 || helyzet.x<width/2) && (szamlalo%2!=0 || helyzet.x>width/2)){
          gameOver = true;
          return;
        } */
     for (int i=0; i<db; ++i)
      for (int j=0; j<6; ++j)
        if (((kritikus_pontok[j].x <= vizszintesSav+haromszogMagassag && hsz_bent(kritikus_pontok[j].x-vizszintesSav, kritikus_pontok[j].y, randomHelyek[i])) || 
            (kritikus_pontok[j].x >= width-(vizszintesSav+haromszogMagassag) && hsz_bent(width-vizszintesSav-kritikus_pontok[j].x, kritikus_pontok[j].y, randomHelyek[i])))
            && !(szamlalo%2==1 && helyzet.x>width/2) && !(szamlalo%2==0 && helyzet.x<width/2)){
          gameOver = true;
          return;
        }
     
     if (!ajandek_felvesz && bent(helyzet, madarSzelesseg, new PVector(ajandekX, ajandekY), ajandekSugar)){
       ajandek_felvesz = true;
       ++ajandekSzamlalo;
     }
  }
  
  boolean hsz_bent(float x, float y, float hsz_y){
    return haromszogSzelesseg/2-abs(y-hsz_y) >= x*haromszogSzelesseg/2/haromszogMagassag;
  }
  
  boolean bent(PVector hely1, float radius1, PVector hely2, float radius2){
    return (hely2.x+radius2>hely1.x-radius1 && hely2.x-radius2<hely1.x+radius1) &&
           (hely2.y+radius2>hely1.y-radius1 && hely2.y-radius2<hely1.y+radius1);
  }
  
  void mutat() {
    if (gameOver) madar_halott(helyzet.x, helyzet.y);
    else if (szamlalo%2==0){
      if (sebesseg.y<0) madar_fent_jobbra(helyzet.x, helyzet.y);
      else madar_jobbra(helyzet.x, helyzet.y);
    }
    else {
      if (sebesseg.y<0) madar_fent_balra(helyzet.x, helyzet.y);
      else madar_balra(helyzet.x, helyzet.y);
    }
  }
  
  void ugras() {
    sebesseg.y = -9;
  }
}
