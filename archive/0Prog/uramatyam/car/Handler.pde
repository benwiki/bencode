
class Handler {
  
  Button startingPoint, play, pause, stop;
  boolean previously_pressed = false, 
          draggingSP = false; // dragging Starting Point
  
  Handler () {
    startingPoint = new Button ("startingpoint", 150, 120, 100, 100) .setShape("oval")
                    .setFillColor(bgcolor).setActiveFillColor(bgcolor).setStrokeColor(bgcolor)
                    .setActiveStrokeColor(color(0, 150, 0));
    
    play = new Button("play", width - width/9*2.5, height-height/10, height/10, height/10)
           .setFillColor(bgcolor).setActiveFillColor(bgcolor).setStrokeColor(color(0)).setActiveStrokeColor(color(0, 200, 0));
    pause = new Button("pause", width - width/6, height-height/10, height/10, height/10)
            .setFillColor(bgcolor).setActiveFillColor(bgcolor).setStrokeColor(color(0)).setActiveStrokeColor(color(200, 200, 0));
    stop = new Button("stop", width - width/9/2, height-height/10, height/10, height/10)
           .setFillColor(bgcolor).setActiveFillColor(bgcolor).setStrokeColor(color(0)).setActiveStrokeColor(color(200, 0, 0));
           
    play.setRectEdge(play.w);
    pause.setRectEdge(pause.w);
    stop.setRectEdge(stop.w);
    
    startingPoint.addSign().setName("SP").setType("startingpoint").setColors(color(0), color(0, 150, 0));
    play.addSign().setName("play").setType("play").setColors(color(0), play.ascolor);
    pause.addSign().setName("pause").setType("pause").setColors(color(0), pause.ascolor);
    stop.addSign().setName("stop").setType("stop").setColors(color(0), stop.ascolor);
    
    executable.add(startingPoint);
    executable.add(play);
    executable.add(pause);
    executable.add(stop);
  }
  //-------------------------------------------------------------------------------------------------------
   
  void executeAll() {
    
    if (mousePressed){
      
      if (!previously_pressed && startingPoint.isOver()) draggingSP = true;
      
      previously_pressed = true;
      
      if (draggingSP) startingPoint.jump(mouseX, mouseY);
    }
    
    else if (previously_pressed){
      
      if (draggingSP && !started)
        for (Car car: population.cars)
          car.pos.set(startingPoint.pos);
      draggingSP = false;
        
      for (Button button: executable)
        if (button.isOver() && button.activated) _runCommand(button.type);
      previously_pressed = false;
    }
    
    for (Button button: executable)
      if (button.visible) button.show();
  }
  //----------------------------------------------
  
  private void _runCommand (String type) {
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    if (type == "play"){
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
      started = true;
      running = true;
    }
    
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    else if (type == "pause"){
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
      running = false;
    }
    
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    else if (type == "stop"){
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
      started = false;
      running = false;
      generation = 0;
      iteration = 0;
      population = new Population(psize, generation);
      ++latest_attempt;
      ani_started = false;
      ani_ended = false;
    }
  }
  
};
