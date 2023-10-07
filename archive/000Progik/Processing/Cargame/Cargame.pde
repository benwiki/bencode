Population population;
Track track;
Gates gates;
Brain[] parents;
Handler handler;

int maxalpha = 255, bgcolor = 255;

int dead_iteration = 15,
    parentcount=10,
    version = 2,
    psize = 1000;

int generation=0, 
    bestindex=0, 
    latest_attempt=0, 
    iteration=0;
boolean ani_started=false, ani_ended=false, paused = true, started = false;

ArrayList<Button> executable = new ArrayList<Button>();

/* IMPROVEMENTS MADE
~2020. 08. 27.:
  1. Gombok létrehozása
  2. Iteráció az idő helyett
  3. Handler kidolgozása
  4. startingPoint koordinátáiból indulnak a kocsik
  
~2020. 08. 15.:
  1. kódrendezgetés, example írása
  2. a Slide objektum ha nincs megadva destination és futtatni akarod, kitörli magát.
  3. Itt is jöhet a handler, mert nehogy már a főfájlban legyen minden
  
~2020. 08. 14.:
  1. tegnap csak egy destination-nel próbáltam ki, úgy ment jól. Ma rengeteget dolgoztam hogy összejöjjön több destiantion-nel - és sikerült.
  2. a Slide.run() elejére tettem a setupot, így bármit módosíthatsz rajta mielőtt elindítod, nem fuckolódik up.
  
~2020. 08. 13.:
  1. kipróbáltam, jól csináltam mindent, csak a setTime-ot vagy setMode-ot az addDestination előtt kellene meghívni, különben hibát okoz.  hibajavítás! 
  
~2020. 08. 12-13.:
  1. Slide, Movements, Rotation, SizeChange class létrehozása
  2. sz*rakodás a Slide-dal, hogy működjön
  
~2020. 08. 11.:
  1. Signs class hozzáadása a Sign filehoz - sokkal kezelhetőbbek a jelek
  2. Jeleknek típusuk ÉS nevük van, könnyebb azonosítás
  3. Button classban "builder-function"-ök
  4. startingPoint gomb
  5. whitespace a kódban, rendezgetés
*/

/* POSSIBLE IMPROVEMENTS
------------------------
1. gombbal való indítás, leállítás, szüneteltetés  ✓ ✓ ✓
  - egyáltalán vmi kezelőfelület, menü: onnan indítható a program vagy a trackdesigner
2. manuális kezdőpozíció  ✓ ✓ ✓
3. trackdesigner: trackpontok gombbal húzkod��������sa
4. ne időt nézzünk, hanem iterációt!!!  ✓ ✓ ✓ kész :)
5. kocsi brain megtekintés (föléhúzott egér) 
6. kódrendezés - sokkal rövidebben meg lehet oldani a függvények működését
7. Slide-ot valahogy rendezd mán el!!! 
  - külön 2 függvény a separated és united style-nak
------------------------------------
*/

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
}

//-----------------------------------------------------------

void draw(){
  background(bgcolor);
  
  handler.executeAll();
  
  track.show();
  stroke(#92EA11);
  gates.show();
  
  stroke(0);
  text(generation, 20, 20);
  //text(millis(), 20, 40);
  

  if (!population.dead){              // Go Cars, GO!!!
    if (started) population.AIdrive();
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
  if (!population.go_small && population.size < 30)
    population.size += 1;
  else if(population.size > 1){
    population.size -= 1;
    population.go_small = true;
  }
  else if (population.go_small) ani_ended = true;
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

float sumList(ArrayList<Float> list) {
  return sumListUntil(list, list.size()-1);
}

float sumListUntil(ArrayList<Float> list, int index) {
  float sum=0;
  for (int i=0; i<=index; ++i) sum += list.get(i);
  return sum;
}

float valueFromSum(ArrayList<Float> list, int index) {
  return (list.size()==0 ? 0 : list.size()==1 || index == 0 ? list.get(0) : index<list.size() && index>0 ? list.get(index)-list.get(index-1) : 0);
}

void changeValue (ArrayList<Float> list, int index, float val) {
  list.remove(index);
  list.add(index, val);
}
