import 'package:flutter/material.dart';
import 'package:prostrationcounter/core/utility.dart';

class ProstrationsModel with ChangeNotifier {
  double _numberOfProstrations = 108;

  double get numberOfProstrations => _numberOfProstrations;

  void changeNumberOfProstrationsBy(double amount) {
    _numberOfProstrations = constrain(_numberOfProstrations + amount, min: 0);
  }

  void subtractOne() {
    if (_numberOfProstrations > 0) {
      _numberOfProstrations--;
      notifyListeners();
    }
  }
}