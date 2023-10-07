class InputHandler {
  Slider markedSlider; 
  ArrayList<Slider> sliders = new ArrayList();
  
  InputHandler() {};
  
  void addSlider(Slider slider) {
    sliders.add(slider);
  }
  
  void updateSlider() {
    if (markedSlider != null) {
      markedSlider.setToMousePos();
    }
  }
  
  void handleMouse() {
    for (Slider slider: sliders) {
      if (slider.mouseOver()) {
        markedSlider = slider;
        return;
      }
    }
    markedSlider = null;
  }
}
