import 'package:flutter/material.dart';
import 'package:niederwerfung/app_theme.dart';
import 'package:niederwerfung/context_extensions.dart';
import 'package:niederwerfung/homepage.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';

void main() {
  runApp(const NwApp());
}

class NwApp extends StatefulWidget {
  const NwApp({super.key});

  @override
  State<NwApp> createState() => NwAppState();

  static NwAppState? of(BuildContext context) => context.findAncestorStateOfType<NwAppState>();
}

class NwAppState extends State<NwApp> {
  Locale _locale = const Locale("en");

  void setLocale(Locale value) {
    setState(() {
      _locale = value;
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      onGenerateTitle: (BuildContext context) {
        return context.text.appName;
      },
      theme: appTheme,
      locale: _locale,
      localizationsDelegates: const [
        AppLocalizations.delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      supportedLocales: AppLocalizations.supportedLocales,
      home: Builder(
        builder: (context) => const HomePage(),
      ),
    );
  }
}
