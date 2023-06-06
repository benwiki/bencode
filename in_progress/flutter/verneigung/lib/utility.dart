import 'package:flutter/material.dart';

class SizedWidget extends SizedBox {
  SizedWidget(BuildContext context,
      {super.key, var wRate = 50, var hRate = 50, Widget? child})
      : super(
            width: wRate != null ? sized(context, wRate: wRate / 360) : null,
            height: hRate != null ? sized(context, hRate: hRate / 762) : null,
            child: child);
}

double sized(BuildContext context, {var wRate, var hRate}) {
  if (hRate == null && wRate == null) {
    throw ArgumentError("You must define either wRate or hRate!");
  }
  if (hRate != null && wRate != null) {
    throw ArgumentError("You mustn't define both wRate and hRate!");
  }
  if (hRate != null) return MediaQuery.of(context).size.height * hRate;
  return MediaQuery.of(context).size.width * wRate;
}
