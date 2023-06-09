import 'package:flutter/material.dart';
import 'package:niederwerfung/amount_changer.dart';
import 'package:niederwerfung/utility.dart';

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _gongInterval = 10, _numOfProstrations = 108;
  // bool _gongPlaying = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: buildAppBar(),
      body: buildBody(context),
      floatingActionButton: buildFAB(),
    );
  }

  AppBar buildAppBar() {
    return AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title, style: const TextStyle(fontSize: 30)),
        centerTitle: true);
  }

  Widget buildBody(BuildContext context) {
    return Column(crossAxisAlignment: CrossAxisAlignment.center, children: [
      const SizedBox(height: 20),
      AmountChanger(
          title: "Gong-Intervall:",
          unit: "Sek.",
          amountChangerValues: const [
            [1, -1],
            [10, -10]
          ],
          changeAmountBy: (value) => _changeGongIntervalBy(value),
          getAmount: () => _gongInterval),
      const SizedBox(height: 35),
      AmountChanger(
          title: "Anzahl Niederwerfungen:",
          amountChangerValues: const [
            [1, -1],
            [10, -10],
            [108, -108]
          ],
          changeAmountBy: (value) => _changeNumOfProstrationsBy(value),
          getAmount: () => _numOfProstrations),
    ]);
  }

  Widget buildFAB() {
    return SizedBox(
        width: sized(context, wRate: 0.4),
        height: sized(context, hRate: 0.07),
        child: ElevatedButton(
            onPressed: _startGong,
            style: ElevatedButton.styleFrom(
                backgroundColor: Colors.red[900],
                foregroundColor: Colors.white,
                side: const BorderSide(width: 3, color: Colors.white),
                shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10))),
            child: const Text("Start Gong", style: TextStyle(fontSize: 25))));
  }

  _changeGongIntervalBy(int amount) {
    if (isNotBetween(_gongInterval + amount, 1, 99)) return;
    setState(() => _gongInterval += amount);
  }

  _changeNumOfProstrationsBy(int amount) {
    if (isNotBetween(_numOfProstrations + amount, 1, 9999)) return;
    setState(() => _numOfProstrations += amount);
  }

  _startGong() {
    // _gongPlaying = true;
  }
}
