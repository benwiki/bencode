
ArrayList<PVector> points;
ArrayList<PVector> pts_on_screen;

void setup(){
  size(800,800);
  points = new ArrayList<PVector>();
  pts_on_screen = new ArrayList<PVector>();
  stroke(0);
  strokeWeight(5);
  fill(0);
}

void draw(){
  background(255);
  for (int i=0; i<points.size()-1; ++i) line(points.get(i).x, 
                                             points.get(i).y, 
                                             points.get(i+1).x, 
                                             points.get(i+1).y);
                                             
  for (int i=0; i<pts_on_screen.size()-1; ++i) line(pts_on_screen.get(i).x, 
                                                    pts_on_screen.get(i).y, 
                                                    pts_on_screen.get(i+1).x, 
                                                    pts_on_screen.get(i+1).y);
                                                    
  for (PVector pt: points) ellipse(pt.x, pt.y, 5, 5);
  for (PVector pt: pts_on_screen) ellipse(pt.x, pt.y, 5, 5);
}

String[] list_to_string(){
  String[] pts = new String[points.size()];
  for (int i=0; i<points.size(); ++i)
    pts[i] = points.get(i).x + ";" + points.get(i).y;
  return pts;
}

void keyPressed(){
  if (key == 'o'){
    //points.add(points.get(0).copy());
    saveStrings("trackout3.csv", list_to_string());
    pts_on_screen.addAll(points);
    points.clear();
  }
  else if (key == 'i'){
    saveStrings("trackin3.csv", list_to_string());
    pts_on_screen.addAll(points);
    points.clear();
  }
  else if (key == 'g'){
    saveStrings("gates3.csv", list_to_string());
    pts_on_screen.addAll(points);
    points.clear();
  }
  else if (key == 'e')
    points.clear();
}

void mouseClicked(){
  points.add(new PVector(mouseX, mouseY));
}
