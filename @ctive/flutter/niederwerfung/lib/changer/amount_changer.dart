import 'package:flutter/material.dart';
import 'package:prostrationcounter/core/context_extension.dart';

class AmountChanger extends StatelessWidget {
  final Function(double) changeAmountBy;
  final num amount;
  final String title;
  final String? unit;
  final List<List<num>> amountChangerValues;
  final Color? textColor;
  final Color? buttonColor;
  final Color? buttonTextColor;

  int get valuesLen => amountChangerValues.length;
  int valuesLenAt(int index) => amountChangerValues[index].length;

  const AmountChanger({
    super.key,
    required this.changeAmountBy,
    required this.amount,
    required this.amountChangerValues,
    this.title = "Title",
    this.unit,
    this.textColor,
    this.buttonColor,
    this.buttonTextColor,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        buildLabel(context),
        const SizedBox(height: 10),
        buildButtonMatrix(context)
      ],
    );
  }

  Widget buildLabel(BuildContext context) {
    final baseTextStyle =
        TextStyle(color: textColor ?? context.appColors.blackStrong);
    final normalTextStyle = baseTextStyle.copyWith(fontSize: 20);
    final amountTextStyle = baseTextStyle.copyWith(fontSize: 40);

    return Column(
      children: [
        Text(title, style: normalTextStyle),
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(convertToText(amount), style: amountTextStyle),
            if (unit != null) ...[
              const SizedBox(width: 10),
              Text(unit ?? '', style: normalTextStyle)
            ]
          ],
        )
      ],
    );
  }

  String convertToText(num value) {
    return value % 1 == 0 ? value.toInt().toString() : value.toStringAsFixed(1);
  }

  Widget buildButtonMatrix(BuildContext context) {
    return Column(
      children: [
        for (int i = 0; i < valuesLen; ++i) ...[
          if (i > 0) const SizedBox(height: 10),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              for (int j = 0; j < valuesLenAt(i); ++j) ...[
                if (j > 0) const SizedBox(width: 10),
                buildAmountChangeButton(
                    amountChangerValues[i][j].toDouble(), context),
              ]
            ],
          )
        ]
      ],
    );
  }

  Widget buildAmountChangeButton(double changeValue, BuildContext context) {
    String prefix = changeValue > 0 ? '+' : '';
    String buttonText = changeValue % 1 == 0
        ? '$prefix${changeValue.toInt()}'
        : '$prefix${changeValue.toStringAsFixed(1)}';

    return SizedBox(
      width: 100,
      height: 45,
      child: ElevatedButton(
        onPressed: () => changeAmountBy(changeValue),
        style: ElevatedButton.styleFrom(
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(15),
          ),
          backgroundColor: buttonColor ?? context.appColors.butterMedium,
        ),
        child: Text(
          buttonText,
          style: TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
            color: buttonTextColor ?? context.appColors.blackStrong,
          ),
        ),
      ),
    );
  }
}
