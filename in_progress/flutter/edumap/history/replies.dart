import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:edumap/auth.dart';
import 'package:edumap/content_assets.dart';
import 'package:edumap/my_content.dart';
import 'package:edumap/utility.dart';
import 'package:flutter/material.dart';

final FirebaseFirestore _db = FirebaseFirestore.instance;

class Replies extends StatefulWidget {
  Replies(this.contenttype, this.contenti, this.commenttype, this.commenti);

  final int commenti, contenti;
  final String commenttype, contenttype;

  @override
  RepliesState createState() => RepliesState(contenttype, contenti);
}

class RepliesState extends State<Replies> {
  RepliesState(this.contenttype, this.contenti);

  int contenti;
  String contenttype;
  int l;
  String sortRule = SortRule.quality.str;
  bool sorted = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(appBar: buildAppBar(), body: buildBody());
  }

  buildAppBar() => AppBar(title: Text('Replies'), actions: [
        Row(children: [
          getSortRuleSelector((rule) => setState(() {
                sortRule = rule;
              })),
          SizedBox(width: 5)
        ]),
        IconButton(icon: Icon(Icons.sync), onPressed: () => setState(() {}))
      ]);

  buildBody() => StreamBuilder(
      stream: _db.collection(contenttype[0] + '_replies').snapshots(),
      builder: (context, snapshot) {
        if (!snapshot.hasData) return CenteredLoadingSign();

        var snap = snapshot.data.docs
            .firstWhere((doc) => doc.id == 'r$contenti', orElse: () => null);
        if (snap != null) {
          snap = snap.data();
        }

        List rkeys;
        initReplyKeys(rkeys, snap);
        return buildFeedbackScrollView(snap, rkeys);
      });

  initReplyKeys(rkeys, snap) {
    if (snap != null && snap[widget.commenttype] != null) {
      Map commentsnap = snap[widget.commenttype][widget.commenti];
      l = commentsnap.length - 1;
      rkeys = commentsnap.keys
          .where((e) => commentsnap[e].length != 0)
          .map((f) => int.parse(f))
          .toList();
      rkeys = rkeys.reversed.toList();
      if (rkeys.length != 0 && !sorted) {
        sorted = true;
        sortReplyKeys(rkeys, commentsnap);
      }
    }
  }

  sortReplyKeys(rkeys, commentsnap) {
    if (sortRule == SortRule.quality.str) {
      rkeys.sort((j, i) =>
          convert(commentsnap['$i']).compareTo(convert(commentsnap['$j'])));
    } else if (sortRule == SortRule.latest.str) {}
  }

  buildFeedbackScrollView(snap, rkeys) => SingleChildScrollView(
          child: Column(children: [
        ReplyAdder(contenti, widget.commenti, contenttype, widget.commenttype),
        if (snap != null && snap[widget.commenttype] != null)
          Column(
              children: List.generate(
                  rkeys.length,
                  (i) => getCard(
                      snap[widget.commenttype][widget.commenti]['${rkeys[i]}'],
                      rkeys[i])))
      ]));

  getCard(temp, rkey) => Card(
          child: Row(children: [
        SizedBox(width: 20),
        buildFeedbackContainer(context, temp, rkey),
        if (temp['uid'] == user.id)
          Container(
              width: 25,
              child: GestureDetector(
                  child: Icon(Icons.delete),
                  onTap: () => Deleter(context).deletereply(
                        contenti,
                        widget.commenti,
                        rkey,
                        contenttype,
                        widget.commenttype,
                      )))
      ]));

  buildFeedbackContainer(context, temp, rkey) => Container(
      width: (temp['uid'] == user.id)
          ? MediaQuery.of(context).size.width - 55
          : MediaQuery.of(context).size.width - 30,
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        SizedBox(height: 15),
        Row(children: [
          if (temp['imgurl'] != null)
            Container(
                width: 32,
                height: 32,
                decoration: BoxDecoration(shape: BoxShape.circle),
                child: ClipRRect(
                    borderRadius: BorderRadius.circular(100.0),
                    child: Image.network(temp['imgurl']))),
          SizedBox(width: 5),
          Text(temp['name'] + ": ", style: TextStyle(fontSize: 15))
        ]),
        SizedBox(height: 3),
        ConstrainedBox(
            constraints: BoxConstraints(
                maxWidth: MediaQuery.of(context).size.width - 30),
            child: Text(temp['text'],
                style: TextStyle(fontSize: 17), maxLines: 30)),
        SizedBox(height: 10),
        Row(children: [
          Text("Helpful?   ", style: TextStyle(fontSize: 15)),
          RatingIcons(
            temp,
            (String rating) async => replyf(rkey, rating),
            temp['uid'],
            k: ValueKey(rkey),
          ),
        ]),
      ]));

  Future<void> replyf(int replyi, String rating) async {
    await _db.runTransaction((transaction) async {
      var value = await transaction
          .get(_db.collection(contenttype[0] + '_replies').doc('r$contenti'));
      Map ratings = value.data()[widget.commenttype];
      ratings = ratings[widget.commenti];
      ratings = ratings['$replyi'];
      if (rating != "neutrals") {
        var opp = (rating == 'likes') ? 'dislikes' : 'likes';
        updateList(ratings[rating], user.id);
        ratings[opp].remove(user.id);
      } else {
        ratings['likes'].remove(user.id);
        ratings['dislikes'].remove(user.id);
      }
      transaction.set(value.reference, {widget.commenttype: ratings},
          SetOptions(merge: true));
    });
  }
}

class ReplyAdder extends StatefulWidget {
  ReplyAdder(this.i, this.commenti, this.typecontent, this.typecomment);

  int commenti;
  int i;
  String typecomment;
  String typecontent;

  @override
  _ReplyAdderState createState() =>
      _ReplyAdderState(i, commenti, typecontent, typecomment);
}

class _ReplyAdderState extends State<ReplyAdder> {
  _ReplyAdderState(this.i, this.commenti, this.typecontent, this.typecomment);

  TextEditingController c = TextEditingController();
  int commenti;
  var data;
  int i;
  bool pressed = false;
  String typecomment;
  String typecontent;

  Future<void> savereply(String reply) async {
    await _db.runTransaction((transaction) async {
      var value = await transaction
          .get(_db.collection(typecontent[0] + '_replies').doc('r$i'));
      data = value.data()[typecomment];
      int index = value.data()[typecomment][commenti].length;
      data[commenti]['$index'] = {
        'name': user.name,
        'text': reply,
        'uid': user.id,
        'likes': [],
        'dislikes': [],
        'imgurl': user.profileURL
      };
      transaction.set(
          value.reference, {typecomment: data}, SetOptions(merge: true));
    });
  }

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Container(
            width: MediaQuery.of(context).size.width - 100,
            height: 50,
            child: TextFormField(
                autocorrect: true,
                cursorRadius: Radius.circular(5),
                controller: c,
                decoration: new InputDecoration(
                  border: InputBorder.none,
                  contentPadding: EdgeInsets.fromLTRB(30, 0, 30, 5),
                  hintText: "Type here...",
                  fillColor: Colors.black,
                ),
                validator: (txt) =>
                    (txt.length == 0) ? "Text field is empty..." : null)),
        Container(
            child: ElevatedButton(
          child: Text("Add"),
          onPressed: () async {
            if (user.notSignedIn()) return await user.showSignInAlert(context);
            await savereply(c.text);
            setState(() {});
          },
        ))
      ],
    );
  }
}
