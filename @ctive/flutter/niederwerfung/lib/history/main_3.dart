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
          background: const Color.fromARGB(255, 1, 25, 62),
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
      AmountChangerMatrix(
          title: "Gong-Intervall:",
          amountChangerValues: const [
            [1, -1],
            [10, -10]
          ],
          changeAmountBy: (changeValue) =>
              setState(() => _changeGongIntervalBy(changeValue)),
          getAmount: () => _gongInterval)
    ]);
  }

  Widget buildFAB() {
    return ElevatedButton(
        onPressed: _startGong,
        style: ElevatedButton.styleFrom(
            shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(10))),
        child: const Text("Start Gong", style: TextStyle(fontSize: 25)));
  }

  _changeGongIntervalBy(int amount) {
    if (_gongInterval + amount > 99 || _gongInterval + amount < 1) return;
    setState(() => _gongInterval += amount);
  }

  _startGong() {
    // _gongPlaying = true;
  }
}

class AmountChangerMatrix extends StatelessWidget {
  final Function changeAmountBy, getAmount;
  final String title;
  final List<List>? amountChangerValues;

  const AmountChangerMatrix(
      {super.key,
      required this.changeAmountBy,
      required this.getAmount,
      this.title = "Title",
      this.amountChangerValues});

  @override
  Widget build(BuildContext context) {
    return Row(mainAxisAlignment: MainAxisAlignment.center, children: [
      buildTitleWidget(),
      const SizedBox(width: 20),
      buildAmountWidget(context),
      const SizedBox(width: 20),
      buildButtonMatrix()
    ]);
  }

  Widget buildTitleWidget() {
    return Text(title,
        style: const TextStyle(fontSize: 20, color: Colors.amber));
  }

  Widget buildAmountWidget(BuildContext context) {
    return Container(
        alignment: Alignment.center,
        width: sized(context, wRate: 0.1),
        child: Text(getAmount().toString(),
            style: const TextStyle(fontSize: 40, color: Colors.white)));
  }

  Widget buildButtonMatrix() {
    return Column(children: [
      for (int i = 0; i < (amountChangerValues?.length ?? 0); ++i) ...[
        if (i > 0) const SizedBox(height: 10),
        Row(children: [
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
                style: const TextStyle(fontSize: 20))));
  }
}
