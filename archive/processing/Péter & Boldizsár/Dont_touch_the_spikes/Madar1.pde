


void madar_jobbra(float x,float y){
  // Lent van a madár
  beginShape(QUADS);
  noStroke();
  //test felso
  fill(#f93737);
  vertex(x-madarMagassag, y   );
  vertex(x-madarMagassag, y-madarMagassag);
  vertex(x+madarMagassag, y-madarMagassag);
  vertex(x+madarMagassag, y   );
  
  //test also
  fill(#ec2b2b);
  vertex(x-madarMagassag, y   );
  vertex(x-madarMagassag, y+madarMagassag);
  vertex(x+madarMagassag, y+madarMagassag);
  vertex(x+madarMagassag, y   );
  
  //szem
  fill(255);
  vertex(x+(madarSzelesseg-madarMagassag)-2,y-(madarSzelesseg-madarMagassag)+2);
  vertex(x+(madarSzelesseg-madarMagassag)-2,y-(madarSzelesseg-madarMagassag)-2);
  vertex(x+(madarSzelesseg-madarMagassag)+2,y-(madarSzelesseg-madarMagassag)-2);
  vertex(x+(madarSzelesseg-madarMagassag)+2,y-(madarSzelesseg-madarMagassag)+2);
  
  
  //csőr alsó
  fill(255,220,0);
  vertex(x+madarMagassag,y);
  vertex(x+madarMagassag+1,y);
  vertex(x+madarSzelesseg,y);
  vertex(x+madarMagassag,y+(madarSzelesseg-madarMagassag));
  
  //csőr felső
  fill(255,240,0);
  vertex(x+madarMagassag,y);
  vertex(x+madarMagassag+1,y);
  vertex(x+madarSzelesseg,y);
  vertex(x+madarMagassag,y-(madarSzelesseg-madarMagassag));
  
  //farok
  fill(#f93737);
  vertex(x-madarSzelesseg,y-(madarSzelesseg-madarMagassag));
  vertex(x-(madarSzelesseg-madarMagassag),y-(madarSzelesseg-madarMagassag));
  vertex(x-(madarSzelesseg-madarMagassag),y);
  vertex(x-(madarSzelesseg-madarMagassag),y+(madarSzelesseg-madarMagassag)-2);
  
  //szárny
  fill(#ca1414);
  vertex(x-(madarSzelesseg-madarMagassag),y);
  vertex(x-(madarSzelesseg-madarMagassag),y+1);
  vertex(x-(madarSzelesseg-madarMagassag),y+(madarSzelesseg-madarMagassag)+4);
  vertex(x+(madarSzelesseg-madarMagassag)/2,y);
  
  endShape();
}


void madar_balra(float x,float y){
  // Lent van a madár
  beginShape(QUADS);
  noStroke();
 //test felso
  fill(#f93737);
  vertex(x-madarMagassag, y   );
  vertex(x-madarMagassag, y-madarMagassag);
  vertex(x+madarMagassag, y-madarMagassag);
  vertex(x+madarMagassag, y   );
  
  //test also
  fill(#ec2b2b);
  vertex(x-madarMagassag, y   );
  vertex(x-madarMagassag, y+madarMagassag);
  vertex(x+madarMagassag, y+madarMagassag);
  vertex(x+madarMagassag, y   );
  
  //szem
   //szem
  fill(255);
  vertex(x-(madarSzelesseg-madarMagassag)-2,y-(madarSzelesseg-madarMagassag)+2);
  vertex(x-(madarSzelesseg-madarMagassag)-2,y-(madarSzelesseg-madarMagassag)-2);
  vertex(x-(madarSzelesseg-madarMagassag)+2,y-(madarSzelesseg-madarMagassag)-2);
  vertex(x-(madarSzelesseg-madarMagassag)+2,y-(madarSzelesseg-madarMagassag)+2);
  
  
  //csőr alsó
  fill(255,220,0);
  vertex(x-madarMagassag,y);
  vertex(x-madarMagassag+1,y);
  vertex(x-madarSzelesseg,y);
  vertex(x-madarMagassag,y+(madarSzelesseg-madarMagassag));
  
    //csőr felső
  fill(255,240,0);
  vertex(x-madarMagassag,y);
  vertex(x-madarMagassag+1,y);
  vertex(x-madarSzelesseg,y);
  vertex(x-madarMagassag,y-(madarSzelesseg-madarMagassag));
  
    //farok
  fill(#f93737);
  vertex(x+madarSzelesseg,y-(madarSzelesseg-madarMagassag));
  vertex(x+(madarSzelesseg-madarMagassag),y-(madarSzelesseg-madarMagassag));
  vertex(x+(madarSzelesseg-madarMagassag),y);
  vertex(x+(madarSzelesseg-madarMagassag),y+(madarSzelesseg-madarMagassag)-2);
  
  //szárny
  //szárny
  fill(#ca1414);
  vertex(x+(madarSzelesseg-madarMagassag),y);
  vertex(x+(madarSzelesseg-madarMagassag),y+1);
  vertex(x+(madarSzelesseg-madarMagassag),y+(madarSzelesseg-madarMagassag)+4);
  vertex(x-(madarSzelesseg-madarMagassag)/2,y);
  
  endShape();
}


void madar_fent_jobbra(float x, float y){
  //Fent van a madár
  beginShape(QUADS);
  noStroke();
  //test felso
  fill(#f93737);
  vertex(x-18, y   );
  vertex(x-18, y-18);
  vertex(x+18, y-18);
  vertex(x+18, y   );
  
  //test also
  fill(#ec2b2b);
  vertex(x-18, y   );
  vertex(x-18, y+18);
  vertex(x+18, y+18);
  vertex(x+18, y   );
  
  //szem
  fill(255);
  vertex(x+7,y-7);
  vertex(x+7,y-11);
  vertex(x+11,y-11);
  vertex(x+11,y-7);
  
  
  //csőr alsó
  fill(255,220,0);
  vertex(x+18,y);
  vertex(x+18,y-1);
  vertex(x+18,y-8);
  vertex(x+28,y-8);
  
  
  
  //csőr felső
  fill(255,240,0);
  vertex(x+18,y);
  vertex(x+18,y+1);
  vertex(x+18,y+10);
  vertex(x+28,y+10);
  
  //farok
  fill(#f93737);
  vertex(x-30,y-9);
  vertex(x-10,y-9);
  vertex(x-10,y);
  vertex(x-10,y+8);
  
  //szárny
  fill(#ca1414);
  vertex(x-10,y);
  vertex(x-10,y+2);
  vertex(x-10,y+14);
  vertex(x+6,y);
  
  endShape();
  
}

void madar_fent_balra(float x,float y){
  // Lent van a madár
  beginShape(QUADS);
  noStroke();
 //test felso
  fill(#f93737);
  vertex(x-madarMagassag, y   );
  vertex(x-madarMagassag, y-madarMagassag);
  vertex(x+madarMagassag, y-madarMagassag);
  vertex(x+madarMagassag, y   );
  
  //test also
  fill(#ec2b2b);
  vertex(x-madarMagassag, y   );
  vertex(x-madarMagassag, y+madarMagassag);
  vertex(x+madarMagassag, y+madarMagassag);
  vertex(x+madarMagassag, y   );
  
  //szem
   //szem
  fill(255);
  vertex(x-(madarSzelesseg-madarMagassag)-2,y-(madarSzelesseg-madarMagassag)+2);
  vertex(x-(madarSzelesseg-madarMagassag)-2,y-(madarSzelesseg-madarMagassag)-2);
  vertex(x-(madarSzelesseg-madarMagassag)+2,y-(madarSzelesseg-madarMagassag)-2);
  vertex(x-(madarSzelesseg-madarMagassag)+2,y-(madarSzelesseg-madarMagassag)+2);
  
  
  //csőr alsó
  fill(255,220,0);
  vertex(x-madarMagassag,y);
  vertex(x-madarMagassag,y-1);
  vertex(x-madarMagassag,y+(madarSzelesseg-madarMagassag));
  vertex(x-madarSzelesseg,y+(madarSzelesseg-madarMagassag));
  
  //csőr felső
  fill(255,240,0);
  vertex(x-madarMagassag,y);
  vertex(x-madarMagassag,y+1);
  vertex(x-madarMagassag,y-(madarSzelesseg-madarMagassag));
  vertex(x-madarSzelesseg,y-(madarSzelesseg-madarMagassag));
  
    //farok
  fill(#f93737);
  vertex(x+madarSzelesseg,y-(madarSzelesseg-madarMagassag));
  vertex(x+(madarSzelesseg-madarMagassag),y-(madarSzelesseg-madarMagassag));
  vertex(x+(madarSzelesseg-madarMagassag),y);
  vertex(x+(madarSzelesseg-madarMagassag),y+(madarSzelesseg-madarMagassag)-2);
  
  //szárny
  //szárny
  fill(#ca1414);
  vertex(x+(madarSzelesseg-madarMagassag),y);
  vertex(x+(madarSzelesseg-madarMagassag),y+1);
  vertex(x+(madarSzelesseg-madarMagassag),y+(madarSzelesseg-madarMagassag)+4);
  vertex(x-(madarSzelesseg-madarMagassag)/2,y);
  
  endShape();
}
 
void madar_halott(float x, float y){
  beginShape(QUADS);
  noStroke();
  //test felso
  fill(#404040);
  vertex(x-18, y   );
  vertex(x-18, y-18);
  vertex(x+18, y-18);
  vertex(x+18, y   );
  
  //test also
  fill(#202020);
  vertex(x-18, y   );
  vertex(x-18, y+18);
  vertex(x+18, y+18);
  vertex(x+18, y   );
  
  //szem
  fill(255);
  vertex(x+5,y-4);
  vertex(x+7,y-2);
  vertex(x+14,y-13);
  vertex(x+12,y-15);
  
  vertex(x+12,y-2);
  vertex(x+14,y-4);
  vertex(x+7,y-15);
  vertex(x+5,y-13);
  
  //csőr alsó
  fill(255,220,0);
  vertex(x+18,y);
  vertex(x+18,y-1);
  vertex(x+18,y-8);
  vertex(x+28,y-8);
  
  //csőr felső
  fill(255,240,0);
  vertex(x+18,y);
  vertex(x+18,y+1);
  vertex(x+18,y+10);
  vertex(x+28,y+10);
  
  //farok
  fill(#404040);
  vertex(x-30,y-9);
  vertex(x-10,y-9);
  vertex(x-10,y);
  vertex(x-10,y+8);
  
  //szárny
  fill(#000000);
  vertex(x-10,y);
  vertex(x-10,y+2);
  vertex(x-10,y+14);
  vertex(x+6,y);
  
  endShape();
}
