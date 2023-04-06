

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
  for (int i=0; i<db; ++i) haromszog_oldalt(randomHelyek[i]);
}

void haromszog_oldalt(int x) {
  if (szamlalo%2==0)
    haromszog_jobb(width-vizszintesSav, x);
  else
    haromszog_bal(vizszintesSav, x);
}
