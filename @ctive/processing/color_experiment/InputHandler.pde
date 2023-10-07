class InputHandler {
  Slider markedSlider = null; 
  ArrayList<Slider> sliders = new ArrayList<Slider>();
  
  InputHandler() {};
  
  void addSlider(Slider slider) {
    sliders.add(slider);
  }
  
  void updateSlider() {
    if (markedSlider != null) {
      markedSlider.setToMousePos();
    }
  }
  
  void handlePress() {
    for (Slider slider: sliders) {
      if (slider.mouseOver()) {
        markedSlider = slider;
        break;
      }
    } 
  }
  
  void handleRelease() {
    markedSlider = null;
  }
}
