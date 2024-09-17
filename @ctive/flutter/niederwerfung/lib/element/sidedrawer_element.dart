import 'package:flutter/material.dart';
import 'package:prostrationcounter/core/color_extension.dart';
import 'package:prostrationcounter/core/context_extension.dart';
import 'package:prostrationcounter/core/string_extension.dart';
import 'package:prostrationcounter/main.dart';
import 'package:shared_preferences/shared_preferences.dart';

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
            Container(height: 2, color: context.appColors.blueDeep),
            _languageTile("de", "Deutsch", context),
            Container(height: 2, color: context.appColors.blueDeep),
            // Container(height: 3, color: context.appColors.whiteStrong),
            // const SizedBox(height: 20),
            _specialThanksTile(context),
            // Container(height: 3, color: context.appColors.whiteStrong),
            const SizedBox(height: 20),
            _supportTile(context),
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
      onTap: () async {
        if (!context.mounted) return;
        NwApp.of(context)?.setLocale(Locale(iso));
        final prefs = await SharedPreferences.getInstance();
        prefs.setString("language", iso);
        if (!context.mounted) return;
        // Navigator.pop(context);
      },
    );
  }

  Widget _specialThanksTile(BuildContext context) {
    return ListTile(
      // special thanks
      tileColor: context.appColors.blueDeep.darken(0.3),
      title: GestureDetector(
          onTap: () => showSpecialThanksDialog(context),
          child: Text(
            "🙏 ${context.text.specialThanks}",
            style: textStyle.copyWith(fontWeight: FontWeight.bold),
          )),
    );
  }

  void showSpecialThanksDialog(BuildContext context) {
    final textStyle = TextStyle(color: context.appColors.blackStrong);
    showDialog(
      context: context,
      builder: (context) => Padding(
        padding: EdgeInsets.symmetric(
          horizontal: context.sizeConstant / 12,
          vertical: context.sizeConstant / 5,
        ),
        child: Container(
          decoration: BoxDecoration(
            color: context.appColors.yellowLight,
            borderRadius: BorderRadius.circular(20),
          ),
          child: Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(context.text.specialThanksText,
                      textAlign: TextAlign.center,
                      style: textStyle.copyWith(
                          fontSize: 20, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 20),
                  Text(
                    "Vajramala, Amoghavajra",
                    style: textStyle.copyWith(
                      fontSize: 18,
                      fontWeight: FontWeight.w700,
                      color: Colors.red.darken(0.3),
                    ),
                  ),
                  const SizedBox(height: 20),
                  context.text.singingBowl_1.link(
                      textStyle: TextStyle(
                    color: context.appColors.blackStrong,
                    fontSize: 18,
                  )),
                  const Spacer(),
                  Align(
                    alignment: Alignment.bottomRight,
                    child: TextButton(
                      onPressed: () => Navigator.pop(context),
                      child: Text(context.text.back,
                          style: textStyle.copyWith(
                            fontSize: 18,
                          )),
                    )
                  ),
                ],
              )),
        ),
      ),
    );
  }

  Widget _supportTile(BuildContext context) {
    return ListTile(
      tileColor: context.appColors.blueDeep.darken(0.3),
      title: GestureDetector(
        onTap: () => showSupportDialog(context),
        child: Text(
          "🖐️ ${context.text.support}",
          style: textStyle.copyWith(fontWeight: FontWeight.bold),
        ),
      ),
    );
  }

  void showSupportDialog(BuildContext context) {
    final textStyle =
        TextStyle(color: context.appColors.blackStrong, fontSize: 18);
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        // surfaceTintColor: context.appColors.blackStrong,
        backgroundColor: context.appColors.yellowLight,
        title: Text(
          context.text.supportTitle,
          style: textStyle.copyWith(
            fontWeight: FontWeight.bold,
            fontSize: 22,
          ),
        ),
        content: context.text.supportText.link(
          textStyle: textStyle.copyWith(fontSize: 18),
        ),

        //Text(context.text.supportText, style: textStyle),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text(context.text.back, style: textStyle),
          ),
          // TextButton(
          //   onPressed: () async =>
          //       await launchUrlString("mailto:govindapp@proton.me"),
          //   child: Text("Email", style: textStyle),
          // ),
          // TextButton(
          //   onPressed: () async =>
          //       await launchUrlString("https://paypal.me/benkex"),
          //   child: Text("PayPal", style: textStyle),
          // ),
        ],
      ),
    );
  }
}
