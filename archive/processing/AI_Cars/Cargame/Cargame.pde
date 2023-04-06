Population population;
Track track;
Gates gates;
Brain[] parents;

int generation = 0;

void setup()
{
 size(800,800);
 population = new Population(1000, 0);
 track = new Track();
 gates = new Gates();
}

//-----------------------------------------------------------

void draw()
{
  background(255);
  
  track.show();
  
  stroke(#92EA11);
  gates.show();
  stroke(0);
  text(generation, 20, 20);
  text(millis(), 20, 40);
  
  if(!population.dead){
  population.AIdrive();
  population.show();
  }
  
  else{
    generation++;
    println(max(population.scores));
    parents = population.getparents(100);
   population = new Population(1000, generation); 
   population.mutate(parents);
   //population.randomize();
  }  
}

//------------------------------------------------------------
