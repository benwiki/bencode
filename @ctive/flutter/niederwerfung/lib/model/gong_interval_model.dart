import 'package:flutter/material.dart';
import 'package:prostrationcounter/core/utility.dart';
import 'package:shared_preferences/shared_preferences.dart';

class GongIntervalModel with ChangeNotifier {
  double _gongInterval = 10;
  bool _loaded = false;

  double get gongInterval => _gongInterval;
  bool get loaded => _loaded;

  static const String _prefsKey = 'gong_interval';

  GongIntervalModel();

  Future<void> init() async {
    await _loadFromPrefs();
  }

  void changeValueBy(double amount) async {
    _gongInterval = constrain(_gongInterval + amount, min: 1, max: 99);
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    prefs.setDouble(_prefsKey, _gongInterval);
  }

  Future<void> _loadFromPrefs() async {
    final prefs = await SharedPreferences.getInstance();
    final value = prefs.getDouble(_prefsKey);
    if (value != null) {
      _gongInterval = value;
    }
    _loaded = true;
    notifyListeners();
  }
}