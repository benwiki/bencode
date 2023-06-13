import 'package:flutter/material.dart';

class AmountChanger extends StatelessWidget {
  final Function(int) changeAmountBy;
  final Function getAmount;
  final String title;
  final String? unit;
  final List<List>? amountChangerValues;

  const AmountChanger(
      {super.key,
      required this.changeAmountBy,
      required this.getAmount,
      this.title = "Title",
      this.unit,
      this.amountChangerValues});

  @override
  Widget build(BuildContext context) {
    final normalTextStyle =
        TextStyle(fontSize: 20, color: Theme.of(context).colorScheme.surface);
    const amountTextStyle = TextStyle(fontSize: 40, color: Colors.white);

    return Column(children: [
      Row(mainAxisAlignment: MainAxisAlignment.center, children: [
        Text(title, style: normalTextStyle),
        const SizedBox(width: 20),
        Text(getAmount().toString(), style: amountTextStyle),
        if (unit != null) ...[
          const SizedBox(width: 20),
          Text(unit ?? '', style: normalTextStyle)
        ]
      ]),
      const SizedBox(height: 10),
      buildButtonMatrix()
    ]);
  }

  Widget buildButtonMatrix() {
    return Column(children: [
      for (int i = 0; i < (amountChangerValues?.length ?? 0); ++i) ...[
        if (i > 0) const SizedBox(height: 10),
        Row(mainAxisAlignment: MainAxisAlignment.center, children: [
          for (int j = 0; j < (amountChangerValues?[i].length ?? 0); ++j) ...[
            if (j > 0) const SizedBox(width: 10),
            buildAmountChangeButton(amountChangerValues?[i][j] ?? 0)
          ]
        ])
      ]
    ]);
  }

  Widget buildAmountChangeButton(int changeValue) {
    return SizedBox(
        width: 100,
        height: 45,
        child: ElevatedButton(
            onPressed: () => changeAmountBy(changeValue),
            style: ElevatedButton.styleFrom(
                shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(15))),
            child: Text('${changeValue > 0 ? '+' : ''}$changeValue',
                style: const TextStyle(
                    fontSize: 20, fontWeight: FontWeight.bold))));
  }
}
