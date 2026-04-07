import 'package:flutter/material.dart';
import 'package:prostrationcounter/core/surface/nw_colors.dart';
import 'package:prostrationcounter/l10n/app_localizations.dart';

extension BuildContextX on BuildContext {
  AppLocalizations get text => AppLocalizations.of(this)!;
  ThemeData get theme => Theme.of(this);
  NwColors get appColors => theme.extension<NwColors>()!;
  Size get windowSize => MediaQuery.of(this).size;
  double get windowWidth => windowSize.width;
  double get windowHeight => windowSize.height;
  double get sizeConstant => (windowWidth + windowHeight) / 2;
  Orientation get appOrientation => MediaQuery.of(this).orientation;
  bool get orientationIsLandscape => appOrientation == Orientation.landscape;
  bool get orientationIsPortrait => appOrientation == Orientation.portrait;

  
  /// Returns a proportion of the screen height based on the orientation.
  ///
  /// [land] - The proportion of the screen height to return if the orientation is landscape.
  ///
  /// [port] - The proportion of the screen height to return if the orientation is portrait.
  double height({required double land, required double port}) =>
      orientationIsLandscape ? windowHeight * land : windowHeight * port;

  /// Returns a proportion of the screen width based on the orientation.
  ///
  /// [land] - The proportion of the screen width to return if the orientation is landscape.
  ///
  /// [port] - The proportion of the screen width to return if the orientation is portrait.
  double width({required double land, required double port}) =>
      orientationIsLandscape ? windowWidth * land : windowWidth * port;
}
