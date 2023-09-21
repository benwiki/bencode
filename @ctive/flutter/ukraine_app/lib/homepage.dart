import 'package:flutter/material.dart';

import 'package:ukraine_app/data.dart';
import 'package:ukraine_app/main.dart';
import 'package:ukraine_app/settings.dart';
import 'package:ukraine_app/webpage.dart';

enum OptionType { lang, country, objective }

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> with Settings {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: const Text("Home"),
        ),
        body: Center(
            child: Column(
          children: <Widget>[
            buildSettingButtons(context),
            // buildCategoryGrid(context), // on-coming
            // Text(lang + " ; " + country + " ; " + objective), // debug
            Expanded(child: SizedBox(child: WebPage()))
          ],
        )));
  }

  Widget buildSettingButtons(context) => GridView.count(
        crossAxisCount: 2,
        crossAxisSpacing: 1.0,
        mainAxisSpacing: 10.0,
        shrinkWrap: true,
        padding: const EdgeInsets.all(10.0),
        childAspectRatio: MediaQuery.of(context).size.height / 200,
        children: [
          ElevatedButton(
              style: ElevatedButton.styleFrom(backgroundColor: Colors.red[800]),
              onPressed: () => navigateToSetting(context, OptionType.lang),
              child: const Text("Мову/Language/Sprache/Nyelv",
                  textAlign: TextAlign.center)),
          Center(child: Text(showLang, textAlign: TextAlign.center)),
          //
          OutlinedButton(
              style: OutlinedButton.styleFrom(
                  side: const BorderSide(width: 3.0, color: Colors.blue)),
              onPressed: () => navigateToSetting(context, OptionType.country),
              child:
                  Text(titles["country"][lang], textAlign: TextAlign.center)),
          Center(child: Text(showCountry, textAlign: TextAlign.center)),
          //
          OutlinedButton(
              style: OutlinedButton.styleFrom(
                side: const BorderSide(width: 3.0, color: Colors.blue),
              ),
              onPressed: () => navigateToSetting(context, OptionType.objective),
              child:
                  Text(titles["objective"][lang], textAlign: TextAlign.center)),
          Center(child: Text(showObjective, textAlign: TextAlign.center)),
        ],
      );

  Widget buildCategoryGrid(context) => GridView.count(
      crossAxisCount: 3,
      crossAxisSpacing: 5.0,
      mainAxisSpacing: 5.0,
      shrinkWrap: true,
      childAspectRatio: MediaQuery.of(context).size.height / 500,
      children: categoryByLang[lang]!
          .entries
          .map((entry) => SizedBox(
              height: 30,
              child: OutlinedButton(
                onPressed: () {},
                child: Text(
                  entry.value,
                  textAlign: TextAlign.center,
                ),
                style: OutlinedButton.styleFrom(
                    padding: const EdgeInsets.all(0.5)),
              )))
          .toList());
}
