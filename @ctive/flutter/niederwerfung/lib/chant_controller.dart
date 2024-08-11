import 'package:flutter/material.dart';
import 'package:niederwerfung/model/chant_model.dart';
import 'package:niederwerfung/core/context_extension.dart';
import 'package:niederwerfung/model/gong_interval_model.dart';
import 'package:provider/provider.dart';

class ChantController extends StatefulWidget {
  const ChantController({super.key});

  @override
  State<ChantController> createState() => _ChantControllerState();
}

class _ChantControllerState extends State<ChantController> {
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
    final chantModel = Provider.of<ChantModel>(context);

    final offColor = context.appColors.redVivid;
    final onColor = context.appColors.greenVivid;
    final mantraTextStyle = TextStyle(
      color: chantModel.chantIsOn ? onColor : offColor,
      fontSize: 20,
      fontWeight: FontWeight.bold,
    );
    final mantraText = chantModel.chantIsOn
        ? context.text.mantraIsOn
        : context.text.mantraIsOff;
    return Text(mantraText, style: mantraTextStyle);
  }

  Widget _buildMantraSwitch(BuildContext context) {
    final chantModel = Provider.of<ChantModel>(context);
    final gongIntervalModel = Provider.of<GongIntervalModel>(context);

    return Switch(
      activeTrackColor: context.appColors.greenMedium,
      inactiveTrackColor: context.appColors.blueDeep,
      activeColor: context.appColors.whiteStrong,
      inactiveThumbColor: context.appColors.whiteStrong,
      value: chantModel.chantIsOn,
      onChanged: (chantShouldBeOn) {
        if (gongIntervalModel.gongInterval < 8 && chantShouldBeOn) {
          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
            backgroundColor: context.appColors.blueDeep,
            content: Text(context.text.mantraPaceWarning),
            duration: const Duration(seconds: 3),
          ));
          chantModel.setChantState(false);
        } else {
          chantModel.setChantState(chantShouldBeOn);
        }
        setState(() {});
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
