import 'package:flutter/material.dart';
import 'package:niederwerfung/homepage.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Niederwerfungen',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color.fromARGB(255, 253, 207, 71),
          primary: const Color.fromARGB(255, 1, 25, 62),
          surface: const Color.fromARGB(255, 253, 207, 71),
          background: const Color.fromARGB(255, 1, 25, 62),
        ),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'Niederwerfungen'),
    );
  }
}
