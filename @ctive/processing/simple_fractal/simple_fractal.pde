int SIZE = 500;
FractalApp app;
int i = 0;
int[] draws = {0, 20, 40, 60, 80, 100, 120, 140, 160};
ArrayList<Integer> ds;

void setup() {
  //size(SIZE, SIZE);
  background(255);
  fullScreen();
  //smooth();
  app = new FractalApp();
  //app.drawNextLayer();
  ds = new ArrayList<Integer>();
  for (int draw: draws) ds.add(draw);
}

void draw() {
  background(255);
  ++i;

  if (i % 300 == 0) {
    i = 0;
    app.reset();
  } else if (ds.contains(i)) {
    app.drawNextLayer();
  }
  delay(50);
  //translate(width>>1, height>>1);
  //scale(1 + i / 500);
  app.drawPoints();
  println(i);
}

void keyReleased() {
  if (key == 'a') {
    app.drawNextLayer();
  }
}

class Point {
  float x, y, size;
  Integer angle;
  
  Point(float x, float y, Integer angle, float size) {
    this.x = x;
    this.y = y;
    this.angle = angle;
    this.size = size;
  }
}

class FractalApp {
  int n = 4;
  float size = width / 4.0;
  ArrayList<Point> points = new ArrayList<Point>();
  ArrayList<Point> leaves = new ArrayList<Point>();

  FractalApp() {
    Point p = new Point(width/2, height/2, null, size);
    points.add(p);
    leaves.add(p);
  }
  
  void reset() {
    size = width / 4.0;
    points.clear();
    leaves.clear();
    Point p = new Point(width/2, height/2, null, size);
    points.add(p);
    leaves.add(p);
    
    drawNextLayer();
  }
  
  void drawNextLayer() {
    
    ArrayList<Point> pts = drawFractalLayer();
    leaves = pts;
    points.addAll(pts);
    size /= 2;
  }

  Point pointOnCircle(Point pos, float size, float angle) {
    return new Point(pos.x + size * cos(angle), pos.y + size * sin(angle), null, size);
  }

  ArrayList<Point> drawFractalLayer() {
    ArrayList<Point> newPoints = new ArrayList<Point>();
    
    for (Point p : leaves) {
      for (int i = 0; i < n; i++) {
        if (p.angle != null && i == (p.angle + 2) % n) {
          continue;
        }
        float angle = TWO_PI * i / n;
        Point end = pointOnCircle(p, size, angle);
        end.angle = i;
        line(p.x, p.y, end.x, end.y);
        newPoints.add(end);
      }
    }
    return newPoints;
  }
  
  void drawPoints() {
    for (Point p : points) {
      for (int i = 0; i < n; i++) {
        if (p.angle != null && i == (p.angle + 2) % n) {
          continue;
        }
        float angle = TWO_PI * i / n;
        Point end = pointOnCircle(p, p.size, angle);
        end.angle = i;
        line(p.x, p.y, end.x, end.y);
      }
    }
  }
}
