import 'package:niederwerfung/generated/fonts.gen.dart';
import 'package:flutter/material.dart';

abstract final class TextStyles {
  static const _lalezarHeight = 0.7;

  static const titleExtraLarge = TextStyle(
    fontFamily: FontFamily.lalezar,
    fontSize: 40,
  );

  static const titleLarge = TextStyle(
    fontFamily: FontFamily.lalezar,
    fontSize: 36,
  );

  static const titleMedium = TextStyle(
    fontFamily: FontFamily.lalezar,
    fontSize: 20,
  );

  static const titleSmall = TextStyle(
    fontFamily: FontFamily.openSans,
    fontWeight: FontWeight.w800,
    fontSize: 17,
  );

  static const titleExtraSmall = TextStyle(
    fontFamily: FontFamily.openSans,
    fontWeight: FontWeight.w800,
    fontSize: 14,
  );

  static const boldText = TextStyle(
    fontFamily: FontFamily.openSans,
    fontWeight: FontWeight.w700,
    fontSize: 12,
  );

  static const smallRegularTitle = TextStyle(
    fontFamily: FontFamily.lalezar,
    fontSize: 16,
    height: _lalezarHeight,
  );

  static const baseText = TextStyle(
    fontFamily: FontFamily.openSans,
    fontSize: 16,
    height: 1,
  );

  static const regularText = TextStyle(
    fontFamily: FontFamily.openSans,
    fontWeight: FontWeight.w400,
    fontSize: 12,
  );

  static const smallRegularText = TextStyle(
    fontFamily: FontFamily.openSans,
    fontWeight: FontWeight.w400,
    fontSize: 10,
  );
}
