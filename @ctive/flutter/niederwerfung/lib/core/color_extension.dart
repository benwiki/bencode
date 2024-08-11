import 'package:flutter/material.dart';

extension ColorX on Color {
  Color darken(double amount) {
    assert(amount >= 0 && amount <= 1);
    return Color.fromARGB(
      alpha,
      (red * (1 - amount)).round(),
      (green * (1 - amount)).round(),
      (blue * (1 - amount)).round(),
    );
  }
}