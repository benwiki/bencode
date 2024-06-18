import 'dart:async';

import 'package:audioplayers/audioplayers.dart';

class GongPlayer {
  GongPlayer() {
    for (int i = 0; i < numberOfPlayers; i++) {
      final player = AudioPlayer();
      player.setReleaseMode(ReleaseMode.stop);
      player.setSource(AssetSource('gong_shorter.wav'));
      players.add(player);
    }
    mantraPlayer.setReleaseMode(ReleaseMode.stop);
    mantraPlayer.setSource(AssetSource('mantra.wav'));
  }

  int numberOfPlayers = 10;
  int currentPlayer = 0;
  List<AudioPlayer> players = [];
  List<Timer> timers = [];
  AudioPlayer mantraPlayer = AudioPlayer();

  Future<void> play({bool withMantra = false}) async {
    await players[currentPlayer].stop();
    await players[currentPlayer].resume();
    currentPlayer = (currentPlayer + 1) % numberOfPlayers;
    if (withMantra) {
      await mantraPlayer.stop();
      await mantraPlayer.resume();
    }
  }

  void stop() {
    for (final player in players) {
      player.stop();
    }
    for (final timer in timers) {
      timer.cancel();
    }
  }

  void dispose() {
    for (final player in players) {
      player.dispose();
    }
  }
}
