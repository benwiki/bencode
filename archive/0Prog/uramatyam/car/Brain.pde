class Brain{
 
  float[][]  intohidden = new float[5][8], 
            hiddentoout = new float[8][4];
  
  //-----------------------------------------------------------------
  
  Brain(){}
   
  //-----------------------------------------------------------------
   
  void show(int size){
    int x = 800;
    for(int i = 0; i < 5; ++i){
      for(int j = 0; j < 8; ++j){
        if(intohidden[i][j] >=0) stroke(#FF0303);
        else stroke(#1203FF);
        strokeWeight(abs(intohidden[i][j]) * 10);
        line(x, 40*size + 20*size*i, x+50*size, 20*size + 20*size*j);
      }
    }
    for(int i = 0; i < 8; ++i){
      for(int j = 0; j < 4; ++j){
        if(hiddentoout[i][j] >= 0) stroke(#FF0303);
        else stroke(#1203FF);
        strokeWeight(abs(hiddentoout[i][j]) * 10);
        line(x+50*size, 20*size + 20 *size* i, x+100*size, 40*size + 20*size * j); 
      }
    }
    stroke(0);
    strokeWeight(1);
    for(int i = 0; i < 5; ++i) ellipse(x, 40*size + 20*size * i, 10*size, 10*size);
    for(int i = 0; i < 8; ++i) ellipse(x+50*size, 20*size + 20 *size* i, 10*size, 10*size);
    for(int i = 0; i < 4; ++i) ellipse(x+100*size, 40*size + 20 *size* i, 10*size, 10*size);
    
  }
  
  //-----------------------------------------------------------------
   
  void randomize(){
    for(int i = 0; i < 5; ++i)
       for(int j = 0; j < 8; ++j) 
         intohidden[i][j] = random(-1.00, 1.00);
    for(int i = 0; i < 8; ++i)
       for(int j = 0; j < 4; ++j)
         hiddentoout[i][j] = random(-1.00, 1.00);
  }
   
  //------------------------------------------------------------------
   
  void mutate(float rate, int chance){
    for(int i = 0; i < 5; ++i){
      for(int j = 0; j < 8; ++j){ 
        if(int(random(chance + 1)) == chance) intohidden[i][j] +=random(-1 * rate, rate);
        if(intohidden[i][j] > 1) intohidden[i][j] = 1;
        else if(intohidden[i][j] < -1) intohidden[i][j] = -1;
      }
    }
    for(int i = 0; i < 8; ++i){
      for(int j = 0; j < 4; ++j){
        if(int(random(chance + 1)) == chance) hiddentoout[i][j] += random(-1 * rate, rate);
        if(hiddentoout[i][j] > 1) hiddentoout[i][j] = 1;
        else if(hiddentoout[i][j] < -1) hiddentoout[i][j] = -1;
      }
    }
  }
  
  //------------------------------------------------------------------
   
  int[] hidden = new int[8];
  boolean[] output = new boolean[4];
  float[] drive = new float[2];
  float node_value;
   
  float[] drive (float[] input){
    for(int i = 0; i < 8; ++i){
       node_value = 0;
       for (int j = 0; j < 5; ++j) node_value += input[j] * intohidden[j][i];
       if (node_value > 0) hidden[i] = 1;
       else hidden[i] = 0;
    }
     
    for(int i = 0; i < 4; ++i){
       node_value = 0;
       for (int j = 0; j < 8; ++j) node_value += hidden[j] * hiddentoout[j][i];
       if (node_value > 0) output[i] = true;
       else output[i] = false;
    }
    if (output[0] == output[1]) drive[0] = 0;
    else if (output[0]) drive[0] = .5;
    else drive[0] = -.5;
    
    if (output[2] == output[3]) drive[1] = 0;
    else if (output[2]) drive[1] = .017;
    else drive[1] = -.017;
     
    return drive;
  }
   
  //----------------------------------------------------------------------
  
  String[] layers_to_string (){
    String[] outcome = new String [72];
    for (int i=0; i<5; ++i)
      for (int j=0; j<8; ++j)
        outcome[i*8+j] = str(i)+" "+str(j)+" "+str(intohidden[i][j]);
    for (int i=0; i<8; ++i)
      for (int j=0; j<4; ++j)
        outcome[i*4+j+40] = str(i)+" "+str(j)+" "+str(hiddentoout[i][j]);
    return outcome;
  }
  //------------------------------------------------------------------------
  
  void compare_cars (String car1, String car2){
    
    String[] conn, conn2, goodcar1 = loadStrings(car1), goodcar2 = loadStrings(car2), hybrid = new String[74];
    float into_final_avg=0, out_final_avg=0;
    
    for(int i = 0; i < 40; ++i){
      conn = split(goodcar1[i], ' ');
      conn2 = split(goodcar2[i], ' ');
      into_final_avg += abs(float(conn[2])-float(conn2[2]))/2;
      hybrid[i] = str(int(i/8)) + " " + str(i%8) + " " + str((float(conn[2])+float(conn2[2]))/2);
    }
    println("++++++++++++++++++++++++++++");
    for(int i = 0; i < 32; ++i){
      conn = split(goodcar1[40+i], ' ');
      conn2 = split(goodcar2[40+i], ' ');
      out_final_avg += abs(float(conn[2])-float(conn2[2]))/2;
      hybrid[40+i] = str(int(i/4)) + " " + str(i%4) + " " + str((float(conn[2])+float(conn2[2]))/2);
    }
    into_final_avg /= 40;
    out_final_avg /= 32;
    println("---------------------------------");
    println(into_final_avg, out_final_avg);
    println("---------------------------------");
    saveStrings("Hybrid.txt", hybrid);
  }
  //-------------------------------------------------------------------------------------------
}
