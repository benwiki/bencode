import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:intl/intl.dart' as intl;

import 'app_localizations_de.dart';
import 'app_localizations_en.dart';

// ignore_for_file: type=lint

/// Callers can lookup localized strings with an instance of AppLocalizations
/// returned by `AppLocalizations.of(context)`.
///
/// Applications need to include `AppLocalizations.delegate()` in their app's
/// `localizationDelegates` list, and the locales they support in the app's
/// `supportedLocales` list. For example:
///
/// ```dart
/// import 'l10n/app_localizations.dart';
///
/// return MaterialApp(
///   localizationsDelegates: AppLocalizations.localizationsDelegates,
///   supportedLocales: AppLocalizations.supportedLocales,
///   home: MyApplicationHome(),
/// );
/// ```
///
/// ## Update pubspec.yaml
///
/// Please make sure to update your pubspec.yaml to include the following
/// packages:
///
/// ```yaml
/// dependencies:
///   # Internationalization support.
///   flutter_localizations:
///     sdk: flutter
///   intl: any # Use the pinned version from flutter_localizations
///
///   # Rest of dependencies
/// ```
///
/// ## iOS Applications
///
/// iOS applications define key application metadata, including supported
/// locales, in an Info.plist file that is built into the application bundle.
/// To configure the locales supported by your app, you’ll need to edit this
/// file.
///
/// First, open your project’s ios/Runner.xcworkspace Xcode workspace file.
/// Then, in the Project Navigator, open the Info.plist file under the Runner
/// project’s Runner folder.
///
/// Next, select the Information Property List item, select Add Item from the
/// Editor menu, then select Localizations from the pop-up menu.
///
/// Select and expand the newly-created Localizations item then, for each
/// locale your application supports, add a new item and select the locale
/// you wish to add from the pop-up menu in the Value field. This list should
/// be consistent with the languages listed in the AppLocalizations.supportedLocales
/// property.
abstract class AppLocalizations {
  AppLocalizations(String locale)
      : localeName = intl.Intl.canonicalizedLocale(locale.toString());

  final String localeName;

  static AppLocalizations? of(BuildContext context) {
    return Localizations.of<AppLocalizations>(context, AppLocalizations);
  }

  static const LocalizationsDelegate<AppLocalizations> delegate =
      _AppLocalizationsDelegate();

  /// A list of this localizations delegate along with the default localizations
  /// delegates.
  ///
  /// Returns a list of localizations delegates containing this delegate along with
  /// GlobalMaterialLocalizations.delegate, GlobalCupertinoLocalizations.delegate,
  /// and GlobalWidgetsLocalizations.delegate.
  ///
  /// Additional delegates can be added by appending to this list in
  /// MaterialApp. This list does not have to be used at all if a custom list
  /// of delegates is preferred or required.
  static const List<LocalizationsDelegate<dynamic>> localizationsDelegates =
      <LocalizationsDelegate<dynamic>>[
    delegate,
    GlobalMaterialLocalizations.delegate,
    GlobalCupertinoLocalizations.delegate,
    GlobalWidgetsLocalizations.delegate,
  ];

  /// A list of this localizations delegate's supported locales.
  static const List<Locale> supportedLocales = <Locale>[
    Locale('de'),
    Locale('en')
  ];

  /// The name of the app.
  ///
  /// In en, this message translates to:
  /// **'Prostrations'**
  String get appName;

  /// No description provided for @homeScreenName.
  ///
  /// In en, this message translates to:
  /// **'Prostrations'**
  String get homeScreenName;

  /// No description provided for @gongInterval.
  ///
  /// In en, this message translates to:
  /// **'Gong interval'**
  String get gongInterval;

  /// No description provided for @sec.
  ///
  /// In en, this message translates to:
  /// **'sec.'**
  String get sec;

  /// No description provided for @numberOfProstrations.
  ///
  /// In en, this message translates to:
  /// **'Number of prostrations'**
  String get numberOfProstrations;

  /// No description provided for @mantraIsOn.
  ///
  /// In en, this message translates to:
  /// **'Mantra is on'**
  String get mantraIsOn;

  /// No description provided for @mantraIsOff.
  ///
  /// In en, this message translates to:
  /// **'Mantra is off'**
  String get mantraIsOff;

  /// No description provided for @title.
  ///
  /// In en, this message translates to:
  /// **'Title'**
  String get title;

  /// No description provided for @start.
  ///
  /// In en, this message translates to:
  /// **'Start'**
  String get start;

  /// No description provided for @stop.
  ///
  /// In en, this message translates to:
  /// **'STOP'**
  String get stop;

  /// No description provided for @mantraPaceWarning.
  ///
  /// In en, this message translates to:
  /// **'Gong interval is too short for mantra. At least 8 seconds are required.'**
  String get mantraPaceWarning;

  /// No description provided for @gongIntervalWarning.
  ///
  /// In en, this message translates to:
  /// **'Gong interval is too short for mantra. At least 8 seconds are required. Mantra turned off.'**
  String get gongIntervalWarning;

  /// No description provided for @support.
  ///
  /// In en, this message translates to:
  /// **'I want to support the development'**
  String get support;

  /// No description provided for @supportTitle.
  ///
  /// In en, this message translates to:
  /// **'Support'**
  String get supportTitle;

  /// No description provided for @supportText.
  ///
  /// In en, this message translates to:
  /// **'If you want to give feedback about the app, or you have ideas, please contact me on this email address:\n[govindapp@proton.me;mailto:govindapp@proton.me]\n\nIf you like the app, please please consider donating via PayPal:\n[paypal.me/benkex;https://paypal.me/benkex]\n\nEven 1€ (1\$) helps.'**
  String get supportText;

  /// No description provided for @back.
  ///
  /// In en, this message translates to:
  /// **'Back'**
  String get back;

  /// No description provided for @specialThanks.
  ///
  /// In en, this message translates to:
  /// **'Special thanks'**
  String get specialThanks;

  /// No description provided for @specialThanksText.
  ///
  /// In en, this message translates to:
  /// **'Special thanks to all the people and organizations listed here!'**
  String get specialThanksText;

  /// No description provided for @singingBowl_1.
  ///
  /// In en, this message translates to:
  /// **'The sound comes from [SoundEffectStudio;https://www.youtube.com/@SoundEffectStudioNo.1], the link to the video: [Singing Bowl (Deep Sound) - Sound Effect;https://youtu.be/y96ARieC9HY].'**
  String get singingBowl_1;
}

class _AppLocalizationsDelegate
    extends LocalizationsDelegate<AppLocalizations> {
  const _AppLocalizationsDelegate();

  @override
  Future<AppLocalizations> load(Locale locale) {
    return SynchronousFuture<AppLocalizations>(lookupAppLocalizations(locale));
  }

  @override
  bool isSupported(Locale locale) =>
      <String>['de', 'en'].contains(locale.languageCode);

  @override
  bool shouldReload(_AppLocalizationsDelegate old) => false;
}

AppLocalizations lookupAppLocalizations(Locale locale) {
  // Lookup logic when only language code is specified.
  switch (locale.languageCode) {
    case 'de':
      return AppLocalizationsDe();
    case 'en':
      return AppLocalizationsEn();
  }

  throw FlutterError(
      'AppLocalizations.delegate failed to load unsupported locale "$locale". This is likely '
      'an issue with the localizations generation tool. Please file an issue '
      'on GitHub with a reproducible sample app and the gen-l10n configuration '
      'that was used.');
}
