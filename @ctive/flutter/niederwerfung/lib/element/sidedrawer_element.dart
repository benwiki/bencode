import 'package:flutter/material.dart';
import 'package:prostrationcounter/core/color_extension.dart';
import 'package:prostrationcounter/core/context_extension.dart';
import 'package:prostrationcounter/core/language.dart';
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
            // const SizedBox(height: 20),
            ListTile(
              tileColor: context.appColors.blueStrong,
              title: Text(
                "🌐 Language",
                style: textStyle.copyWith(fontWeight: FontWeight.bold),
              ),
              subtitle: SizedBox(
                height: 72,
                child: Padding(
                  padding: EdgeInsets.only(left: textPadding, top: 8),
                  child: FutureBuilder(
                    future: SharedPreferences.getInstance(),
                    builder: (context, snapshot) {
                      if (snapshot.connectionState != ConnectionState.done) {
                        return const Center(child: CircularProgressIndicator());
                      }
                      final prefs = snapshot.data;
                      final lang = prefs?.getString('language') ?? 'en';
                      return DropdownButton<String>(
                        dropdownColor: context.appColors.blueDeep,
                        iconDisabledColor: context.appColors.whiteStrong,
                        iconEnabledColor: context.appColors.whiteStrong,
                        value: lang,
                        itemHeight: 60,
                        items: [
                          for (final lang in Language.values)
                            DropdownMenuItem(
                              value: lang.code,
                              child: Text(
                                lang.nameWithFlag,
                                style: textStyle,
                              ),
                            ),
                        ],
                        onChanged: (lang) async {
                          if (lang == null) return;
                          NwApp.of(context)?.setLocale(Locale(lang));
                          final prefs = await SharedPreferences.getInstance();
                          prefs.setString('language', lang);
                        },
                        underline: Container(),
                        isExpanded: true,
                      );
                    },
                  ),
                ),
              ),
            ),
            Container(height: 3, color: context.appColors.blueLight),
            // const SizedBox(height: 3),
            _specialThanksTile(context),
            Container(height: 3, color: context.appColors.blueLight),
            // const SizedBox(height: 3),
            _supportTile(context),
          ],
        ),
      ),
    );
  }

  Widget _specialThanksTile(BuildContext context) {
    return GestureDetector(
      onTap: () => showSpecialThanksDialog(context),
      child: ListTile(
        // special thanks
        tileColor: context.appColors.blueDeep.darken(0.3),
        title: Text(
          "🙏 ${context.text.specialThanks}",
          style: textStyle.copyWith(fontWeight: FontWeight.bold),
        ),
      ),
    );
  }

  void showSpecialThanksDialog(BuildContext context) {
    final textStyle = TextStyle(color: context.appColors.blackStrong);
    showDialog(
      context: context,
      builder: (context) => _dialog(context, [
        Text(context.text.specialThanksText,
            textAlign: TextAlign.center,
            style:
                textStyle.copyWith(fontSize: 20, fontWeight: FontWeight.bold)),
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
      ]),
    );
  }

  Widget _dialog(BuildContext context, List<Widget> children) {
    return Padding(
      padding: EdgeInsets.symmetric(
        horizontal: context.width(land: 0.1, port: 0.1),
        vertical: context.height(land: 0.1, port: 0.1),
      ),
      child: Stack(
        children: [
          Container(
            decoration: BoxDecoration(
              color: context.appColors.yellowLight,
              borderRadius: BorderRadius.circular(20),
            ),
            child: SingleChildScrollView(
              child: Padding(
                padding: const EdgeInsets.all(20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: children,
                ),
              ),
            ),
          ),
          Positioned(
            top: 0,
            right: 0,
            child: GestureDetector(
              onTap: () => Navigator.pop(context),
              child: Container( 
                width: 40,
                height: 40,
                decoration: BoxDecoration(
                  color: context.appColors.whiteStrong.withAlpha(130),
                  borderRadius: const BorderRadius.only(
                    topRight: Radius.circular(20),
                    bottomLeft: Radius.circular(20),
                  ),
                ),
                child: const Center(
                  child: Icon(Icons.close, size: 24),
                ),
              ),
            ),
          ),
        ],
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
      builder: (context) => _dialog(context, [
        Text(
          context.text.supportTitle,
          style: textStyle.copyWith(
            fontWeight: FontWeight.bold,
            fontSize: 22,
          ),
        ),
        const SizedBox(height: 20),
        context.text.supportText.link(
          textStyle: textStyle.copyWith(fontSize: 18),
        ),
      ]),
    );

    // AlertDialog(
    //   // surfaceTintColor: context.appColors.blackStrong,
    //   backgroundColor: context.appColors.yellowLight,
    //   title: Text(
    //     context.text.supportTitle,
    //     style: textStyle.copyWith(
    //       fontWeight: FontWeight.bold,
    //       fontSize: 22,
    //     ),
    //   ),
    //   content:

    //   //Text(context.text.supportText, style: textStyle),
    //   actions: [
    //     TextButton(
    //       onPressed: () => Navigator.pop(context),
    //       child: Text(context.text.back, style: textStyle),
    //     ),
    //     // TextButton(
    //     //   onPressed: () async =>
    //     //       await launchUrlString("mailto:govindapp@proton.me"),
    //     //   child: Text("Email", style: textStyle),
    //     // ),
    //     // TextButton(
    //     //   onPressed: () async =>
    //     //       await launchUrlString("https://paypal.me/benkex"),
    //     //   child: Text("PayPal", style: textStyle),
    //     // ),
    //   ],
    // ),
  }
}
