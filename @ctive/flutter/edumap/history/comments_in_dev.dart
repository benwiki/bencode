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
  Comments(this.nodei, this.contenti, this.contenttype, this.k, this.lim,
      [this.commenttype, this.commenti])
      : super(key: k);

  final int commenti;
  final String commenttype;
  int contenti;
  String contenttype;
  GlobalKey<CommentsState> k;
  int lim;
  int nodei;

  @override
  CommentsState createState() => CommentsState();
}

class CommentsState extends State<Comments> {
  GlobalKey<ScaffoldState> scaffold = GlobalKey<ScaffoldState>();
  int l, l2;
  String sortRule = SortRule.quality.str;
  bool sorted = false, isReply;
  String prefix, postfix;

  @override
  void initState() {
    super.initState();
    isReply = widget.commenti != null && widget.commenttype != null;
    this.prefix = isReply ? 'r' : 'c';
    this.postfix = isReply ? '_replies' : '_comments';
  }

  Future<void> commentf(String commenttype, int commenti, String rating) async {
    await _db.runTransaction((transaction) {
      return transaction
          .get(_db
              .collection(widget.contenttype[0] + postfix)
              .doc('$prefix${widget.contenti}'))
          .then((value) {
        Map arr = value.data()[commenttype];
        arr = arr[isReply ? widget.commenti : commenti];
        if (isReply) arr = arr['$commenti'];
        if (rating != "neutrals") {
          var opp = (rating == 'likes') ? 'dislikes' : 'likes';
          updateList(arr[rating], user.id);
          arr[opp].remove(user.id);
        } else {
          arr['likes'].remove(user.id);
          arr['dislikes'].remove(user.id);
        }
        transaction.set(
            value.reference, {commenttype: arr}, SetOptions(merge: true));
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    if (isReply)
      return Scaffold(appBar: buildAppBar(context), body: buildBody(context));
    return MaterialApp(
        home: DefaultTabController(
            length: 3,
            child: Scaffold(
                key: scaffold,
                resizeToAvoidBottomInset: false,
                appBar: buildAppBar(context),
                body: buildBody(context))));
  }

  buildAppBar(context) => AppBar(
      title: Text(isReply ? "Replies" : "Responses"),
      leading: (isReply)
          ? IconButton(
              icon: Icon(Icons.arrow_back),
              onPressed: () => Navigator.pop(context),
            )
          : null,
      actions: [
        Row(children: [
          getSortRuleSelector((rule) => setState(() {
                sortRule = rule;
              })),
          SizedBox(width: 5)
        ]),
        IconButton(icon: Icon(Icons.sync), onPressed: () => setState(() {})),
      ],
      bottom: (isReply)
          ? TabBar(isScrollable: true, tabs: <Widget>[
              Tab(text: 'Other perspectives'),
              Tab(text: 'Content feedback'),
              Tab(text: 'Discussions'),
            ])
          : null);

  buildBody(context) => StreamBuilder(
      stream: _db.collection(widget.contenttype[0] + '_comments').snapshots(),
      builder: (context, snapshot) {
        if (!snapshot.hasData)
          return (isReply)
              ? CenteredLoadingSign()
              : TabBarView(
                  children: List.generate(3, (_) => CenteredLoadingSign()));

        var snap = snapshot.data.docs.firstWhere(
            (doc) => doc.id == '$prefix${widget.contenti}',
            orElse: () => null);
        Map temp = {'feedback': [], 'discussion': []};
        if (snap != null) {
          if (isReply) {
            snap = snap.data();
          } else {
            initTemp(context, snap, temp, 'feedback');
            initTemp(context, snap, temp, 'discussion');
          }
        }
        if (isReply) {
          List rkeys;
          if (snap != null && snap[widget.commenttype] != null) {
            Map commentsnap = snap[widget.commenttype][widget.commenti];
            l = commentsnap.length - 1;
            rkeys = commentsnap.keys
                .where((e) {
                  return (commentsnap[e].length != 0);
                })
                .map((f) => int.parse(f))
                .toList();
            rkeys = rkeys.reversed.toList();
            if (rkeys.length != 0 && !sorted) {
              sorted = true;
              if (sortRule == SortRule.quality.str) {
                rkeys.sort((j, i) => convert(commentsnap['$i'])
                    .compareTo(convert(commentsnap['$j'])));
              } else if (sortRule == SortRule.latest.str) {}
            }
          }
          return SingleChildScrollView(
              child: Column(children: [
            ReplyAdder(widget.contenti, widget.commenti, widget.contenttype,
                widget.commenttype),
            if (snap != null && snap[widget.commenttype] != null)
              Column(
                  children: List.generate(
                      rkeys.length,
                      (i) => getCard(rkeys[i],
                          snap[widget.commenttype][widget.commenti], i)))
          ]));
        }

        return TabBarView(children: [
          RefShow(widget.contenti, widget.contenttype, widget.nodei, widget.k,
              scaffold, widget.lim,
              k2: GlobalKey<RefShowState>()),
          buildFeedbackScrollView(
              context, snap, temp, 'Good feedback?', 'feedback'),
          buildFeedbackScrollView(
              context, snap, temp, 'Helpful?', 'discussion'),
        ]);
      });

  initTemp(context, snap, temp, type) {
    if (snap.data()[type] != null) {
      l = snap.data()[type].length - 1;
      temp[type] = snap
          .data()[type]
          .where((e) => e.length != 0)
          .toList()
          .reversed
          .toList();
      if (!sorted) {
        if (sortRule == SortRule.quality.str) {
          temp[type].sort((c2, c1) {
            return convert(c1).compareTo(convert(c2));
          });
        } else if (sortRule == SortRule.latest.str) {}
      }
    }
  }

  buildFeedbackScrollView(context, snap, temp, message, type) =>
      SingleChildScrollView(
          child: Column(children: [
        CommentAdder(widget.contenti, widget.contenttype, type),
        if (snap != null && temp[type] != null)
          Column(
              children: List.generate(
                  temp[type].length, (i) => getCard(temp, type, message, i)))
      ]));

  getCard(temp, type, message, i) => Card(
          child: Row(children: [
        SizedBox(width: 20),
        buildFeedbackContainer(context, i, temp[type], message, type),
        if (temp[type][i]['uid'] == user.id)
          Container(
              width: 25,
              child: GestureDetector(
                  child: Icon(Icons.delete),
                  onTap: () {
                    Deleter d = Deleter(context);
                    d.deletecomment(
                      widget.contenttype,
                      type,
                      widget.contenti,
                      temp[type][i]['i'],
                    );
                  }))
      ]));

  buildFeedbackContainer(context, i, temp, message, type) => Container(
      width: (temp[i]['uid'] == user.id)
          ? MediaQuery.of(context).size.width - 55
          : MediaQuery.of(context).size.width - 30,
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        SizedBox(height: 15),
        Row(children: [
          if (temp[i]['imgurl'] != null)
            Container(
                width: 32,
                height: 32,
                decoration: BoxDecoration(shape: BoxShape.circle),
                child: ClipRRect(
                    borderRadius: BorderRadius.circular(100.0),
                    child: Image.network(
                      temp[i]['imgurl'],
                      fit: BoxFit.cover,
                    ))),
          SizedBox(width: 5),
          Text(temp[i]['name'] + ": ", style: TextStyle(fontSize: 15))
        ]),
        SizedBox(height: 3),
        ConstrainedBox(
            constraints: BoxConstraints(
                maxWidth: MediaQuery.of(context).size.width - 30),
            child: Text(temp[i]['text'],
                style: TextStyle(fontSize: 17), maxLines: 30)),
        SizedBox(height: 10),
        Row(children: [
          Text(message, style: TextStyle(fontSize: 15)),
          RatingIcons(
            temp[i],
            (String likeordislike) async =>
                commentf(type, temp[i]['i'], likeordislike),
            temp[i]['uid'],
            k: ValueKey(temp[i]['i']),
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
                builder: (context) => Replies(
                    widget.contenttype, widget.contenti, type, temp[i]['i'])),
          ),
        )),
        SizedBox(height: 20),
      ]));
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
      await _db.runTransaction((transaction) {
        return transaction
            .get(_db.collection(typecontent[0] + '_replies').doc('r$i'))
            .then((value) async {
          if (value.data() != null) {
            var initial = value.data()[typecomment];
            initial.add({'0': {}});
            return transaction.set(value.reference, {typecomment: initial},
                SetOptions(merge: true));
          } else {
            transaction.set(
                _db.collection(typecontent[0] + '_replies').doc('r$i'),
                {
                  typecomment: [{}]
                },
                SetOptions(merge: true));
          }
        });
      });
    } catch (e) {
      await _db.collection(typecontent[0] + '_replies').doc('r$i').set({
        typecomment: [{}]
      }, SetOptions(merge: true));
    }
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
