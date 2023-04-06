class Population{
 Car[] cars;
 //Track track;
 Brain[] brains;
 int[] scores;
 boolean dead;
 int popsize;
 
 Population(int size, int generation){
   popsize = size;
  cars = new Car[size];
  brains = new Brain[size];
  scores = new int[size];
  dead = false;
  
  

 for (int i = 0; i < size; i++){
    cars[i] = new Car();
    brains[i] = new Brain();
  }
  if(generation == 0) randomize();
 }
 
 //--------------------------------------------------------------
 
 void show(){
   for(int i = 0; i < cars.length; i++){
    cars[i].show(); 
   }  
 }
 
 //---------------------------------------------------------------
 
 void drive(float gas, float steering){
   int g = 0;
 for(int i = 0; i < cars.length; i++){
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
   int g = 0;
   brainoutput = new float[7];
   for(int i = 0; i < cars.length; i++){
     if (!cars[i].dead){
       brainoutput = brains[i].drive(cars[i].braininput());
       cars[i].drive(brainoutput[0], brainoutput[1]);
       g++;
     }
     //else scores[i] = cars[i].score;
   }
   dead = g == 0;
   if(dead) for(int i = 0; i < cars.length; i++) scores[i] = cars[i].score;
 }
 
 //--------------------------------------------------------------
 /*
 int max;
 int border;
 int scoresupto;
 
 Brain[] getparents(int count){
 parents =new Brain[count];
 max = 0;
 for(int i = 0; i < popsize; i++) max += scores[i]*scores[i];
 
 for(int j = 0; j < popsize; j++){
    if(scores[j] == max(scores)) { 
      parents[0] = brains[j];
      println(0 + "  " + j + "  " + scores[j]);
      break;
    }
 }
 
 for(int i = 1; i < count; i++){
   
   border = int(random(max));
   scoresupto = 0;
 
  for(int j = 0; j < popsize; j++){
   scoresupto += scores[j]*scores[j];
    if( scoresupto >= border && scores[j] >= .5 * max(scores)){ 
      parents[i] = brains[j];
      println(i + "  " + j + "  " + scores[j]); 
      
      break;
    }
    else if(j == popsize - 1){
      parents[i] = parents[0];
      break;
    }
  }
  
 }
 return parents;
 }
 */
 //------------------------------------------------------------------
 
/* Brain[] getparents(int count){
   boolean[] volt = new boolean[popsize];
   parents =new Brain[count];
   int best, ind;
   for (int i=0; i<count; ++i){
     best = 0;
     ind = 0;
     for (int j=0; j<popsize; ++j){
       if (scores[j] > best && !volt[j]){
         best = scores[j];
         ind = j;
       }
     }
     volt[ind] = true;
     parents[i] = brains[ind];
   }
   return parents;
 }
       
  */
  Brain[] parents;
  boolean parent;
  Brain[] getparents(int count){
    parents = new Brain[count];
    int i = 0;
    while(i < count){
      //parent = false;
      for(int j = 0; j < popsize; j++){
        if(scores[j] == max(scores)){
          parents[i] = brains[j];
          scores[j] = -1;
          ++i;
          //parent = true;
          break;
        }
      }
    }
    return parents;
  }
  
   
 //------------------------------------------------------------------
 
 void randomize(){
  for(int i = 0; i < popsize; i++){
    brains[i].randomize();
 }
 }
 
  //------------------------------------------------------------------
 
  void mutate(Brain[] parents){
    //for(int i = 0; i < parents.length; i++) brains[i] = parents[i];
    for(int k = 0; k < popsize; ++k){
      for(int i = 0; i <= 4; i++){
        for(int j = 0; j <= 7; j++){ 
          brains[k].intohidden[i][j] = parents[k % parents.length].intohidden[i][j];
        }
      }
    
      for(int i = 0; i <= 7; i++){
         for(int j = 0; j <= 3; j++){
           brains[k].hiddentoout[i][j] = parents[k % parents.length].hiddentoout[i][j];
         }
      }
      //brains[i] = braincopy(parents[i % parents.length]);
      brains[k].mutate(.2, 5);
      //brains[i].randomize();
    }
  }
 
  Brain braincopy(Brain b) {
    Brain new_b = new Brain();
    new_b.intohidden = b.intohidden.clone();
    new_b.hiddentoout = b.hiddentoout.clone();
    return new_b;
  }
}
