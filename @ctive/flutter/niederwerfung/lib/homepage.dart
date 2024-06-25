/*
Rules:
- if the gong interval is less than 8 seconds, and mantra is turned on, the app should display a warning message
  about the pace for the mantra being too fast.
*/

import 'dart:async';

import 'package:flutter/material.dart';
import 'package:niederwerfung/chant_model.dart';
import 'package:niederwerfung/gong_interval_changer.dart';
import 'package:niederwerfung/chant_controller.dart';
import 'package:niederwerfung/context_extensions.dart';
import 'package:niederwerfung/gong_player.dart';
import 'package:niederwerfung/main.dart';
import 'package:niederwerfung/number_of_prostrations_changer.dart';
import 'package:niederwerfung/prostrations_model.dart';
import 'package:niederwerfung/utility.dart';
import 'package:provider/provider.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  double _gongInterval = 10;
  bool _gongPlaying = false;

  Locale _locale = const Locale("en");

  final double textPadding = 20;
  final TextStyle textStyle =
      const TextStyle(fontSize: 20, color: Colors.white);

  NumberOfProstrationsChanger? prostrationsChanger;
  ChantController? chantController;
  GongPlayer gongPlayer = GongPlayer();

  @override
  void dispose() {
    gongPlayer.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: context.appColors.blueDeep,
      drawerScrimColor: Colors.black.withOpacity(0.8),
      appBar: _buildAppBar(context),
      body: _buildBody(context),
      floatingActionButton: _buildFAB(context),
      endDrawer: _buildDrawer(),
    );
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
    final chantModel = Provider.of<ChantModel>(context, listen: false);
    prostrationsChanger = const NumberOfProstrationsChanger();
    chantController = ChantController(onSwitch: (isMantraOn) {
      if (_gongInterval < 8 && isMantraOn) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
          backgroundColor: context.appColors.blueDeep,
          content: Text(context.text.mantraPaceWarning),
          duration: const Duration(seconds: 3),
        ));
        chantModel.setChantState(false);
      }
    });

    return ListView(
      children: [
        const SizedBox(height: 20),
        //
        GongIntervalChanger(onChanged: (value) {
          if (value < 8 && chantModel.chantIsOn) {
            ScaffoldMessenger.of(context).showSnackBar(SnackBar(
              backgroundColor: context.appColors.blueDeep,
              content: Text(context.text.mantraPaceWarning),
              duration: const Duration(seconds: 3),
            ));
            chantModel.setChantState(false);
          }
          _gongInterval = value;
          setState(() {});
        }),
        //
        const SizedBox(height: 35),
        //
        prostrationsChanger!,
        //
        const SizedBox(height: 35),
        //
        chantController!,
        //
        const SizedBox(height: 80),
      ],
    );
  }

  Widget _buildFAB(BuildContext context) {
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

  Widget _buildDrawer() {
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
            _languageTile("de", "Deutsch"),
          ],
        ),
      ),
    );
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

  _startGong(BuildContext context) async {
    final prostrationsModel =
        Provider.of<ProstrationsModel>(context, listen: false);
    final chantModel = Provider.of<ChantModel>(context, listen: false);

    setState(() {
      _gongPlaying = true;
    });
    for (var i = 0; i < prostrationsModel.numberOfProstrations; i++) {
      if (_gongPlaying) {
        await gongPlayer.play(withMantra: chantModel.chantIsOn);
        prostrationsModel.subtractOne();
        await waitForSeconds(_gongInterval);
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
