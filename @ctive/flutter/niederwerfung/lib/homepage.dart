/*
Rules:
- if the gong interval is less than 8 seconds, and mantra is turned on, the app should display a warning message
  about the pace for the mantra being too fast.
*/

import 'dart:async';

import 'package:flutter/material.dart';
import 'package:niederwerfung/gong_interval_changer.dart';
import 'package:niederwerfung/chant_controller.dart';
import 'package:niederwerfung/context_extensions.dart';
import 'package:niederwerfung/gong_player.dart';
import 'package:niederwerfung/main.dart';
import 'package:niederwerfung/number_of_prostrations_changer.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  double _gongInterval = 10;
  double _numberOfProstrations = 108;
  double _fixedNumberOfProstrations = 0;

  Locale _locale = const Locale("en");

  bool _gongPlaying = false;
  bool _mantraOn = false;

  GongPlayer gongPlayer = GongPlayer();

  final double textPadding = 20;
  final TextStyle textStyle =
      const TextStyle(fontSize: 20, color: Colors.white);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: context.appColors.blueDeep,
      drawerScrimColor: const Color(0xAA000000),
      appBar: _buildAppBar(context),
      body: _buildBody(context),
      floatingActionButton: _buildFAB(),
      endDrawer: _buildLanguageChangeButton(),
    );
  }

  @override
  void dispose() {
    gongPlayer.dispose();
    super.dispose();
  }

  AppBar _buildAppBar(BuildContext context) {
    final titleStyle =
        TextStyle(fontSize: 30, color: context.appColors.whiteStrong);
    return AppBar(
      backgroundColor: context.appColors.blueStrong,
      foregroundColor: context.appColors.whiteStrong,
      shadowColor: context.appColors.blackStrong,
      // surfaceTintColor: context.appColors.whiteStrong,
      title: Text(context.text.homeScreenName, style: titleStyle),
      centerTitle: true,
    );
  }

  Widget _buildBody(BuildContext context) {
    print("locale: $_locale, text: ${context.text.gongInterval}");
    return ListView(
      children: [
        const SizedBox(height: 20),
        //
        GongIntervalChanger(onChanged: (value) {
          print("value: $value, mantraOn: $_mantraOn");
          if (value < 8 && _mantraOn) {
            print("...... ON");
            ScaffoldMessenger.of(context).showSnackBar(SnackBar(
              content: Text(context.text.mantraPaceWarning),
              duration: const Duration(seconds: 3),
            ));
            _mantraOn = false;
          }
          _gongInterval = value;
          setState(() {});
        }),
        //
        const SizedBox(height: 35),
        //
        NumberOfProstrationsChanger(onChanged: (value) {
          _numberOfProstrations = value;
          setState(() {});
        }),
        //
        const SizedBox(height: 35),
        //
        ChantController(onSwitch: (isMantraOn) {
          if (_gongInterval < 8 && isMantraOn) {
            ScaffoldMessenger.of(context).showSnackBar(SnackBar(
              content: Text(context.text.mantraPaceWarning),
              duration: const Duration(seconds: 3),
            ));
            _mantraOn = false;
          } else {
            _mantraOn = isMantraOn;
          }
          setState(() {});
        }),
        //
        const SizedBox(height: 80),
      ],
    );
  }

  Widget _buildFAB() {
    return SizedBox(
      width: 120,
      height: 50,
      child: ElevatedButton(
        onPressed: _gongPlaying ? _stopGong : _startGong,
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

  Widget _buildLanguageChangeButton() {
    return SafeArea(
        child: Drawer(
      backgroundColor: context.appColors.blueStrong,
      child: ListView(
        children: [
          const SizedBox(height: 10),
          ListTile(
            title: Text(
              "Language",
              style: textStyle.copyWith(fontWeight: FontWeight.bold),
            ),
          ),
          _languageTile("en", "English"),
          ListTile(
            title: Padding(
                padding: EdgeInsets.only(left: textPadding),
                child: Text("Deutsch", style: textStyle)),
            onTap: () => setState(() {
              _locale = const Locale("de");
              Navigator.pop(context);
            }),
          ),
        ],
      ),
    ));
  }

  Widget _languageTile(String iso, String language) {
    return ListTile(
      title: Padding(
          padding: EdgeInsets.only(left: textPadding),
          child: Text(language, style: textStyle)),
      onTap: () => setState(() {
        _locale = Locale(iso);
        NwApp.of(context)?.setLocale(_locale);
        Navigator.pop(context);
      }),
    );
  }

  _startGong() async {
    setState(() {
      _gongPlaying = true;
    });
    _fixedNumberOfProstrations = _numberOfProstrations;

    for (var i = 0; i < _fixedNumberOfProstrations; i++) {
      if (_gongPlaying) {
        await gongPlayer.play(withMantra: _mantraOn);
        setState(() {
          _numberOfProstrations--;
        });
        await Future.delayed(
          Duration(milliseconds: (_gongInterval * 1000).toInt()),
          () {},
        );
      }
    }
  }

  Future<void> _stopGong() async {
    gongPlayer.stop();
    setState(() {
      _gongPlaying = false;
    });
  }
}
