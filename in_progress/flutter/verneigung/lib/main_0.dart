import 'package:flutter/material.dart';
import 'package:verneigung/utility.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Verneigung',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.amber,
          primary: Colors.black,
          surface: Colors.amber,
          background: const Color.fromARGB(255, 1, 36, 88),
        ),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'Verneigung'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _gongInterval = 10;
  bool _gongPlaying = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
        centerTitle: true,
      ),
      body: Column(crossAxisAlignment: CrossAxisAlignment.center, children: [
        const SizedBox(height: 20),
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text(
              "Gong-Intervall:",
              style: TextStyle(fontSize: 20, color: Colors.amber),
            ),
            const SizedBox(width: 20),
            Container(
                alignment: Alignment.center,
                width: sized(context, wRate: 0.1),
                child: Text(
                  "$_gongInterval",
                  style: const TextStyle(fontSize: 40, color: Colors.white),
                )),
            const SizedBox(width: 20),
            Column(children: [
              Row(children: [
                SizedBox(
                    width: 100,
                    height: 45,
                    child: ElevatedButton(
                      onPressed: () => _changeGongIntervalBy(1),
                      style: ElevatedButton.styleFrom(
                          shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(15))),
                      child: const Text('+1', style: TextStyle(fontSize: 20)),
                    )),
                const SizedBox(width: 10),
                SizedBox(
                    width: 100,
                    height: 45,
                    child: ElevatedButton(
                      onPressed: () => _changeGongIntervalBy(-1),
                      style: ElevatedButton.styleFrom(
                          shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(15))),
                      child: const Text('-1', style: TextStyle(fontSize: 20)),
                    ))
              ]),
              const SizedBox(height: 10),
              Row(children: [
                SizedBox(
                    width: 100,
                    height: 45,
                    child: ElevatedButton(
                      onPressed: () => _changeGongIntervalBy(10),
                      style: ElevatedButton.styleFrom(
                          shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(15))),
                      child: const Text('+10', style: TextStyle(fontSize: 20)),
                    )),
                const SizedBox(width: 10),
                SizedBox(
                    width: 100,
                    height: 45,
                    child: ElevatedButton(
                      onPressed: () => _changeGongIntervalBy(-10),
                      style: ElevatedButton.styleFrom(
                          shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(15))),
                      child: const Text('-10', style: TextStyle(fontSize: 20)),
                    ))
              ]),
            ])
          ],
        )
      ]),
      floatingActionButton: ElevatedButton(
        onPressed: _startGong,
        style: ElevatedButton.styleFrom(
            shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(10))),
        child: const Text(
          "Start Gong",
          style: TextStyle(
            fontSize: 25,
          ),
        ),
      ),
    );
  }

  _changeGongIntervalBy(int amount) {
    if (_gongInterval + amount > 99 || _gongInterval + amount < 1) return;
    setState(() => _gongInterval += amount);
  }

  _startGong() {
    _gongPlaying = true;
  }
}
