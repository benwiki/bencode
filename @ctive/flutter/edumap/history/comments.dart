import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:edumap/auth.dart';
import 'package:edumap/content_assets.dart';
import 'package:edumap/my_content.dart';
import 'package:edumap/reference.dart';
import 'package:edumap/replies.dart';
import 'package:edumap/utility.dart';
import 'package:flutter/material.dart';

final FirebaseFirestore _db = FirebaseFirestore.instance;

class Comments extends StatefulWidget {
  Comments(this.nodei, this.contenti, this.contenttype, this.k, this.lim)
      : super(key: k);

  final int contenti, lim, nodei;
  String contenttype;
  GlobalKey<CommentsState> k;

  @override
  CommentsState createState() => CommentsState(contenti, contenttype);
}

class CommentsState extends State<Comments> {
  CommentsState(this.contenti, this.contenttype);

  int contenti;
  String contenttype;
  int l, l2;
  GlobalKey<ScaffoldState> scaffold = GlobalKey<ScaffoldState>();
  String sortRule = SortRule.quality.str;
  bool sorted = false;

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        home: DefaultTabController(
            length: 3,
            child: Scaffold(
                key: scaffold,
                resizeToAvoidBottomInset: false,
                appBar: buildAppBar(context),
                body: buildBody())));
  }

  buildAppBar(context) => AppBar(
      title: Text("Responses"),
      leading: IconButton(
        icon: Icon(Icons.arrow_back),
        onPressed: () => Navigator.pop(context),
      ),
      actions: [
        Row(children: [
          getSortRuleSelector((rule) => setState(() {
                sortRule = rule;
              })),
          SizedBox(width: 5)
        ]),
        IconButton(icon: Icon(Icons.sync), onPressed: () => setState(() {})),
      ],
      bottom: TabBar(isScrollable: true, tabs: <Widget>[
        Tab(text: 'Other perspectives'),
        Tab(text: 'Content feedback'),
        Tab(text: 'Discussions'),
      ]));

  buildBody() => StreamBuilder(
      stream: _db.collection(contenttype[0] + '_comments').snapshots(),
      builder: (context, snapshot) {
        if (!snapshot.hasData)
          return TabBarView(
              children: List.generate(3, (_) => CenteredLoadingSign()));

        var snap = snapshot.data.docs
            .firstWhere((doc) => doc.id == 'c$contenti', orElse: () => null);
        Map temp = {'feedback': [], 'discussion': []};
        if (snap != null) {
          initTemp(snap, temp, 'feedback');
          initTemp(snap, temp, 'discussion');
        }

        return TabBarView(children: [
          RefShow(contenti, contenttype, widget.nodei, widget.k, scaffold,
              widget.lim,
              k2: GlobalKey<RefShowState>()),
          buildFeedbackScrollView(snap, temp, 'Good feedback?', 'feedback'),
          buildFeedbackScrollView(snap, temp, 'Helpful?', 'discussion'),
        ]);
      });

  initTemp(snap, temp, type) {
    if (snap.data()[type] == null) return;
    l = snap.data()[type].length - 1;
    temp[type] = snap
        .data()[type]
        .where((e) => e.length != 0)
        .toList()
        .reversed
        .toList();
    if (!sorted) sortComments(temp[type]);
  }

  sortComments(comments) {
    if (sortRule == SortRule.quality.str) {
      comments.sort((c2, c1) => convert(c1).compareTo(convert(c2)));
    } else if (sortRule == SortRule.latest.str) {}
  }

  buildFeedbackScrollView(snap, temp, message, type) => SingleChildScrollView(
          child: Column(children: [
        CommentAdder(contenti, contenttype, type),
        if (snap != null && temp[type] != null)
          Column(
              children: List.generate(temp[type].length,
                  (i) => getCard(temp[type][i], message, type)))
      ]));

  getCard(temp, message, type) => Card(
          child: Row(children: [
        SizedBox(width: 20),
        buildFeedbackContainer(context, temp, message, type),
        if (temp['uid'] == user.id)
          Container(
              width: 25,
              child: GestureDetector(
                  child: Icon(Icons.delete),
                  onTap: () => Deleter(context).deletecomment(
                        contenttype,
                        type,
                        contenti,
                        temp['i'],
                      )))
      ]));

  buildFeedbackContainer(context, temp, message, type) => Container(
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
                    child: Image.network(
                      temp['imgurl'],
                      fit: BoxFit.cover,
                    ))),
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
          Text(message, style: TextStyle(fontSize: 15)),
          RatingIcons(
            temp,
            (String rating) async => commentf(type, temp['i'], rating),
            temp['uid'],
            k: ValueKey(temp['i']),
          ),
          SizedBox(width: 40),
        ]),
        SizedBox(height: 15),
        Container(
            child: ElevatedButton(
          child: Text("Replies", style: TextStyle(fontSize: 15)),
          onPressed: () => Navigator.push(
            context,
            MaterialPageRoute(
                builder: (context) =>
                    Replies(contenttype, contenti, type, temp['i'])),
          ),
        )),
        SizedBox(height: 20),
      ]));

  Future<void> commentf(String commenttype, int commenti, String rating) async {
    await _db.runTransaction((transaction) async {
      var value = await transaction
          .get(_db.collection(contenttype[0] + '_comments').doc('c$contenti'));
      Map ratings = value.data()[commenttype];
      ratings = ratings[commenti];
      if (rating != "neutrals") {
        var opp = (rating == 'likes') ? 'dislikes' : 'likes';
        updateList(ratings[rating], user.id);
        ratings[opp].remove(user.id);
      } else {
        ratings['likes'].remove(user.id);
        ratings['dislikes'].remove(user.id);
      }
      transaction.set(
          value.reference, {commenttype: ratings}, SetOptions(merge: true));
    });
  }
}

