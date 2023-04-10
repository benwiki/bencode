

void haromszog_bal(float x, float y) {
  beginShape(TRIANGLES);
  noStroke();
  fill(40);
  vertex(x, y+(haromszogSzelesseg/2));
  vertex(x, y-(haromszogSzelesseg/2));
  vertex(x+haromszogMagassag, y);

  endShape();
}

void haromszog_jobb(float x, float y) {
  beginShape(TRIANGLES);
  noStroke();
  fill(40);
  vertex(x, y-(haromszogSzelesseg/2));
  vertex(x, y+(haromszogSzelesseg/2));
  vertex(x-haromszogMagassag, y);

  endShape();
}


void haromszog_fent(float x, float y) {
  beginShape(TRIANGLES);
  noStroke();
  fill(40);
  vertex(x-(haromszogSzelesseg/2), y);
  vertex(x+(haromszogSzelesseg/2), y);
  vertex(x, y+haromszogMagassag);

  endShape();
}


void haromszog_lent(float x, float y) {
  beginShape(TRIANGLES);
  noStroke();
  fill(40);
  vertex(x-(haromszogSzelesseg/2), y);
  vertex(x+(haromszogSzelesseg/2), y);
  vertex(x, y-haromszogMagassag);

  endShape();
}

void haromszog_mutat() {
  for (int i=vizszintesSav+(haromszogTavolsag/9); i<(width-vizszintesSav); i+=haromszogTavolsag) {
    haromszog_fent(i+(haromszogSzelesseg/2), fuggolegesSavFent);
    haromszog_lent(i+(haromszogSzelesseg/2), height-fuggolegesSavLent);
  }
  haromszog_oldalt();
}

void haromszog_oldalt() {
    if (jobb_oldal) {
      for (int i=0; i<db; i++) { 
        haromszog_jobb(width-vizszintesSav, randomHelyek[i]);
      }
    } else {
      for (int i=0; i<db; i++) {
        haromszog_bal(vizszintesSav, randomHelyek[i]);
      }
    } 
}

boolean elso=false;
boolean masodik=false;
boolean harmadik=false;
boolean vegleg = false;

