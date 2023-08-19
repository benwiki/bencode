import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:edumap/auth.dart';
import 'package:edumap/content_assets.dart';
import 'package:edumap/content_viewer.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:youtube_player_flutter/youtube_player_flutter.dart';

final FirebaseFirestore _db = FirebaseFirestore.instance;

class MyVideoPlayer extends StatefulWidget {
  MyVideoPlayer(this.nodei, this.i, this.url, this.cred, this.inf, this.eng,
      this.creator, this.lim);

  String creator;
  Map cred, inf, eng;
  int i;
  int lim;
  int nodei;
  String url;

  State<StatefulWidget> createState() =>
      MyVideoPlayerState(nodei, i, url, [cred, inf, eng]);
}

class MyVideoPlayerState extends State<MyVideoPlayer> {
  MyVideoPlayerState(this.nodei, this.contenti, this.url, List<Map> values) {
    this.values = values;
  }

  YoutubePlayerController ytController;
  int contenti, nodei;
  String url;
  List<Map> values;

  @override
  void dispose() async {
    super.dispose();
  }

  @override
  void initState() {
    super.initState();
    SystemChrome.setPreferredOrientations(DeviceOrientation.values);
    ytController = YoutubePlayerController(
      initialVideoId: YoutubePlayer.convertUrlToId(url),
      flags: YoutubePlayerFlags(autoPlay: false, forceHD: true),
    );
  }

  @override
  Widget build(BuildContext context) {
    return YoutubePlayerBuilder(
        player: YoutubePlayer(controller: ytController),
        builder: (context, player) => Scaffold(
            appBar: buildAppBar(context),
            body: buildBody(context, player),
            floatingActionButton: buildFABs(context)));
  }

  buildAppBar(context) => AppBar(
      title: Text('Content viewer'),
      automaticallyImplyLeading: false,
      leading: IconButton(
          icon: Icon(Icons.arrow_back),
          onPressed: () async {
            Navigator.pop(context);
            if (user.signedIn()) {
              var doc = await _db.collection('Videos').doc('v$contenti').get();
              if (shouldDeleteContent(doc.data()['cred'], widget.lim)) {
                await _db.collection('Map_details').doc('node$nodei').update({
                  'Videos': FieldValue.arrayRemove([contenti])
                });
                var val =
                    await _db.collection('Videos').doc('v$contenti').get();
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

  buildBody(context, player) => Container(
      decoration: BoxDecoration(border: Border.all(color: Colors.black)),
      child: Column(crossAxisAlignment: CrossAxisAlignment.end, children: [
        player,
        SizedBox(height: 50, width: 2),
        Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [getFeedbackContainer(context)])
      ]));

  buildFABs(context) => Stack(children: [
        Positioned(
            child: Row(
                mainAxisAlignment: MainAxisAlignment.end,
                children: [SizedBox(width: 10), SizedBox(width: 5)]))
      ]);

  getFeedbackContainer(context) => Container(
      decoration:
          BoxDecoration(border: Border.all(color: Colors.grey, width: 3)),
      padding: EdgeInsets.fromLTRB(25, 25, 25, 25),
      child: Column(
          crossAxisAlignment: CrossAxisAlignment.end,
          children: getFeedbackElements(context)));

  List<Widget> getFeedbackElements(context) =>
      List.generate(3, (i) => buildColumn(context, i));

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
                    'Videos',
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
