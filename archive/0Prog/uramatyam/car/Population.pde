
class Population {
  
  Car[] cars;
  Brain[] brains;
  int[] scores;
  float[] coeffs; //mutation coefficients
  boolean dead;
  int popsize;
  float[][] into_avg, out_avg;
  float into_final_avg, out_final_avg;
  float size = 1;
  boolean go_small = false;
  int bestindex=0;
  
  //--------------------------------------
 
  Population(int size, int generation){
    popsize = size;
    cars = new Car[size];
    brains = new Brain[size];
    scores = new int[size];
    dead = false;
    into_avg = new float[5][8];
    out_avg = new float[8][4];
    
    iteration = 0;

    for (int i = 0; i < size; ++i){
      cars[i] = new Car();
      brains[i] = new Brain();
    }
    if(generation == 0) randomize();
    
    ////////////////////////////////////
    //load_good_car(brains[0]);
    ////////////////////////////////////
    cars[0].carcolor = color(255, 0, 0);
    cars[0].size = 3;
    
  }
 
  //--------------------------------------------------------------
  
  void load_good_car(Brain brain){
    String[] conn, goodcar = loadStrings("/Good_Cars/track3_score600.txt");
    //String[] conn, goodcar = loadStrings("/Good_Cars/track3_score70.txt");
    for(int i = 0; i < 40; ++i){
      conn = split(goodcar[i], ' ');
      brain.intohidden[int(conn[0])][int(conn[1])] = float(conn[2]);
    }
    for(int i = 0; i < 32; ++i){
      conn = split(goodcar[40+i], ' ');
      brain.hiddentoout[int(conn[0])][int(conn[1])] = float(conn[2]);
    }
  }
 
  void show(){
    for(int i = 0; i < cars.length; ++i) cars[i].show();
  }
 
  //---------------------------------------------------------------
 
  void drive(float gas, float steering){
    int g = 0;
    for(int i = 0; i < cars.length; ++i){
      if (!cars[i].dead){
        cars[i].drive(gas, steering);
        g++;
      }
      else scores[i] = cars[i].score;
    }
    dead = g == 0;
  }
 
  //---------------------------------------------------------------
  float[] brainoutput;
 
  void AIdrive(){
    boolean isalldead = true;
    brainoutput = new float[2];
    for(int i = 0; i < cars.length; ++i){
      if (!cars[i].dead){
        brainoutput = brains[i].drive(cars[i].braininput());
        cars[i].drive(brainoutput[0], brainoutput[1]);
        isalldead = false;
      }
      else scores[i] = cars[i].score;
      //scores[i] = cars[i].score;
    }
    dead = isalldead;
    //if(dead) for(int i = 0; i < cars.length; ++i) scores[i] = cars[i].score;
    ++iteration;
  }
 
  //--------------------------------------------------------------
  int max, border, scoresupto, notvalid=0;
 
  void getparents(int count){
    parents = new Brain[count];
    max = 0;
    for(int i = 0; i < popsize; ++i) max += pow(scores[i],4);
    
    for(int j = 0; j < popsize; ++j){
      if(scores[j] == max(scores)) { 
        parents[0] = brains[j];
        bestindex = j;
        println(0 + "  " + j + "  " + scores[j]);
        break;
      }
    }
   
    for(int i = 1; i < count; ++i){
      border = int(random(max));
      scoresupto = 0;
      for(int j = 0; j < popsize; ++j){
        scoresupto += pow(scores[j],4);
        if( scoresupto >= border && scores[j] >= max(scores)/2){ 
          parents[i] = brains[j];
          //println(i + "  " + j + "  " + scores[j]); 
          break;
        }
        else if(j == popsize - 1){
          parents[i] = brains[bestindex];
          ++notvalid;
        }
      }
    }
    saveStrings("/Best_Weights/BestCar-attempt"+str(latest_attempt)+"-gen"+str(generation-1)+".txt", parents[0].layers_to_string());
  }

  /*void getparents(int count){
    parents = new Brain[count];
    for (int i = 0; i<count; ++i){
      for(int j = 0; j < popsize; ++j){
        if(scores[j] == max(scores)){
          if (i==0){
            bestindex = j;
            println("Car:",j, "Score:",scores[j]);
          }
          parents[i] = brains[j];
          scores[j] = -1;
          break;
        }
      }
    }
    saveStrings("/Best_Weights/BestCar-attempt"+str(latest_attempt)+"-gen"+str(generation-1)+".txt", parents[0].layers_to_string());
  }*/
  
   
  //------------------------------------------------------------------
 
  void randomize(){
    for(int i = 0; i < popsize; ++i)
      brains[i].randomize();
  }
 
  //------------------------------------------------------------------
 
  void mutate(Brain[] parents){
    
    for(int k = 0; k < popsize; ++k){
      for(int i = 0; i < 5; ++i)
        for(int j = 0; j < 8; ++j)
          brains[k].intohidden[i][j] = parents[k%parents.length].intohidden[i][j];
          
      for(int i = 0; i < 8; ++i)
        for(int j = 0; j < 4; ++j)
          brains[k].hiddentoout[i][j] = parents[k%parents.length].hiddentoout[i][j];
      
      if (k != 0) brains[k].mutate(.25/pow(cars[k].score, 0.1) ,4);
    }
  }
  
  //-----------------------------------------------------------------
  
  float[] countAverages(){
    
    for(int i = 0; i < 5; ++i)
      for(int j = 0; j < 8; ++j) {
        into_avg[i][j] = 0;
        for (int k=0; k < parents.length; ++k) into_avg[i][j] += parents[k].intohidden[i][j];
        into_avg[i][j] /= parents.length;
        into_final_avg += abs(abs(parents[0].intohidden[i][j])-abs(into_avg[i][j]));
        //println(i, j, abs(abs(parents[0].intohidden[i][j])-abs(into_avg[i][j])), " az eltérés");
      }
    into_final_avg /= 40;
    
    //println("+++++++++++++++++++++++++++++++++");
    
    for(int i = 0; i < 8; ++i)
      for(int j = 0; j < 4; ++j){
        out_avg[i][j] = 0;
        for (int k=0; k < parents.length; ++k) out_avg[i][j] += parents[k].hiddentoout[i][j];
        out_avg[i][j] /= parents.length;
        out_final_avg += abs(abs(parents[0].hiddentoout[i][j])-abs(out_avg[i][j]));
        //println(i, j, abs(abs(parents[0].hiddentoout[i][j])-abs(out_avg[i][j])),"az eltérés");
      }
    out_final_avg /= 32;
    
    float[] result = new float[2];
    result[0] = into_final_avg;
    result[0] = out_final_avg;
    
    /*println("-------------------");
    println(result);
    println("-------------------");*/
    
    return result;
  }
}
