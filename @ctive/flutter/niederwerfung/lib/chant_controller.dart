import 'package:flutter/material.dart';
import 'package:niederwerfung/context_extensions.dart';

class ChantController extends StatefulWidget {
  const ChantController({
    required this.onSwitch,
    super.key,
  });

  final Function(bool) onSwitch;

  @override
  State<ChantController> createState() => _ChantControllerState();
}

class _ChantControllerState extends State<ChantController> {
  bool _mantraOn = false;

  @override
  Widget build(BuildContext context) {
    final textStyle =
        TextStyle(color: context.appColors.whiteStrong, fontSize: 20);

    return Container(
      margin: const EdgeInsets.all(10),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(10),
        color: context.appColors.blueStrong,
      ),
      child: Padding(
          padding: const EdgeInsets.only(left: 30),
          child: Column(
            children: [
              const SizedBox(height: 15),
              Row(
                children: [
                  _buildMantraSwitch(context),
                  const SizedBox(width: 15),
                  _buildMantraText(context),
                ],
              ),
              const SizedBox(height: 15),
              Row(
                children: [
                  Text("${context.text.title}:", style: textStyle),
                ],
              ),
              const SizedBox(height: 20),
            ],
          )),
    );
  }

  Widget _buildMantraText(BuildContext context) {
    final offColor = context.appColors.redVivid;
    final onColor = context.appColors.greenVivid;
    final mantraTextStyle = TextStyle(
      color: _mantraOn ? onColor : offColor,
      fontSize: 20,
      fontWeight: FontWeight.bold,
    );
    final mantraText =
        _mantraOn ? context.text.mantraIsOn : context.text.mantraIsOff;
    return Text(mantraText, style: mantraTextStyle);
  }

  Widget _buildMantraSwitch(BuildContext context) {
    return Switch(
      activeTrackColor: context.appColors.greenMedium,
      inactiveTrackColor: context.appColors.blueDeep,
      activeColor: context.appColors.whiteStrong,
      inactiveThumbColor: context.appColors.whiteStrong,
      value: _mantraOn,
      onChanged: (value) {
        setState(() {
          _mantraOn = value;
          widget.onSwitch(value);
        });
      },
    );
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
