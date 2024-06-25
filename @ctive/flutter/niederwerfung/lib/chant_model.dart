import 'package:flutter/material.dart';

class ChantModel with ChangeNotifier {
  bool _chantOn = false;

  bool get chantIsOn => _chantOn;

  void setChantState(bool state) {
    _chantOn = state;
    notifyListeners();
  }
}