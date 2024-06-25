import 'package:flutter/material.dart';
import 'package:niederwerfung/amount_changer.dart';
import 'package:niederwerfung/context_extensions.dart';
import 'package:niederwerfung/prostrations_model.dart';
import 'package:niederwerfung/utility.dart';
import 'package:provider/provider.dart';

class NumberOfProstrationsChanger extends StatefulWidget {
  const NumberOfProstrationsChanger({
    super.key,
    this.onChanged,
  });

  final Function(double)? onChanged;

  @override
  State<NumberOfProstrationsChanger> createState() =>
      _NumberOfProstrationsChangerState();
}

class _NumberOfProstrationsChangerState
    extends State<NumberOfProstrationsChanger> {
  @override
  Widget build(BuildContext context) {
    final prostrationsModel = Provider.of<ProstrationsModel>(context);
    print("changer rebuit ------------");
    
    return AmountChanger(
      title: "${context.text.numberOfProstrations}:",
      amountChangerValues: const [
        [-1, 1],
        [-10, 10],
        [-108, 108]
      ],
      changeAmountBy: (value) {
        prostrationsModel.changeNumberOfProstrationsBy(value);
        setState(() {});
      },
      amount: prostrationsModel.numberOfProstrations,
      textColor: context.appColors.whiteStrong,
      buttonTextColor: context.appColors.blueDeep,
    );
  }
}
