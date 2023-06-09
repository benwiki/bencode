import 'package:flutter/material.dart';
import 'package:niederwerfung/utility.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Niederwerfung',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.amber,
          primary: Colors.black,
          surface: Colors.amber,
          background: const Color.fromARGB(255, 1, 36, 88),
        ),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'Niederwerfung'),
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
  // bool _gongPlaying = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(
          widget.title,
          style: const TextStyle(fontSize: 30),
        ),
        centerTitle: true,
      ),
      body: Column(crossAxisAlignment: CrossAxisAlignment.center, children: [
        const SizedBox(height: 20),
        buildAmountChanger(
            title: "Gong-Intervall:",
            amountButtons: [
              [1, -1],
              [10, -10]
            ],
            changeAmountBy: (changeValue) =>
                setState(() => _changeGongIntervalBy(changeValue)),
            getAmount: () => _gongInterval)
      ]),
      floatingActionButton: ElevatedButton(
        onPressed: _startGong,
        style: ElevatedButton.styleFrom(
            shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(10))),
        child: const Text("Start Gong", style: TextStyle(fontSize: 25)),
      ),
    );
  }

  Widget buildAmountChanger(
      {required Function changeAmountBy,
      required Function getAmount,
      String title = "Title",
      List<List>? amountButtons}) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Text(title, style: const TextStyle(fontSize: 20, color: Colors.amber)),
        const SizedBox(width: 20),
        Container(
            alignment: Alignment.center,
            width: sized(context, wRate: 0.1),
            child: Text(getAmount().toString(),
                style: const TextStyle(fontSize: 40, color: Colors.white))),
        const SizedBox(width: 20),
        Column(children: [
          for (int i = 0; i < (amountButtons?.length ?? 0); ++i) ...[
            if (i > 0) const SizedBox(height: 10),
            Row(children: [
              for (int j = 0; j < (amountButtons?[i].length ?? 0); ++j) ...[
                if (j > 0) const SizedBox(width: 10),
                SizedBox(
                    width: 100,
                    height: 45,
                    child: ElevatedButton(
                      onPressed: () =>
                          changeAmountBy(amountButtons?[i][j] ?? 0),
                      style: ElevatedButton.styleFrom(
                          shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(15))),
                      child: Text(
                          '${amountButtons?[i][j] > 0 ? '+' : ''}${amountButtons?[i][j]}',
                          style: const TextStyle(fontSize: 20)),
                    ))
              ]
            ])
          ]
        ])
      ],
    );
  }

  _changeGongIntervalBy(int amount) {
    if (_gongInterval + amount > 99 || _gongInterval + amount < 1) return;
    setState(() => _gongInterval += amount);
  }

  _startGong() {
    // _gongPlaying = true;
  }
}
