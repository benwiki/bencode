import 'package:niederwerfung/core/surface/app_colors.dart';
import 'package:flutter/material.dart';

@immutable
class NwColors extends ThemeExtension<NwColors> {
  const NwColors({
    required this.beecoYellow,
    required this.beecoOrange,
    required this.blackStrong,
    required this.beecoGreen,
    required this.beecoPink,
    required this.whiteStrong,
    required this.beecoBgMain,
    required this.butterLight,
    required this.yellowLight,
    required this.yellowVeryLight,
    required this.butterMedium,
    required this.brownStrong,
    required this.brownMedium,
    required this.brownLight,
    required this.greenVivid,
    required this.greenMedium,
    required this.orangeMedium,
    required this.redStrong,
    required this.redVivid,
    required this.blueDeep,
    required this.blueStrong,
    required this.blueMedium,
    required this.blueLight,
    required this.blueExtraLight,
    required this.purpleMedium,
    required this.lightGrey,
  });
  final Color beecoYellow;
  final Color beecoOrange;
  final Color blackStrong;
  final Color beecoGreen;
  final Color beecoPink;
  final Color whiteStrong;
  final Color beecoBgMain;
  final Color butterLight;
  final Color yellowLight;
  final Color yellowVeryLight;
  final Color butterMedium;
  final Color brownStrong;
  final Color brownMedium;
  final Color brownLight;
  final Color greenVivid;
  final Color greenMedium;
  final Color orangeMedium;
  final Color redStrong;
  final Color redVivid;
  final Color blueDeep;
  final Color blueStrong;
  final Color blueMedium;
  final Color blueLight;
  final Color blueExtraLight;
  final Color purpleMedium;
  final Color lightGrey;

  static const standard = NwColors(
    beecoYellow: AppColors.beecoYellow,
    beecoOrange: AppColors.beecoOrange,
    blackStrong: AppColors.blackStrong,
    beecoGreen: AppColors.beecoGreen,
    beecoPink: AppColors.beecoPink,
    whiteStrong: AppColors.whiteStrong,
    beecoBgMain: AppColors.beecoBgMain,
    butterLight: AppColors.butterLight,
    yellowLight: AppColors.yellowLight,
    yellowVeryLight: AppColors.yellowVeryLight,
    butterMedium: AppColors.butterMedium,
    brownStrong: AppColors.brownStrong,
    brownMedium: AppColors.brownMedium,
    brownLight: AppColors.brownLight,
    greenVivid: AppColors.greenVivid,
    greenMedium: AppColors.greenMedium,
    orangeMedium: AppColors.orangeMedium,
    redStrong: AppColors.redStrong,
    redVivid: AppColors.redVivid,
    blueDeep: AppColors.blueDeep,
    blueStrong: AppColors.blueStrong,
    blueMedium: AppColors.blueMedium,
    blueLight: AppColors.blueLight,
    blueExtraLight: AppColors.blueExtraLight,
    purpleMedium: AppColors.purpleMedium,
    lightGrey: AppColors.lightGrey,
  );
  @override
  ThemeExtension<NwColors> copyWith({
    Color? beecoYellow,
    Color? beecoOrange,
    Color? blackStrong,
    Color? beecoGreen,
    Color? beecoPink,
    Color? whiteStrong,
    Color? beecoBgMain,
    Color? butterLight,
    Color? yellowLight,
    Color? yellowVeryLight,
    Color? butterMedium,
    Color? brownStrong,
    Color? brownMedium,
    Color? brownLight,
    Color? greenVivid,
    Color? greenMedium,
    Color? orangeMedium,
    Color? redStrong,
    Color? redVivid,
    Color? blueDeep,
    Color? blueStrong,
    Color? blueMedium,
    Color? blueLight,
    Color? blueExtraLight,
    Color? purpleMedium,
    Color? lightGrey,
  }) {
    return NwColors(
      beecoYellow: beecoYellow ?? this.beecoYellow,
      beecoOrange: beecoOrange ?? this.beecoOrange,
      blackStrong: blackStrong ?? this.blackStrong,
      beecoGreen: beecoGreen ?? this.beecoGreen,
      beecoPink: beecoPink ?? this.beecoPink,
      whiteStrong: whiteStrong ?? this.whiteStrong,
      beecoBgMain: beecoBgMain ?? this.beecoBgMain,
      butterLight: butterLight ?? this.butterLight,
      yellowLight: yellowLight ?? this.yellowLight,
      yellowVeryLight: yellowVeryLight ?? this.yellowVeryLight,
      butterMedium: butterMedium ?? this.butterMedium,
      brownStrong: brownStrong ?? this.brownStrong,
      brownMedium: brownMedium ?? this.brownMedium,
      brownLight: brownLight ?? this.brownLight,
      greenVivid: greenVivid ?? this.greenVivid,
      greenMedium: greenMedium ?? this.greenMedium,
      orangeMedium: orangeMedium ?? this.orangeMedium,
      redStrong: redStrong ?? this.redStrong,
      redVivid: redVivid ?? this.redVivid,
      blueDeep: blueDeep ?? this.blueDeep,
      blueStrong: blueStrong ?? this.blueStrong,
      blueMedium: blueMedium ?? this.blueMedium,
      blueLight: blueLight ?? this.blueLight,
      blueExtraLight: blueExtraLight ?? this.blueExtraLight,
      purpleMedium: purpleMedium ?? this.purpleMedium,
      lightGrey: lightGrey ?? this.lightGrey,
    );
  }

