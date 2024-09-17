/*
Rules:
- if the gong interval is less than 8 seconds, and mantra is turned on, the app should display a warning message
  about the pace for the mantra being too fast.
*/


import 'package:flutter/material.dart';
import 'package:prostrationcounter/element/button/start_button.dart';
import 'package:prostrationcounter/element/sidedrawer_element.dart';
import 'package:prostrationcounter/changer/gong_interval_changer.dart';
import 'package:prostrationcounter/chant_controller.dart';
import 'package:prostrationcounter/core/context_extension.dart';
import 'package:prostrationcounter/changer/number_of_prostrations_changer.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: context.appColors.blueStrong,
      drawerScrimColor: Colors.black.withOpacity(0.8),
      appBar: _buildAppBar(context),
      body: _buildBody(context),
      floatingActionButton: const StartButton(),
      endDrawer: const SideDrawerElement(),
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
    return ListView(
      children: const [
        SizedBox(height: 20),
        //
        GongIntervalChanger(),
        //
        SizedBox(height: 35),
        //
        NumberOfProstrationsChanger(),
        //
        SizedBox(height: 35),
        //
        ChantController(),
        //
        SizedBox(height: 80),
      ],
    );
  }
}
