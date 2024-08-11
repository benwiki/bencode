import 'package:flutter/material.dart';
import 'package:niederwerfung/core/color_extension.dart';
import 'package:niederwerfung/core/context_extension.dart';
import 'package:niederwerfung/main.dart';

class SideDrawerElement extends StatelessWidget {
  const SideDrawerElement({super.key});

  final TextStyle textStyle =
      const TextStyle(fontSize: 20, color: Colors.white);
  final double textPadding = 20;

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Drawer(
        backgroundColor: context.appColors.blueStrong,
        child: ListView(
          children: [
            const SizedBox(height: 10),
            ListTile(
              tileColor: context.appColors.blueDeep.darken(0.3),
              title: Text(
                "🌐 Language",
                style: textStyle.copyWith(fontWeight: FontWeight.bold),
              ),
            ),
            _languageTile("en", "English", context),
            _languageTile("de", "Deutsch", context),
          ],
        ),
      ),
    );
  }

  Widget _languageTile(String iso, String language, BuildContext context) {
    return ListTile(
      title: Padding(
          padding: EdgeInsets.only(left: textPadding),
          child: Text(language, style: textStyle)),
      onTap: () {
        NwApp.of(context)?.setLocale(Locale(iso));
        Navigator.pop(context);
      },
    );
  }
}
