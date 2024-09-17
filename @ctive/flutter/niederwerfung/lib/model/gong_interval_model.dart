import 'package:flutter/material.dart';
import 'package:prostrationcounter/core/utility.dart';

class GongIntervalModel with ChangeNotifier {
  double _gongInterval = 10;

  double get gongInterval => _gongInterval;

  void changeValueBy(double amount) {
    _gongInterval = constrain(_gongInterval + amount, min: 1, max: 99);
  }
}