import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:niederwerfung/app_colors.dart';
import 'package:niederwerfung/nw_colors.dart';
import 'package:niederwerfung/nw_text_styles.dart';
import 'package:niederwerfung/text_styles.dart';
import 'package:niederwerfung/generated/fonts.gen.dart';

const lightYellowOverlayStyle = SystemUiOverlayStyle(
  statusBarIconBrightness: Brightness.dark,
  statusBarColor: Colors.transparent,
  systemNavigationBarColor: AppColors.beecoBgMain,
  systemNavigationBarIconBrightness: Brightness.dark,
);

final appTheme = ThemeData(
  useMaterial3: true,
  fontFamily: FontFamily.openSans,
  appBarTheme: const AppBarTheme(
    backgroundColor: AppColors.beecoBgMain,
    elevation: 0,
    shadowColor: Colors.transparent,
    surfaceTintColor: Colors.transparent,
    foregroundColor: Colors.black,
    titleTextStyle: TextStyle(
      fontFamily: FontFamily.lalezar,
      letterSpacing: 0.5,
      fontSize: 26,
      height: 2,
      color: Colors.black,
    ),
  ),
  cupertinoOverrideTheme:
      const NoDefaultCupertinoThemeData(primaryColor: Colors.black),
  scaffoldBackgroundColor: AppColors.beecoBgMain,
  tabBarTheme: TabBarTheme(
    splashFactory: NoSplash.splashFactory,
    indicatorColor: Colors.black,
    indicatorSize: TabBarIndicatorSize.tab,
    labelStyle: TextStyles.titleMedium.copyWith(color: Colors.black),
    unselectedLabelStyle: TextStyles.titleMedium.copyWith(
      color: AppColors.grey,
    ),
    overlayColor: WidgetStateProperty.resolveWith(
      (states) {
        return states.contains(WidgetState.pressed) ? Colors.black12 : null;
      },
    ),
  ),
  textSelectionTheme: const TextSelectionThemeData(
    cursorColor: Colors.black,
    selectionColor: Colors.black38,
    selectionHandleColor: Colors.black,
  ),
  navigationBarTheme: NavigationBarThemeData(
    labelTextStyle: MaterialStateProperty.all(
      const TextStyle(
        fontFamily: FontFamily.lalezar,
        fontSize: 14,
      ),
    ),
  ),
  datePickerTheme: DatePickerThemeData(
    backgroundColor: AppColors.beecoBgMain,
    todayBackgroundColor: const MaterialStatePropertyAll(AppColors.beecoYellow),
    todayBorder: BorderSide.none,
    rangeSelectionBackgroundColor: Colors.amber,
    todayForegroundColor: const MaterialStatePropertyAll(Colors.black),
    cancelButtonStyle: TextButton.styleFrom(
      foregroundColor: AppColors.blackStrong,
    ),
    confirmButtonStyle: TextButton.styleFrom(
      foregroundColor: AppColors.blackStrong,
    ),
  ),
  snackBarTheme: const SnackBarThemeData(
    elevation: 0,
    backgroundColor: Colors.transparent,
  ),
  extensions: const [
    NwColors.standard,
    NwTextStyles.standard,
  ],
);
