import 'dart:async';

import 'package:audioplayers/audioplayers.dart';
import 'package:flutter/material.dart';

class GongPlayer {
  GongPlayer() {
    // Configure audio context to avoid focus stealing
    final audioContext = AudioContext(
      android: const AudioContextAndroid(
        audioMode: AndroidAudioMode.normal,
        contentType: AndroidContentType.music,
        usageType: AndroidUsageType.media,
        audioFocus: AndroidAudioFocus.none,
      ),
      iOS: AudioContextIOS(
        category: AVAudioSessionCategory.playback,
        options: const {AVAudioSessionOptions.mixWithOthers},
      ),
    );
    for (int i = 0; i < numberOfPlayers; i++) {
      final player = AudioPlayer();
      player.setAudioContext(audioContext);
      player.setReleaseMode(ReleaseMode.stop);
      player.setSource(AssetSource('gong_shorter.wav'));
      players.add(player);
    }
    mantraPlayer.setAudioContext(audioContext);
    mantraPlayer.setReleaseMode(ReleaseMode.stop);
    mantraPlayer.setSource(AssetSource('mantra.wav'));
  }

  int numberOfPlayers = 10;
  int currentPlayer = 0;
  List<AudioPlayer> players = [];
  List<Timer> timers = [];
  AudioPlayer mantraPlayer = AudioPlayer();

  Future<void> play({bool withMantra = false}) async {
    debugPrint('Playing gong sound, current player: $currentPlayer');
    await players[currentPlayer].stop();
    await players[currentPlayer].play(
      AssetSource('gong_shorter.wav'),
      mode: PlayerMode.lowLatency,
    );
    currentPlayer = (currentPlayer + 1) % numberOfPlayers;
    if (withMantra) {
      await mantraPlayer.stop();
      await mantraPlayer.play(
        AssetSource('mantra.wav'),
        mode: PlayerMode.lowLatency,
      );
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
