import 'app_localizations.dart';

// ignore_for_file: type=lint

/// The translations for Hungarian (`hu`).
class AppLocalizationsHu extends AppLocalizations {
  AppLocalizationsHu([String locale = 'hu']) : super(locale);

  @override
  String get appName => 'Leborulások';

  @override
  String get homeScreenName => 'Leborulások';

  @override
  String get gongInterval => 'Gong intervallum';

  @override
  String get sec => 's';

  @override
  String get numberOfProstrations => 'Leborulások száma';

  @override
  String get mantraIsOn => 'Mantra bekapcsolva';

  @override
  String get mantraIsOff => 'Mantra kikapcsolva';

  @override
  String get title => 'Cím';

  @override
  String get start => 'START';

  @override
  String get stop => 'STOP';

  @override
  String get mantraPaceWarning => 'A gong intervalluma túl rövid a mantrához. Legalább 8 másodperc szükséges.';

  @override
  String get gongIntervalWarning => 'A gong intervalluma túl rövid a mantrához. Legalább 8 másodperc szükséges. A mantra kikapcsolva.';

  @override
  String get support => 'Szeretném támogatni a fejlesztést';

  @override
  String get supportTitle => 'Támogatás';

  @override
  String get supportText => 'Ha visszajelzést szeretnél adni az alkalmazásról, vagy ötleteid lennének, kérlek írd meg őket erre az e-mail címre:\n[govindapp@proton.me;mailto:govindapp@proton.me]\n\nHa tetszik az alkalmazás, és szeretnéd támogatni a fejlesztését, küldhetsz adományt PayPal-on keresztül:\n[paypal.me/benkex;https://paypal.me/benkex]\nKöszönöm!\n\nAzzal is sokat segítesz, ha továbbajánlod az alkalmazást! :)';

  @override
  String get back => 'Vissza';

  @override
  String get specialThanks => 'Külön köszönet';

  @override
  String get specialThanksText => 'Külön köszönet mindenkinek, akik itt szerepelnek!';

  @override
  String get singingBowl_1 => 'A hang a [SoundEffectStudio;https://www.youtube.com/@SoundEffectStudioNo.1] csatornától származik, a videó linkje: [Singing Bowl (Deep Sound) - Sound Effect;https://youtu.be/y96ARieC9HY].';
}
