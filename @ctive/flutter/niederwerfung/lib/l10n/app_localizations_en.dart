import 'app_localizations.dart';

// ignore_for_file: type=lint

/// The translations for English (`en`).
class AppLocalizationsEn extends AppLocalizations {
  AppLocalizationsEn([String locale = 'en']) : super(locale);

  @override
  String get appName => 'Prostrations';

  @override
  String get homeScreenName => 'Prostrations';

  @override
  String get gongInterval => 'Gong interval';

  @override
  String get sec => 'sec.';

  @override
  String get numberOfProstrations => 'Number of prostrations';

  @override
  String get mantraIsOn => 'Mantra is on';

  @override
  String get mantraIsOff => 'Mantra is off';

  @override
  String get title => 'Title';

  @override
  String get start => 'START';

  @override
  String get stop => 'STOP';

  @override
  String get mantraPaceWarning => 'Gong interval is too short for mantra. At least 8 seconds are required.';

  @override
  String get gongIntervalWarning => 'Gong interval is too short for mantra. At least 8 seconds are required. Mantra turned off.';

  @override
  String get support => 'I want to support the development';

  @override
  String get supportTitle => 'Support';

  @override
  String get supportText => 'If you want to give feedback about the app, or you have ideas, please contact me on this email address:\n[govindapp@proton.me;mailto:govindapp@proton.me]\n\nIf you enjoy using the app and would like to support its ongoing development, please consider making a donation via PayPal:\n[paypal.me/benkex;https://paypal.me/benkex]\n\nFeel free to recommend the app to others! :)';

  @override
  String get back => 'Back';

  @override
  String get specialThanks => 'Special thanks';

  @override
  String get specialThanksText => 'Special thanks to all the people and organizations listed here!';

  @override
  String get singingBowl_1 => 'The sound comes from [SoundEffectStudio;https://www.youtube.com/@SoundEffectStudioNo.1], the link to the video: [Singing Bowl (Deep Sound) - Sound Effect;https://youtu.be/y96ARieC9HY].';
}
