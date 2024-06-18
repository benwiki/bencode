import 'package:flutter/material.dart';
import 'package:niederwerfung/amount_changer.dart';
import 'package:niederwerfung/context_extensions.dart';
import 'package:niederwerfung/utility.dart';

class NumberOfProstrationsChanger extends StatefulWidget {
  const NumberOfProstrationsChanger({
    super.key,
    required this.onChanged,
  });

  final Function(double) onChanged;

  @override
  State<NumberOfProstrationsChanger> createState() =>
      _NumberOfProstrationsChangerState();
}

class _NumberOfProstrationsChangerState
    extends State<NumberOfProstrationsChanger> {
  double _numberOfProstrations = 10;

  @override
  Widget build(BuildContext context) {
    return AmountChanger(
      title: "${context.text.numberOfProstrations}:",
      amountChangerValues: const [
        [-1, 1],
        [-10, 10],
        [-108, 108]
      ],
      changeAmountBy: (value) => _changeNumberOfProstrationsBy(value),
      getAmount: () => _numberOfProstrations,
      textColor: context.appColors.whiteStrong,
      buttonTextColor: context.appColors.blueDeep,
    );
  }

  _changeNumberOfProstrationsBy(double amount) {
    setState(() {
      _numberOfProstrations = constrain(_numberOfProstrations + amount, min: 1);
      widget.onChanged(_numberOfProstrations);
    });
  }
}
