import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import 'package:ukraine_app/data.dart';
import 'package:ukraine_app/homepage.dart';

String lang = "ukr", country = "hungary", objective = "get-help";
String showLang = langByLang[lang],
    showCountry = countryByLang[lang][country],
    showObjective = objectiveByLang[lang][objective];

String webpageURL = "https://ukrainehelp.hu/uk";
String defaultURL = "https://blank.org";

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await SystemChrome.setPreferredOrientations(
      [DeviceOrientation.portraitUp, DeviceOrientation.portraitDown]);

  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Get help, give help',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      routes: {'/': (context) => const HomePage()},
    );
  }
}
