import 'package:flutter/material.dart';

class ChantController extends StatefulWidget {
  const ChantController({super.key});

  @override
  State<ChantController> createState() => _ChantControllerState();
}

class _ChantControllerState extends State<ChantController> {
  SoundFile? chantFile;
  bool _mantraOn = false;

  @override
  Widget build(BuildContext context) {
    final textStyle =
        TextStyle(color: Theme.of(context).colorScheme.surface, fontSize: 20);
    const Color backgroundColor = Color.fromARGB(255, 30, 43, 94);

    return Container(
        margin: const EdgeInsets.all(10),
        decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(10), color: backgroundColor),
        child: Column(children: [
          const SizedBox(height: 15),
          Row(mainAxisAlignment: MainAxisAlignment.center, children: [
            Text("Mantra:", style: textStyle),
            const SizedBox(width: 15),
            _buildMantraSwitch(context)
          ]),
          const SizedBox(height: 15),
          Row(mainAxisAlignment: MainAxisAlignment.center, children: [
            Text("Name:", style: textStyle),
          ]),
          const SizedBox(height: 20),
        ]));
  }

  Widget _buildMantraSwitch(BuildContext context) {
    return ElevatedButton(
        onPressed: () => setState(() => _mantraOn = !_mantraOn),
        style: ElevatedButton.styleFrom(
            backgroundColor: _mantraOn
                ? Colors.green
                : const Color.fromARGB(255, 244, 120, 111),
            foregroundColor:
                // _mantraOn
                Theme.of(context).colorScheme.primary
            // : Colors.white
            ),
        child: Text(
          _mantraOn ? "anschalten" : "ausschalten",
          style: const TextStyle(fontSize: 20),
        ));
  }
}

class SoundFile {
  SoundFile();
  String name = "";
}

class SoundFileManager {
  List<SoundFile>? soundFiles;

  void load() {}
}
