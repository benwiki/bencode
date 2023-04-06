

void alap() {
  noStroke();
  rectMode(CORNERS);
  fill(220);
  rect(vizszintesSav, fuggolegesSavFent, width-vizszintesSav, height-fuggolegesSavLent);

  fill(255);
  ellipseMode(CENTER);
  ellipse(width/2, (height-(fuggolegesSavLent+fuggolegesSavFent))/2+25, width/2, width/2);

  fill(220);
  textFont(createFont("Comic Sans MS", 100));
  textAlign(CENTER, CENTER);
  if (szamlalo <10) {
    text("0"+szamlalo, width/2, (height-(fuggolegesSavLent+fuggolegesSavFent))/2);
  } else {
    text(szamlalo, width/2, (height-(fuggolegesSavLent+fuggolegesSavFent))/2);
  }
} 

void beforeGame(){
  if (!mozgas){
    noStroke();
    rectMode(CENTER);
    fill(150,99);
    rect(width/2,height/2,width,height);
    
    fill(0);
    textAlign(CENTER, CENTER);
    textFont(createFont("Comic Sans MS", 40));
    text("Press SPACE to start!",width/2,((height-fuggolegesSavLent)/2));
  }
}

void afterGame(){
  if(gameOver){
    noStroke();
    rectMode(CENTER);
    fill(150,99);
    rect(width/2,height/2,width,height);
    
    fill(255);
    textAlign(CENTER, CENTER);
    textFont(createFont("Comic Sans MS", 50));
    text("GAME OVER",width/2,((height-fuggolegesSavLent)/2));
    //////////////////////////////////////
    //////////////////////////////////////
    stroke(0);
    frissit(mouseX,mouseY);
    
    if (replayOver) {
      fill(replayColorOver);
    }else{
      fill(replayColor);
    }
  
    rectMode(CENTER);
    rect(replayX,replayY,replayWidth,replayHeight,5);
    fill(255);
    textFont(createFont("Comic Sans MS", 30));
    text("Replay",width/4,height-height/10-8);
    
    if (exitOver) {
      fill(exitColorOver);
    } else {
      fill(exitColor);
    }
  
    rect(exitX,exitY,exitWidth,exitHeight,5);
    fill(255);    
    text("Exit",3*(width/4),height-height/10-8);
    
    fill(255,128,0);
    textAlign(CENTER, CENTER);
    textFont(createFont("Comic Sans MS", 35));
    text("Ajándékok: "+str(ajandekSzamlalo),width/2,height/2+height/15);
  }
}

boolean overReplay(int x,int y,int szelesseg, int magassag){
  if (mouseX >= x-szelesseg/2 && mouseX <= x+szelesseg/2 && mouseY >= y-magassag/2 && mouseY <= y+magassag/2) {
    return true;
  } else {
    return false;
  }                                  // Felesleges 2 függvény erre a célra, ha mind2ben ugyanaz van :)
}

boolean overExit(int x, int y, int szelesseg,int magassag){ 
  if (mouseX >= x-szelesseg/2 && mouseX <= x+szelesseg/2 && mouseY >= y-magassag/2 && mouseY <= y+magassag/2){  
    return true;
  }else{
    return false;
  }
}

void frissit(int x, int y){  //////////////////////////////////// használatlan argumentumok
  if ( overReplay(replayX, replayY,replayWidth,replayHeight) ) {
    replayOver = true;
    exitOver = false;
  }else if(overExit(exitX,exitY,exitWidth,exitHeight)){ 
    replayOver = false;
    exitOver = true;
  } else{
    replayOver = false;
    exitOver = false;
  }
}


void mousePressed() {
  if (replayOver) {
    gameOver = false;
    mozgas = false;
    szamlalo = 0;
    ajandekSzamlalo = 0;
    madar.mutat();
    madar.helyzet.set(250, 300);
    madar.sebesseg.set(4,2);
    ajandekX = ajandekY = -10;
    for(int i=0;i<6;i++){
      randomHelyek[i] = 0;
    }
  }
  if(exitOver){
    exit();
  }
}
