import 'package:flutter/material.dart';

import 'package:ukraine_app/data.dart';
import 'package:ukraine_app/homepage.dart';
import 'package:ukraine_app/main.dart';
import 'package:ukraine_app/selectpage.dart';

mixin Settings {
  void navigateToSetting(BuildContext context, OptionType optionType) {
    Navigator.push(context, MaterialPageRoute(builder: (context) {
      String title;
      Map options;
      switch (optionType) {
        case OptionType.lang:
          title = 'Мову/Language/Sprache/Nyelv';
          options = langByLang;
          break;
        case OptionType.country:
          title = titles["country"][lang];
          options = countryByLang[lang];
          break;
        case OptionType.objective:
          title = titles["objective"][lang];
          options = objectiveByLang[lang];
          break;
        default:
          throw Exception("Wrong OptionType given to 'navigateToSettings'!");
      }
      List opKeys = options.keys.toList();
      return SelectPage(
          title: title,
          buttons: ListView.builder(
              itemCount: options.length,
              itemBuilder: (context, i) => OutlinedButton(
                  onPressed: () => setOptionAndBuildNewHomePage(
                      context, optionType, opKeys[i]),
                  child: Text(options[opKeys[i]]))));
    }));
  }

  void setOptionAndBuildNewHomePage(
      BuildContext context, OptionType optionType, String toSet) {
    switch (optionType) {
      case OptionType.lang:
        lang = toSet;
        break;
      case OptionType.country:
        country = toSet;
        break;
      case OptionType.objective:
        objective = toSet;
        break;
    }
    webpageURL = (webpageByCountryAndPurpose[country][objective][lang] ??
        (webpageByCountryAndPurpose[country][objective]["default"] ??
            defaultURL));
    showLang = langByLang[lang];
    showCountry = countryByLang[lang][country];
    showObjective = objectiveByLang[lang][objective];
    Navigator.pushAndRemoveUntil(
        context,
        MaterialPageRoute(builder: (context) => const HomePage()),
        (Route<dynamic> route) => false);
  }
}
