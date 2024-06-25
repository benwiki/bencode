import 'package:flutter/material.dart';
import 'package:niederwerfung/utility.dart';

class ProstrationsModel with ChangeNotifier {
  double _numberOfProstrations = 0;

  double get numberOfProstrations => _numberOfProstrations;

  void changeNumberOfProstrationsBy(double amount) {
    _numberOfProstrations = constrain(_numberOfProstrations + amount, min: 1);
  }

  void subtractOne() {
    if (_numberOfProstrations > 0) {
      _numberOfProstrations--;
      notifyListeners();
    }
  }
}