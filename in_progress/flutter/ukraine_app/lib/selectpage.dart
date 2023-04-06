import 'package:flutter/material.dart';

class SelectPage extends StatelessWidget {
  const SelectPage({Key? key, required this.title, required this.buttons})
      : super(key: key);

  final String title;
  final ListView buttons;

  @override
  Widget build(BuildContext context) =>
      Scaffold(appBar: AppBar(title: Text(title)), body: buttons);
}
