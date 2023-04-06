byte[] b;
byte[][][] b2;

void setup(){
  /*ArrayList trying = new ArrayList();
  trying.add(0.8);
  trying.add(0.1);
  trying.add(1, 0.9);
  println(trying);*/
  b = loadBytes("try.txt");
  //printArray(b);
  b2 = new byte[4][6][6];
  for (int i=0; i<b.length; ++i)
    b2[floor(i/36)][floor(i/6)-floor(i/36)*6][i%6] = byte(int(b[i])-48);
}

void draw(){
  //println(str(key), keyPressed);
  
}