  @override
  ThemeExtension<NwColors> lerp(
    covariant ThemeExtension<NwColors>? other,
    double t,
  ) {
    if (other is! NwColors) return this;
    return NwColors(
      beecoYellow: Color.lerp(beecoYellow, other.beecoYellow, t) ?? beecoYellow,
      beecoOrange: Color.lerp(beecoOrange, other.beecoOrange, t) ?? beecoOrange,
      blackStrong: Color.lerp(blackStrong, other.blackStrong, t) ?? blackStrong,
      beecoGreen: Color.lerp(beecoGreen, other.beecoGreen, t) ?? beecoGreen,
      beecoPink: Color.lerp(beecoPink, other.beecoPink, t) ?? beecoPink,
      whiteStrong: Color.lerp(whiteStrong, other.whiteStrong, t) ?? whiteStrong,
      beecoBgMain: Color.lerp(beecoBgMain, other.beecoBgMain, t) ?? beecoBgMain,
      butterLight: Color.lerp(butterLight, other.butterLight, t) ?? butterLight,
      yellowLight: Color.lerp(yellowLight, other.yellowLight, t) ?? yellowLight,
      yellowVeryLight: Color.lerp(yellowVeryLight, other.yellowVeryLight, t) ??
          yellowVeryLight,
      butterMedium:
          Color.lerp(butterMedium, other.butterMedium, t) ?? butterMedium,
      brownStrong: Color.lerp(brownStrong, other.brownStrong, t) ?? brownStrong,
      brownMedium: Color.lerp(brownMedium, other.brownMedium, t) ?? brownMedium,
      brownLight: Color.lerp(brownLight, other.brownLight, t) ?? brownLight,
      greenVivid: Color.lerp(greenVivid, other.greenVivid, t) ?? greenVivid,
      greenMedium: Color.lerp(greenMedium, other.greenMedium, t) ?? greenMedium,
      orangeMedium:
          Color.lerp(orangeMedium, other.orangeMedium, t) ?? orangeMedium,
      redStrong: Color.lerp(redStrong, other.redStrong, t) ?? redStrong,
      redVivid: Color.lerp(redVivid, other.redVivid, t) ?? redVivid,
      blueDeep: Color.lerp(blueDeep, other.blueDeep, t) ?? blueDeep,
      blueStrong: Color.lerp(blueStrong, other.blueStrong, t) ?? blueStrong,
      blueMedium: Color.lerp(blueMedium, other.blueMedium, t) ?? blueMedium,
      blueLight: Color.lerp(blueLight, other.blueLight, t) ?? blueLight,
      blueExtraLight:
          Color.lerp(blueExtraLight, other.blueExtraLight, t) ?? blueExtraLight,
      purpleMedium:
          Color.lerp(purpleMedium, other.purpleMedium, t) ?? purpleMedium,
      lightGrey: Color.lerp(lightGrey, other.lightGrey, t) ?? lightGrey,
    );
  }
}
