import 'package:flutter/material.dart';
import 'package:niederwerfung/amount_changer.dart';
import 'package:niederwerfung/context_extensions.dart';
import 'package:niederwerfung/utility.dart';

class GongIntervalChanger extends StatefulWidget {
  const GongIntervalChanger({
    super.key,
    required this.onChanged,
  });

  final Function(double) onChanged;

  @override
  State<GongIntervalChanger> createState() => _GongIntervalChangerState();
}

class _GongIntervalChangerState extends State<GongIntervalChanger> {
  double _gongInterval = 10;

  @override
  Widget build(BuildContext context) {
    return AmountChanger(
      title: "${context.text.gongInterval}:",
      unit: context.text.sec,
      amountChangerValues: const [
        [-0.1, 0.1],
        [-1, 1],
        [-10, 10]
      ],
      changeAmountBy: (value) => _changeGongIntervalBy(value),
      getAmount: () => _gongInterval,
      textColor: context.appColors.whiteStrong,
      buttonTextColor: context.appColors.blueDeep,
    );
  }

  _changeGongIntervalBy(double amount) {
    setState(() {
      _gongInterval = constrain(_gongInterval + amount, min: 1, max: 99);
      widget.onChanged(_gongInterval);
    });
  }
}
