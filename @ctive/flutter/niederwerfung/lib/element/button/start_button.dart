import 'dart:async';

import 'package:flutter/material.dart';
import 'package:prostrationcounter/core/context_extension.dart';
import 'package:prostrationcounter/gong_player.dart';
import 'package:prostrationcounter/model/chant_model.dart';
import 'package:prostrationcounter/model/gong_interval_model.dart';
import 'package:prostrationcounter/model/prostrations_model.dart';
import 'package:provider/provider.dart';

class StartButton extends StatefulWidget {
  const StartButton({super.key});

  @override
  StartButtonState createState() => StartButtonState();
}

class StartButtonState extends State<StartButton> {
  bool _gongPlaying = false;
  final gongPlayer = GongPlayer();
  Timer? _countdownTimer;
  Timer? _playTimer;
  int _remainingSeconds = 0;
  int _postCount = 0;

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
      child: GestureDetector(
        onTap: _gongPlaying ? _stopGong : _startGong,
        // style: ElevatedButton.styleFrom(
        //     backgroundColor: Colors.red[900],
        //     foregroundColor: Colors.white,
        //     side: const BorderSide(width: 3, color: Colors.white),
        //     shape: RoundedRectangleBorder(
        //         borderRadius: BorderRadius.circular(10))),
        child: Container(
          decoration: BoxDecoration(
            color: _gongPlaying ? Colors.red[900] : Colors.green[700],
            borderRadius: BorderRadius.circular(10),
            border: Border.all(
                width: 4, color: Colors.white),
          ),
          child: Center(
            child: Text(
              _gongPlaying
                  ? (_remainingSeconds > 0
                      ? _remainingSeconds.toString()
                      : context.text.stop)
                  : context.text.start,
              style: const TextStyle(
                  fontSize: 25,
                  color: Colors.white,
                  fontWeight: FontWeight.bold),
            ),
          ),
        ),
      ),
    );
  }

  // helper to play one gong (initial or subsequent)
  Future<void> _playCycle() async {
    if (!_gongPlaying) return;
    if (prostrationsModel.numberOfProstrations > 0) {
      await gongPlayer.play(withMantra: chantModel.chantIsOn);
      prostrationsModel.subtractOne();
      // schedule next at user interval
      _playTimer?.cancel();
      _playTimer = Timer(Duration(seconds: gongIntervalModel.gongInterval.toInt()), _playCycle);
    } else if (_postCount < 3) {
      await gongPlayer.play(withMantra: false);
      _postCount++;
      // schedule next at 1.7 seconds for last three
      _playTimer?.cancel();
      _playTimer = Timer(const Duration(milliseconds: 1700), _playCycle);
    } else {
      await _stopGong();
    }
  }

  void _startGong() {
    setState(() {
      _gongPlaying = true;
      _remainingSeconds = gongIntervalModel.gongInterval.toInt();
    });
    _countdownTimer?.cancel();
    _countdownTimer = Timer.periodic(
      const Duration(seconds: 1),
      (t) {
        if (_remainingSeconds > 1) {
          setState(() => _remainingSeconds--);
        } else {
          t.cancel();
          setState(() => _remainingSeconds = 0);
        }
      },
    );
    _postCount = 0;
    _playCycle(); // initial play, subsequent plays scheduled within
  }

  Future<void> _stopGong() async {
    _playTimer?.cancel();
    _countdownTimer?.cancel();
    gongPlayer.stop();
    setState(() {
      _gongPlaying = false;
      _remainingSeconds = 0;
    });
  }
}
