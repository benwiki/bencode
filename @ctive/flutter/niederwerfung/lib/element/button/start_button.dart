import 'package:flutter/material.dart';
import 'package:niederwerfung/core/context_extension.dart';
import 'package:niederwerfung/core/utility.dart';
import 'package:niederwerfung/gong_player.dart';
import 'package:niederwerfung/model/chant_model.dart';
import 'package:niederwerfung/model/gong_interval_model.dart';
import 'package:niederwerfung/model/prostrations_model.dart';
import 'package:provider/provider.dart';

class StartButton extends StatefulWidget {
  const StartButton({super.key});

  @override
  StartButtonState createState() => StartButtonState();
}

class StartButtonState extends State<StartButton> {
  bool _gongPlaying = false;
  final gongPlayer = GongPlayer();

  late ProstrationsModel prostrationsModel;
  late ChantModel chantModel;
  late GongIntervalModel gongIntervalModel;

  @override
  Widget build(BuildContext context) {
    prostrationsModel = Provider.of<ProstrationsModel>(context, listen: false);
    chantModel = Provider.of<ChantModel>(context, listen: false);
    gongIntervalModel = Provider.of<GongIntervalModel>(context, listen: false);

    return SizedBox(
      width: 120,
      height: 50,
      child: ElevatedButton(
        onPressed: _gongPlaying ? _stopGong : () => _startGong(context),
        style: ElevatedButton.styleFrom(
            backgroundColor: Colors.red[900],
            foregroundColor: Colors.white,
            side: const BorderSide(width: 3, color: Colors.white),
            shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(10))),
        child: Text(
          _gongPlaying ? context.text.stop : context.text.start,
          style: const TextStyle(fontSize: 25),
        ),
      ),
    );
  }

  _startGong(BuildContext context) async {
    setState(() {
      _gongPlaying = true;
    });
    final fixedNumberOfProstrations = prostrationsModel.numberOfProstrations;
    for (var i = 0; i < fixedNumberOfProstrations; i++) {
      if (_gongPlaying) {
        await gongPlayer.play(withMantra: chantModel.chantIsOn);
        prostrationsModel.subtractOne();
        await waitForSeconds(gongIntervalModel.gongInterval);
      }
    }
    // another 3 times at the end
    for (var i = 0; i < 3; i++) {
      if (_gongPlaying) {
        await gongPlayer.play(withMantra: false);
        await waitForSeconds(1.7);
      }
    }
    setState(() {
      _gongPlaying = false;
    });
  }

  Future<void> _stopGong() async {
    gongPlayer.stop();
    setState(() {
      _gongPlaying = false;
    });
  }
}
