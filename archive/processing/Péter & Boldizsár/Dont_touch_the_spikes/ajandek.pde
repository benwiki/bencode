void ajandek_mutat(){
  fill(255,128,0);
  if (!ajandek_felvesz){
    noStroke();
    ellipseMode(RADIUS);
    ellipse(ajandekX, ajandekY, ajandekSugar, ajandekSugar);
  }
  textAlign(CENTER, CENTER);
  textFont(createFont("Comic Sans MS", 25));
  text("Ajándékok: "+str(ajandekSzamlalo),width/2,fuggolegesSavFent*3);
}
 
