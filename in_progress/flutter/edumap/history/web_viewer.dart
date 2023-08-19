import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:edumap/auth.dart';
import 'package:edumap/content_assets.dart';
import 'package:edumap/content_viewer.dart';
import 'package:edumap/utility.dart';
import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';

final FirebaseFirestore _db = FirebaseFirestore.instance;

class MyWebViewer extends StatefulWidget {
  MyWebViewer(this.nodei, this.i, this.url, this.cred, this.inf, this.eng,
      this.creator, this.lim);

  String creator;
  Map cred, inf, eng;
  int i;
  int lim;
  int nodei;
  String url;

  @override
  MyWebViewerState createState() =>
      MyWebViewerState(nodei, i, url, [cred, inf, eng]);
}

class MyWebViewerState extends State<MyWebViewer>
    with SingleTickerProviderStateMixin {
  MyWebViewerState(this.nodei, this.contenti, this.url, List<Map> values) {
    this.values = values;
  }

  WebViewController controller;
  int contenti, nodei;
  bool isLoading = true;
  String url;
  List<Map> values;

  @override
  void dispose() async {
    super.dispose();
  }

  Future<void> updateValues() async {
    await _db.collection('Articles').doc('a$contenti').get().then((val) {
      setState(() {
        values = [val.data()['cred'], val.data()['inf'], val.data()['eng']];
      });
    });
  }

  @override
  void initState() {
    super.initState();
    controller = WebViewController()
      ..loadRequest(Uri.parse(url))
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..setNavigationDelegate(NavigationDelegate(
        onPageStarted: (_) {
          setState(() {
            isLoading = false;
          });
        },
      ));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: buildAppBar(context),
        body: buildBody(context),
        floatingActionButton: buildFABs(context));
  }

  buildAppBar(context) => AppBar(
      title: Text('Content viewer'),
      automaticallyImplyLeading: false,
      leading: IconButton(
          icon: Icon(Icons.arrow_back),
          onPressed: () async {
            Navigator.pop(context);
            if (user.signedIn()) {
              var doc =
                  await _db.collection('Articles').doc('a$contenti').get();
              if (shouldDeleteContent(doc.data()['cred'], widget.lim)) {
                await _db.collection('Map_details').doc('node$nodei').update({
                  'Articles': FieldValue.arrayRemove([contenti])
                });
                var val =
                    await _db.collection('Articles').doc('a$contenti').get();
                String uid = val.data()['uid'];
                await _db.collection('Users').doc(uid).set({
                  'new_ib': true,
                  'Inbox': FieldValue.arrayUnion([
                    {'type': '2', 'read': false, 'title': val.data()['title']}
                  ])
                }, SetOptions(merge: true));
              }
            }
          }));

  buildBody(context) => Stack(children: [
        SizedBox(
            height: MediaQuery.of(context).size.height * (0.8),
            child: WebViewWidget(controller: controller)),
        if (isLoading) CenteredLoadingSign()
      ]);

  buildFABs(context) => Stack(children: [
        Positioned(
            child: Row(mainAxisAlignment: MainAxisAlignment.end, children: [
          SizedBox(width: 10),
          SizedBox(width: 10),
          FloatingActionButton(
              heroTag: null,
              child: Icon(Icons.thumbs_up_down),
              onPressed: () async {
                if (user.notSignedIn())
                  return await user.showSignInAlert(context);
                showDialog(
                    context: context,
                    builder: (dialogCxt) => Dialog(
                        child: FittedBox(
                            fit: BoxFit.fitHeight,
                            child: getFeedbackContainer(dialogCxt))));
              }),
          SizedBox(width: 5)
        ]))
      ]);

  getFeedbackContainer(context) => Container(
      decoration:
          BoxDecoration(border: Border.all(color: Colors.grey, width: 3)),
      padding: EdgeInsets.fromLTRB(25, 25, 25, 25),
      child: Column(
          crossAxisAlignment: CrossAxisAlignment.end,
          children: getFeedbackElements(context)));

  List<Widget> getFeedbackElements(context) =>
      List.generate(3, (i) => buildColumn(context, i)) +
      [
        Column(children: [
          SizedBox(height: 10),
          Container(
              child: ElevatedButton(
                  child: Text("OK", style: TextStyle(fontSize: 18)),
                  onPressed: () async {
                    Navigator.pop(context);
                    await updateValues();
                  }))
        ])
      ];

  // TODO: rename
  Column buildColumn(context, i) => Column(children: [
        Row(mainAxisAlignment: MainAxisAlignment.end, children: [
          ConstrainedBox(
            constraints: BoxConstraints(maxWidth: 150),
            child: Text(qualities[i] + "?",
                textAlign: TextAlign.end,
                style: TextStyle(
                    fontSize: 15,
                    color: Colors.black87,
                    decoration: TextDecoration.none)),
          ),
          SizedBox(width: 10),
          RatingIcons(
              values[i],
              (String rating) async => contentf(
                    'Articles',
                    short[i],
                    rating,
                    contenti,
                  ),
              widget.creator,
              k: ValueKey(i))
        ]),
        SizedBox(height: 10)
      ]);
}
