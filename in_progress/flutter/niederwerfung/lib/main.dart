import 'package:flutter/material.dart';
import 'package:niederwerfung/homepage.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    const Color mainColor = Color.fromARGB(255, 252, 218, 118);
    const Color backgroundColor = Color.fromARGB(255, 1, 25, 62);

    return MaterialApp(
      title: AppLocalizations.of(context)!.appName,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: mainColor,
          primary: backgroundColor,
          surface: mainColor,
          background: backgroundColor,
        ),
        useMaterial3: true,
      ),
      localizationsDelegates: const [
        AppLocalizations.delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      supportedLocales: AppLocalizations.supportedLocales,
      home: MyHomePage(title: AppLocalizations.of(context)!.appName),
    );
  }
}
