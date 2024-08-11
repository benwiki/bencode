import 'package:flutter/material.dart';
import 'package:niederwerfung/core/surface/app_theme.dart';
import 'package:niederwerfung/model/chant_model.dart';
import 'package:niederwerfung/core/context_extension.dart';
import 'package:niederwerfung/homepage.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:niederwerfung/model/gong_interval_model.dart';
import 'package:niederwerfung/model/prostrations_model.dart';
import 'package:provider/provider.dart';

void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => ProstrationsModel()),
        ChangeNotifierProvider(create: (_) => ChantModel()),
        ChangeNotifierProvider(create: (_) => GongIntervalModel()),
      ],
      child: const NwApp(),
    ),
  );
}

class NwApp extends StatefulWidget {
  const NwApp({super.key});

  @override
  State<NwApp> createState() => NwAppState();

  static NwAppState? of(BuildContext context) =>
      context.findAncestorStateOfType<NwAppState>();
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
      debugShowCheckedModeBanner: false,
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
