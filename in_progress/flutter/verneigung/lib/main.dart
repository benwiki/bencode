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
          changeAmountBy: (changeVal) => _changeGongIntervalBy(changeVal),
          getAmount: () => _gongInterval),
      const SizedBox(height: 35),
      AmountChanger(
          title: "Anzahl Niederwerfungen:",
          amountChangerValues: const [
            [1, -1],
            [10, -10],
            [108, -108]
          ],
          changeAmountBy: (changeVal) => _changeNumOfProstrationsBy(changeVal),
          getAmount: () => _numOfProstrations,
          breakAmountChangers: true),
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

class AmountChanger extends StatelessWidget {
  final Function(int) changeAmountBy;
  final Function getAmount;
  final String title;
  final String? unit;
  final List<List>? amountChangerValues;
  final bool breakAmountChangers;

  final normalTextStyle =
      const TextStyle(fontSize: 20, color: Color.fromARGB(255, 253, 207, 71));
  final amountTextStyle = const TextStyle(fontSize: 40, color: Colors.white);

  const AmountChanger(
      {super.key,
      required this.changeAmountBy,
      required this.getAmount,
      this.title = "Title",
      this.unit,
      this.amountChangerValues,
      this.breakAmountChangers = true});

  @override
  Widget build(BuildContext context) {
    return Column(children: [
      Row(mainAxisAlignment: MainAxisAlignment.center, children: [
        Text(title, style: normalTextStyle),
        const SizedBox(width: 20),
        Text(getAmount().toString(), style: amountTextStyle),
        if (unit != null) ...[
          const SizedBox(width: 20),
          Text(unit ?? '', style: normalTextStyle)
        ]
      ]),
      const SizedBox(height: 10),
      buildButtonMatrix()
    ]);
  }

  Widget buildButtonMatrix() {
    return Column(children: [
      for (int i = 0; i < (amountChangerValues?.length ?? 0); ++i) ...[
        if (i > 0) const SizedBox(height: 10),
        Row(mainAxisAlignment: MainAxisAlignment.center, children: [
          for (int j = 0; j < (amountChangerValues?[i].length ?? 0); ++j) ...[
            if (j > 0) const SizedBox(width: 10),
            buildAmountChangeButton(amountChangerValues?[i][j] ?? 0)
          ]
        ])
      ]
    ]);
  }

  Widget buildAmountChangeButton(int changeValue) {
    return SizedBox(
        width: 100,
        height: 45,
        child: ElevatedButton(
            onPressed: () => changeAmountBy(changeValue),
            style: ElevatedButton.styleFrom(
                shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(15))),
            child: Text('${changeValue > 0 ? '+' : ''}$changeValue',
                style: const TextStyle(
                    fontSize: 20, fontWeight: FontWeight.bold))));
  }
}
