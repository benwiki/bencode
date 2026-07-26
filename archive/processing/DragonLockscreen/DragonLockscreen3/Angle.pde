
float tangle (PVector v1, PVector v2) {
  return PI-atan2(v2.y-v1.y, v1.x-v2.x);
}

float tangle (PVector v1, PVector v2, float from) {
  float a = tangle(v1, v2);
  return (a-from<0 ? TWO_PI+a-from : a-from);
}

float tangleBetween (PVector v1, PVector v2, PVector v3, PVector v4) {
  return abs(tangle(v1, v2, tangle(v3, v4)));
}

float tangleDiff (PVector v1, PVector v2, PVector v3, PVector v4) {
  float bw = tangleBetween(v1, v2, v3, v4);
  if (bw>=PI*3/2) return TWO_PI-bw;
  else if (bw>=PI/2) return abs(PI-bw);
  else return bw;
}
