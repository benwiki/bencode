import 'dart:async';
import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';

import 'package:ukraine_app/main.dart';

class WebPage extends StatelessWidget {
  WebPage({Key? key}) : super(key: key);

  late final WebViewController _control;
  final GlobalKey _globalKey = GlobalKey();

  @override
  Widget build(BuildContext context) {
    return WillPopScope(
      onWillPop: _onBack,
      child: Scaffold(
        key: _globalKey,
        body: WebView(
          initialUrl: webpageURL,
          javascriptMode: JavascriptMode.unrestricted,
          onWebViewCreated: (webViewController) {
            _control = webViewController;
          },
          gestureNavigationEnabled: true,
        ),
      ),
    );
  }

  Future<bool> _onBack() async {
    if (!await _control.canGoBack()) return true;
    _control.goBack(); // perform webview back operation
    return false;
  }
}
