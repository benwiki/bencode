class Brain{
  //Track track;
 
  float[] [] intohidden;
  float[] [] hiddentoout;
  
  //-----------------------------------------------------------------
  
  Brain(){
   //track = new Track();
   intohidden = new float[5] [8];
   hiddentoout = new float[8] [4];
   }
   
   //-----------------------------------------------------------------
   
   void show(){
     for(int i = 0; i < 5; i++) ellipse(20, 20 + 20 * i, 10, 10);
     for(int i = 0; i < 8; i++) ellipse(70, 20 + 20 * i, 10, 10);
     for(int i = 0; i < 4; i++) ellipse(120, 20 + 20 * i, 10, 10);
     for(int i = 0; i <= 4; i++){
       for(int j = 0; j <= 7; j++) if(intohidden[i] [j] >=0){
         stroke(#FF0303);
         strokeWeight(intohidden[i] [j] * 10);
         line(20, 20 + 20 * i, 70, 20 + 20 * j);
       }
       else{
         stroke(#1203FF);
         strokeWeight(intohidden[i] [j] * -10);
         line(20, 20 + 20 * i, 70, 20 + 20 * j);
       }
    }
    
    for(int i = 0; i <= 7; i++){
       for(int j = 0; j <= 3; j++) if(hiddentoout[i] [j] >= 0){
        stroke(#FF0303);
         strokeWeight(hiddentoout[i] [j] * 10);
         line(70, 20 + 20 * i, 120, 20 + 20 * j); 
       }
       else{
         stroke(#1203FF);
         strokeWeight(hiddentoout[i] [j] * -10);
         line(70, 20 + 20 * i, 120, 20 + 20 * j);
       }
    }
    stroke(0);
    strokeWeight(1);
   }
   
   void randomize(){
    for(int i = 0; i <= 4; i++)
       for(int j = 0; j <= 7; j++) 
         intohidden[i] [j] =random(-1.00, 1.00);
    
    for(int i = 0; i <= 7; i++)
       for(int j = 0; j <= 3; j++)
         hiddentoout[i] [j] = random(-1.00, 1.00);
    
   }
   
   //------------------------------------------------------------------
   
   void mutate(float rate, int chance){
    for(int i = 0; i <= 4; i++){
       for(int j = 0; j <= 7; j++){ 
        if(int(random(chance + 1)) == chance) intohidden[i] [j] +=random(-1 * rate, rate);
        if(intohidden[i] [j] > 1) intohidden[i] [j] = 1;
        else if(intohidden[i] [j] < -1) intohidden[i] [j] = -1;
    }
    }
    
    for(int i = 0; i <= 7; i++){
       for(int j = 0; j <= 3; j++){
         if(int(random(chance + 1)) == chance) hiddentoout[i] [j] += random(-1 * rate, rate);
         if(hiddentoout[i] [j] > 1) hiddentoout[i] [j] = 1;
         else if(hiddentoout[i] [j] < -1) hiddentoout[i] [j] = -1;
    }
    
    }
   }

   
   //------------------------------------------------------------------
   
   int[] hidden = new int[8];
   boolean[] output = new boolean[4];
   float[] drive = new float[2];
   float a;
   
   float[] drive(float[] input){
     
     for(int i = 0; i <= 7; i++){
        a = 0;
        for (int j = 0; j < 4; j++) a += input[j] * intohidden[j] [i];
        if( a > 0) hidden[i] = 1;
        else hidden[i] = 0;
     }
     
     for(int i = 0; i <= 3; i++){
        a = 0;
        for (int j = 0; j <= 7; j++) a += hidden[j] * hiddentoout[j] [i];
        if(a > 0) output[i] = true;
        else output[i] = false;
     }
     if(output[0] == output[1]) drive[0] = 0;
     else if(output[0]) drive[0] = .5;
     else drive[0] = -.5;
     if(output[2] == output[3]) drive[1] = 0;
     else if(output[2]) drive[1] = .017;
     else drive[1] = -.017;
     
     return drive;
   }
   
   //----------------------------------------------------------------------
  
}