boolean utkozesOldalt(int haromszogY, float madarX,float madarY){
  float terulet,terulet1,terulet2,terulet3;
  if(szamlalo%2==1){
    terulet  = haromszogTerulet(vizszintesSav+haromszogMagassag, haromszogY ,vizszintesSav, haromszogY+haromszogSzelesseg/2,vizszintesSav,haromszogY+haromszogSzelesseg/2);
    for(int i=0;i<=madarMagassag;i++){
      terulet1 = haromszogTerulet(madarX-madarSzelesseg/2,madarY-madarMagassag/2+i, vizszintesSav+haromszogMagassag, haromszogY, vizszintesSav, haromszogY+haromszogSzelesseg/2);
      terulet2 = haromszogTerulet(madarX-madarSzelesseg/2,madarY-madarMagassag/2+i, vizszintesSav, haromszogY+haromszogSzelesseg/2, vizszintesSav,haromszogY+haromszogSzelesseg/2);
      terulet3 = haromszogTerulet(madarX-madarSzelesseg/2,madarY-madarMagassag/2+i, vizszintesSav+haromszogMagassag, haromszogY, vizszintesSav,haromszogY+haromszogSzelesseg/2);
      noStroke();
      fill(#ff6600,50);
      triangle(vizszintesSav+haromszogMagassag, haromszogY ,vizszintesSav, haromszogY+haromszogSzelesseg/2,vizszintesSav,haromszogY+haromszogSzelesseg/2);
      fill(#ffff00,50);
      triangle(madarX-madarSzelesseg/2,madarY-madarMagassag/2+i, vizszintesSav+haromszogMagassag, haromszogY, vizszintesSav, haromszogY+haromszogSzelesseg/2);
      fill(#00ffff,50);
      triangle(madarX-madarSzelesseg/2,madarY-madarMagassag/2+i, vizszintesSav, haromszogY+haromszogSzelesseg/2, vizszintesSav,haromszogY+haromszogSzelesseg/2);
      fill(#ff0000,50);
      triangle(madarX-madarSzelesseg/2,madarY-madarMagassag/2+i, vizszintesSav+haromszogMagassag, haromszogY, vizszintesSav,haromszogY+haromszogSzelesseg/2);
      
      float osszTerulet = terulet1+terulet2+terulet3;
      if(terulet == osszTerulet){
        elso=true;
        break;
      }
    }
    if(!elso){
      for(int i=0;i<=madarSzelesseg;i++){
      terulet1 = haromszogTerulet(madarX+i-madarSzelesseg/2,madarY-madarMagassag/2, vizszintesSav+haromszogMagassag, haromszogY, vizszintesSav, haromszogY+haromszogSzelesseg/2);
      terulet2 = haromszogTerulet(madarX+i-madarSzelesseg/2,madarY-madarMagassag/2, vizszintesSav, haromszogY+haromszogSzelesseg/2, vizszintesSav,haromszogY+haromszogSzelesseg/2);
      terulet3 = haromszogTerulet(madarX+i-madarSzelesseg/2,madarY-madarMagassag/2, vizszintesSav+haromszogMagassag, haromszogY, vizszintesSav,haromszogY+haromszogSzelesseg/2);
      float osszTerulet = terulet1+terulet2+terulet3;
      if(terulet == osszTerulet){
        masodik=true;
        break;
      }
    }
    }
    if(!masodik){
      for(int i=0;i<=madarSzelesseg;i++){
      terulet1 = haromszogTerulet(madarX+i-madarSzelesseg/2,madarY+madarMagassag/2, vizszintesSav+haromszogMagassag, haromszogY, vizszintesSav, haromszogY+haromszogSzelesseg/2);
      terulet2 = haromszogTerulet(madarX+i-madarSzelesseg/2,madarY+madarMagassag/2, vizszintesSav, haromszogY+haromszogSzelesseg/2, vizszintesSav,haromszogY+haromszogSzelesseg/2);
      terulet3 = haromszogTerulet(madarX+i-madarSzelesseg/2,madarY+madarMagassag/2, vizszintesSav+haromszogMagassag, haromszogY, vizszintesSav,haromszogY+haromszogSzelesseg/2);
      float osszTerulet = terulet1+terulet2+terulet3;
      if(terulet == osszTerulet){
        harmadik=true;
        break;
      }
    }
    }
    if(elso || masodik || harmadik) vegleg=true;
    else vegleg = false;
    //CCCCCCCCSSSSSSSSSSŐŐŐŐŐŐŐŐŐŐŐRRRRRRRRRRR
    
  }/*else{
    terulet  = haromszogTerulet(width-(vizszintesSav+haromszogMagassag), haromszogY ,width-vizszintesSav, haromszogY+haromszogSzelesseg/2,width-vizszintesSav,haromszogY+haromszogSzelesseg/2);
    terulet1 = haromszogTerulet(x,y, t.point2x, t.point2y, t.point3x, t.point3y);
    terulet2 = haromszogTerulet(x,y, t.point3x, t.point3y, t.point1x, t.point1y);
    terulet3 = haromszogTerulet(x,y, t.point2x, t.point2y, t.point1x, t.point1y);
  
  }
  
  
  float osszTerulet = terulet1+terulet2+terulet3;
  return (terulet == osszTerulet);
*/
  return vegleg;
}


float haromszogTerulet(float p1, float p2, float p3, float p4, float p5, float p6) {
  float a,b,c,d;
  a = p1 - p5;
  b = p2 - p6;
  c = p3 - p5;
  d = p4 - p6;
  return (0.5* abs((a*d)-(b*c)));
}
