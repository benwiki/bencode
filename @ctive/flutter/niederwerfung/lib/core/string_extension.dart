import 'package:flutter/material.dart';
import 'package:prostrationcounter/core/utility.dart';

extension StringX on String {
  RichText link({TextStyle? textStyle}) {
    return replaceLinks(this, textStyle: textStyle);
  }
}