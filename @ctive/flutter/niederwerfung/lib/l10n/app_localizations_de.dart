// ignore: unused_import
import 'package:intl/intl.dart' as intl;
import 'app_localizations.dart';

// ignore_for_file: type=lint

/// The translations for German (`de`).
class AppLocalizationsDe extends AppLocalizations {
  AppLocalizationsDe([String locale = 'de']) : super(locale);

  @override
  String get appName => 'Verneigungen';

  @override
  String get homeScreenName => 'Verneigungen';

  @override
  String get gongInterval => 'Gong-Intervall';

  @override
  String get sec => 'Sek.';

  @override
  String get numberOfProstrations => 'Anzahl der Verneigungen';

  @override
  String get mantraIsOn => 'Mantra eingeschaltet';

  @override
  String get mantraIsOff => 'Mantra ausgeschaltet';

  @override
  String get title => 'Titel';

  @override
  String get start => 'Start';

  @override
  String get stop => 'STOP';

  @override
  String get mantraPaceWarning =>
      'Gong-Intervall ist zu kurz für Mantra. Mindestens 8 Sekunden sind erforderlich.';

  @override
  String get gongIntervalWarning =>
      'Gong-Intervall ist zu kurz für Mantra. Mindestens 8 Sekunden sind erforderlich. Mantra ausgeschaltet.';

  @override
  String get support => 'Ich möchte die Entwicklung unterstützen';

  @override
  String get supportTitle => 'Unterstützung';

  @override
  String get supportText =>
      'Wenn Sie Feedback zur App geben möchten oder Ideen haben, kontaktieren Sie mich bitte unter dieser E-Mail-Adresse:\n[govindapp@proton.me;mailto:govindapp@proton.me]\n\nWenn Ihnen die App gefällt, erwägen Sie bitte eine Spende über PayPal:\n[paypal.me/benkex;https://paypal.me/benkex]\n\nAuch 1€ hilft.';

  @override
  String get back => 'Zurück';

  @override
  String get specialThanks => 'Besonderer Dank';

  @override
  String get specialThanksText =>
      'Besonderer Dank an alle die hier aufgelisteten Menschen und Organisationen!';

  @override
  String get singingBowl_1 =>
      'Der Klang kommt von [SoundEffectStudio;https://www.youtube.com/@SoundEffectStudioNo.1], der Link zum Video: [Singing Bowl (Deep Sound) - Sound Effect;https://youtu.be/y96ARieC9HY].';
}
