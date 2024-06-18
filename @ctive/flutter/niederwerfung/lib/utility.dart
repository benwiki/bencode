import 'dart:math' as math;

double constrain(num val, {num? min, num? max}) {
  return math
      .min(
        math.max(val, min ?? double.negativeInfinity),
        max ?? double.infinity,
      )
      .toDouble();
}
