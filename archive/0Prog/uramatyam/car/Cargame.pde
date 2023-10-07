Population population;
Track track;
Gates gates;
Brain[] parents;
Handler handler;

int maxalpha = 255, bgcolor = 255;

int dead_iteration = 20,
    parentcount    = 1000,
    version        = 2,
    psize          = 1000;

int generation=0, 
    bestindex=0, 
    latest_attempt=0, 
    iteration=0;
boolean ani_started=false, ani_ended=false, started = false, running = false;
Button my_button;
Slide my_slide;

ArrayList<Button> executable = new ArrayList<Button>();

void setup(){
  size(1200,800);
  //fullScreen();
  
  handler = new Handler();
  
  population = new Population(psize, 0);
  
  track = new Track(version);
  gates = new Gates(version);
  
  if (loadStrings("/Best_Weights/BestCar-attempt0-gen0.txt") != null)
    while (loadStrings("/Best_Weights/BestCar-attempt"+str(++latest_attempt)+"-gen0.txt") != null);
  
  println("Attempt:",latest_attempt);
  /*
  my_button = new Button("somebutton", 100, 100, 50, 50);
  my_slide = my_button.slide().setTime(1500)          // given in milliseconds
                                    .setMode("decelerate"); // possible modes: normal, whole (accelerate, then decelerate), accelerate, decelerate
  for (int i=0; i<5; ++i) my_slide.addDestination(random(0, width), random(0, height));
  my_slide.setStyle("united");*/
  
}
int c = 0;
//-----------------------------------------------------------

void draw(){
  background(bgcolor);
  
  //-- inside draw() --
  //my_button.show(); //Slide automatically starts
  
  handler.executeAll();
  println(c++);
  track.show();
  stroke(#92EA11);
  gates.show();
  
  fill(0);
  text("Attempt: "+latest_attempt, 20, 20); // Mi a tökömért nem jelenik meg mielőtt rányomok a lejátszásra??? Mert a szövegnél a fill számít, nem a stroke.
  text("Generation: "+generation, 20, 40);
  text("Iteration: "+iteration, 20, 60);
  
  if (!started) return;
  
  if (!population.dead){              // Go Cars, GO!!!
    if (running) population.AIdrive();
    population.show();
  }
  else if(!ani_started){             // All dead, starting over, animation starts
    generation++;
    population.getparents(parentcount);
    bestindex = population.bestindex;
    ani_started = true;
  }
  else if(!ani_ended) animation();   // Animation on the screen
  
  else {                             // Setting new Population, starting Cars again!
    population = new Population(psize, generation); 
    population.mutate(parents);
    ani_started = false;
    ani_ended = false;
  }
}

//------------------------------------------------------------

void animation(){
  if (running) {
    if (!population.go_small && population.size < 30)
      population.size += 1;
    else if(population.size > 1){
      population.size -= 1;
      population.go_small = true;
    }
    else if (population.go_small) ani_ended = true;
  }
  population.brains[bestindex].show(3);
  population.cars[bestindex].size = population.size;
  population.show();
}

//-------------------------

String date(){
  return str(year())+"-"+str(month())+"-"+str(day())+"-"+str(hour())+"-"+str(minute())+"-"+str(second())+"-"+str(millis()%1000);
}

int minusplus(float num){
  return (num==0 ? 1 : int(num / abs(num)));
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////





/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class Timer {
  long starttime;
  boolean started = false;
  
  void start(){
    starttime = millis();
    started = true;
  }
  
  long state(){
    return millis()-starttime;
  }
  
  void reset(){
    starttime = 0;
    started = false;
  }
}

//-----------------------------------------------------

float sumList(FloatList list) {
  return sumListUntil(list, list.size()-1);
}

float sumListUntil(FloatList list, int index) {
  float sum=0;
  for (int i=0; i<=index; ++i) sum += list.get(i);
  return sum;
}

float valueFromSum(FloatList list, int index) {
  return (list.size()==0 ? 0 : list.size()==1 || index == 0 ? list.get(0) : index<list.size() && index>0 ? list.get(index)-list.get(index-1) : 0);
}

void changeValue (ArrayList<Float> list, int index, float val) {
  list.remove(index);
  list.add(index, val);
}
