import 'dart:math' as math;

import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:prostrationcounter/core/color_extension.dart';
import 'package:prostrationcounter/main.dart';
import 'package:shared_preferences/shared_preferences.dart';
// import 'package:url_launcher/url_launcher_string.dart';
import 'package:url_launcher/url_launcher.dart';


double constrain(num val, {num? min, num? max}) {
  return math
      .min(
        math.max(val, min ?? double.negativeInfinity),
        max ?? double.infinity,
      )
      .toDouble();
}

Future<void> waitForSeconds(double seconds) {
  return waitForMilliseconds(seconds * 1000);
}

Future<void> waitForMilliseconds(double milliseconds) {
  return Future.delayed(Duration(milliseconds: milliseconds.toInt()));
}

Future<void> initLanguage(BuildContext context) async {
  final prefs = await SharedPreferences.getInstance();
  final locale = Locale(prefs.getString("language") ?? "en");
  if (!context.mounted) return;
  NwApp.of(context)?.setLocale(locale);
}

class Link {
  final String text;
  final String url;

  Link(this.text, this.url);
}

// RichText insertLinks(String text, Map<String, Link> replace) {
//   final parts = text.split(RegExp(r"(\[.*\])"));
//   final children = <TextSpan>[];
//   for (final part in parts) {
//     if (!(part.startsWith("[") && part.endsWith("]"))) {
//       children.add(TextSpan(text: part));
//     }
//     final link = replace[part.substring(1, part.length - 1)];
//     if (link == null) {
//       children.add(TextSpan(text: part));
//     }
//     for (MapEntry<String, Link> e in replace.entries) {
//       if (part == e.key) {
//         final link = e.value;
//         children.add(
//           TextSpan(
//             text: link.text,
//             style: const TextStyle(
//               color: Colors.blue,
//               decoration: TextDecoration.underline,
//             ),
//             recognizer: TapGestureRecognizer()
//               ..onTap = () => launchUrlString(link.url),
//           ),
//         );
//         break;
//       }
//     }
//   }
//   return RichText(text: TextSpan(children: children));
// }

/// The text contains links in the format [text;url]
RichText replaceLinks(String text, {TextStyle? textStyle}) {
  String newText = "";
  String linkText = "";
  final children = <TextSpan>[];
  for (String char in text.characters) {
    if (!["[", ";", "]"].contains(char)) {
      newText += char;
    } else if (char == "[") {
      children.add(
        TextSpan(
          text: newText,
          style: textStyle ??
              const TextStyle(
                color: Colors.black,
              ),
        ),
      );
      newText = "";
    } else if (char == ";") {
      linkText = newText;
      newText = "";
    } else if (char == "]") {
      children.add(
        TextSpan(
          text: linkText,
          style: textStyle?.copyWith(
                color: Colors.blue.darken(0.2),
                decoration: TextDecoration.underline,
              ) ??
              TextStyle(
                color: Colors.blue.darken(0.2),
                decoration: TextDecoration.underline,
              ),
          recognizer: TapGestureRecognizer()
            ..onTap = launcherOf(newText),
        ),
      );
      newText = "";
    }
  }
  if (newText != "") {
    children.add(
      TextSpan(
        text: newText,
        style: textStyle ??
            const TextStyle(
              color: Colors.black,
            ),
      ),
    );
  }
  return RichText(text: TextSpan(children: children));
}

Function() launcherOf(String link) {
  return () async => await launchUrl(Uri.parse(link));
}