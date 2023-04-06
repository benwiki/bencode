

void ajandek_mutat(float x,float y){
 
  noStroke();
  fill(255,128,0);
  ellipse(x,y, width/25, width/25);
}
 
void ajandek_hely(){
  //ajandek_mutat();
  // x: vizszintesSav+haromszogMagassag+width*0.05  -  width-(vizszintesSav+haromszogMagassag+width*0.05)  
  // y: fuggolegesSavFent+haromszogMagassag+height*0.05  -  height-(fuggolegesSavLent+haromszogMagassag+height*0.05)
}
