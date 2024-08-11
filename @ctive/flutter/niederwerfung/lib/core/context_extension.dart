import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:niederwerfung/core/surface/nw_colors.dart';

extension BuildContextX on BuildContext {
  AppLocalizations get text => AppLocalizations.of(this)!;
  ThemeData get theme => Theme.of(this);
  NwColors get appColors => theme.extension<NwColors>()!;
}