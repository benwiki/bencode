import 'package:niederwerfung/text_styles.dart';
import 'package:flutter/material.dart';

@immutable
class NwTextStyles extends ThemeExtension<NwTextStyles> {
  const NwTextStyles({
    required this.h1,
    required this.h2,
    required this.h3,
    required this.h4,
    required this.h5,
    required this.b1,
    required this.b2,
    required this.b3,
    required this.b4,
    required this.b5,
  });
  final TextStyle h1;
  final TextStyle h2;
  final TextStyle h3;
  final TextStyle h4;
  final TextStyle h5;
  final TextStyle b1;
  final TextStyle b2;
  final TextStyle b3;
  final TextStyle b4;
  final TextStyle b5;

  static const standard = NwTextStyles(
    h1: TextStyles.titleExtraLarge,
    h2: TextStyles.titleLarge,
    h3: TextStyles.titleMedium,
    h4: TextStyles.titleSmall,
    h5: TextStyles.titleExtraSmall,
    b1: TextStyles.boldText,
    b2: TextStyles.smallRegularTitle,
    b3: TextStyles.regularText,
    b4: TextStyles.smallRegularText,
    b5: TextStyles.baseText,
  );

  @override
  ThemeExtension<NwTextStyles> copyWith({
    TextStyle? h1,
    TextStyle? h2,
    TextStyle? h3,
    TextStyle? h4,
    TextStyle? h5,
    TextStyle? b1,
    TextStyle? b2,
    TextStyle? b3,
    TextStyle? b4,
    TextStyle? b5,
  }) {
    return NwTextStyles(
      h1: h1 ?? this.h1,
      h2: h2 ?? this.h2,
      h3: h3 ?? this.h3,
      h4: h4 ?? this.h4,
      h5: h5 ?? this.h5,
      b1: b1 ?? this.b1,
      b2: b2 ?? this.b2,
      b3: b3 ?? this.b3,
      b4: b4 ?? this.b4,
      b5: b5 ?? this.b5,
    );
  }

  @override
  ThemeExtension<NwTextStyles> lerp(
    covariant ThemeExtension<NwTextStyles>? other,
    double t,
  ) {
    if (other is! NwTextStyles) return this;
    return NwTextStyles(
      h1: TextStyle.lerp(h1, other.h1, t) ?? h1,
      h2: TextStyle.lerp(h2, other.h2, t) ?? h2,
      h3: TextStyle.lerp(h3, other.h3, t) ?? h3,
      h4: TextStyle.lerp(h4, other.h4, t) ?? h4,
      h5: TextStyle.lerp(h5, other.h5, t) ?? h5,
      b1: TextStyle.lerp(b1, other.b1, t) ?? b1,
      b2: TextStyle.lerp(b2, other.b2, t) ?? b2,
      b3: TextStyle.lerp(b3, other.b3, t) ?? b3,
      b4: TextStyle.lerp(b4, other.b4, t) ?? b4,
      b5: TextStyle.lerp(b5, other.b5, t) ?? b5,
    );
  }
}