class CommentAdder extends StatefulWidget {
  CommentAdder(this.i, this.typecontent, this.typecomment);

  final int i;
  final String typecomment;
  final String typecontent;

  @override
  _CommentAdderState createState() =>
      _CommentAdderState(i, typecontent, typecomment);
}

class _CommentAdderState extends State<CommentAdder> {
  _CommentAdderState(this.i, this.typecontent, this.typecomment);

  TextEditingController c = TextEditingController();
  int i;
  bool pressed = false;
  String typecomment;
  String typecontent;

  Future<void> savecomment(String comment) async {
    int commenti;
    var earlydata;
    String type = typecontent[0];
    try {
      await _db.runTransaction((transaction) async {
        await transaction
            .get(_db.collection('${type}_comments').doc('c$i'))
            .then((d) async {
          if (d.data() != null) {
            commenti = d.data()[typecomment].length;
            earlydata =
                d.data()[typecomment] + [getDefaultConfig(commenti, comment)];
            transaction.set(
                d.reference, {typecomment: earlydata}, SetOptions(merge: true));
          } else {
            transaction.set(
                _db.collection('${type}_comments').doc('c$i'),
                {
                  typecomment: [getDefaultConfig(0, comment)]
                },
                SetOptions(merge: true));
          }
        });
      });
    } catch (e) {
      await _db.collection('${type}_comments').doc('c$i').set({
        typecomment: [getDefaultConfig(0, comment)]
      }, SetOptions(merge: true));
    }
    try {
      await savereply();
    } catch (e) {
      await _db.collection(typecontent[0] + '_replies').doc('r$i').set({
        typecomment: [{}]
      }, SetOptions(merge: true));
    }
  }

  Future<void> savereply() async {
    await _db.runTransaction((transaction) async {
      var value = await transaction
          .get(_db.collection(typecontent[0] + '_replies').doc('r$i'));
      if (value.data() == null)
        return transaction.set(
            _db.collection(typecontent[0] + '_replies').doc('r$i'),
            {
              typecomment: [{}]
            },
            SetOptions(merge: true));
      var data = value.data()[typecomment];
      data.add({'0': {}});
      return transaction.set(
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
                  hintText: "Add your input",
                  fillColor: Colors.black,
                ),
                validator: (txt) =>
                    (txt.length == 0) ? "Add some content!" : null)),
        Container(
            child: ElevatedButton(
          child: Text("Add"),
          onPressed: () async {
            if (user.notSignedIn()) return await user.showSignInAlert(context);
            await savecomment(c.text);
            setState(() {});
          },
        ))
      ],
    );
  }
}
