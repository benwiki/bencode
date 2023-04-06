

void alap() {
  noStroke();
  rectMode(CORNERS);
  fill(220);
  rect(vizszintesSav, fuggolegesSavFent, width-vizszintesSav, height-fuggolegesSavLent);

  fill(255);
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



//
