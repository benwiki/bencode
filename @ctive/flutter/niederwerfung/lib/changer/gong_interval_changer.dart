import 'package:flutter/material.dart';
import 'package:niederwerfung/changer/amount_changer.dart';
import 'package:niederwerfung/core/context_extension.dart';
import 'package:niederwerfung/core/utility.dart';
import 'package:niederwerfung/model/chant_model.dart';
import 'package:niederwerfung/model/gong_interval_model.dart';
import 'package:provider/provider.dart';

class GongIntervalChanger extends StatefulWidget {
  const GongIntervalChanger({
    super.key,
  });

  @override
  State<GongIntervalChanger> createState() => _GongIntervalChangerState();
}

class _GongIntervalChangerState extends State<GongIntervalChanger> {
  late ChantModel chantModel;
  late GongIntervalModel gongIntervalModel;

  @override
  Widget build(BuildContext context) {
    chantModel = Provider.of<ChantModel>(context, listen: false);
    gongIntervalModel =
        Provider.of<GongIntervalModel>(context, listen: false);

    return AmountChanger(
      title: "${context.text.gongInterval}:",
      unit: context.text.sec,
      amountChangerValues: const [
        [-0.1, 0.1],
        [-1, 1],
        [-10, 10]
      ],
      changeAmountBy: (value) => _changeGongIntervalBy(value),
      amount: gongIntervalModel.gongInterval,
      textColor: context.appColors.whiteStrong,
      buttonTextColor: context.appColors.blueDeep,
    );
  }

  _changeGongIntervalBy(double amount) {
    double newValue = gongIntervalModel.gongInterval + amount;
    if (newValue < 8 && chantModel.chantIsOn) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        backgroundColor: context.appColors.blueDeep,
        content: Text(context.text.mantraPaceWarning),
        duration: const Duration(seconds: 3),
      ));
      chantModel.setChantState(false);
    }
    gongIntervalModel.changeValueBy(amount);
    setState(() {});
  }
}
