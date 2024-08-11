import 'dart:math' as math;

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