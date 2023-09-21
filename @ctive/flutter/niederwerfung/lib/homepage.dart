import 'package:flutter/material.dart';
import 'package:niederwerfung/amount_changer.dart';
import 'package:niederwerfung/chant_controller.dart';
import 'package:niederwerfung/utility.dart';

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _gongInterval = 10, _numberOfProstrations = 108;
  Locale _locale = const Locale("en");
  // bool _gongPlaying = false;

  @override
  Widget build(BuildContext context) {
    return Localizations.override(
        context: context,
        locale: _locale,
        child: Scaffold(
          appBar: buildAppBar(),
          body: buildBody(context),
          floatingActionButton: buildFAB(),
          endDrawer: buildLanguageChangeButton(),
        ));
  }

  AppBar buildAppBar() {
    return AppBar(
        backgroundColor: Theme.of(context).colorScheme.surface,
        title: Text(widget.title, style: const TextStyle(fontSize: 30)),
        centerTitle: true);
  }

  Widget buildBody(BuildContext context) {
    return Column(crossAxisAlignment: CrossAxisAlignment.center, children: [
      //
      const SizedBox(height: 20),
      //
      AmountChanger(
          title: "Gong-Intervall:",
          unit: "Sek.",
          amountChangerValues: const [
            [-1, 1],
            [-10, 10]
          ],
          changeAmountBy: (value) => _changeGongIntervalBy(value),
          getAmount: () => _gongInterval),
      //
      const SizedBox(height: 35),
      //
      AmountChanger(
          title: "Anzahl Niederw.:",
          amountChangerValues: const [
            [-1, 1],
            [-10, 10],
            [-108, 108]
          ],
          changeAmountBy: (value) => _changeNumberOfProstrationsBy(value),
          getAmount: () => _numberOfProstrations),
      //
      const SizedBox(height: 35),
      //
      const ChantController()
    ]);
  }

  Widget buildFAB() {
    return SizedBox(
        width: 120,
        height: 50,
        child: ElevatedButton(
            onPressed: _startGong,
            style: ElevatedButton.styleFrom(
                backgroundColor: Colors.red[900],
                foregroundColor: Colors.white,
                side: const BorderSide(width: 3, color: Colors.white),
                shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10))),
            child: const Text("Start", style: TextStyle(fontSize: 25))));
  }

  Widget buildLanguageChangeButton() {
    return IconButton(
        onPressed: () => setState(
            () => _locale = Locale(_locale.languageCode == 'en' ? 'de' : 'en')),
        icon: const Icon(Icons.language));
  }

  _changeGongIntervalBy(int amount) {
    if (isNotBetween(_gongInterval + amount, 1, 99)) return;
    setState(() => _gongInterval += amount);
  }

  _changeNumberOfProstrationsBy(int amount) {
    if (isNotBetween(_numberOfProstrations + amount, 1, 9999)) return;
    setState(() => _numberOfProstrations += amount);
  }

  _startGong() {
    // _gongPlaying = true;
  }
}
