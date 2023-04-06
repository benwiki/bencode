import 'package:edumap/firebase_options.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/material.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:google_sign_in/google_sign_in.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform);
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Login Test',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const MyHomePage(title: 'Login Test'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  final FirebaseAuth _auth = FirebaseAuth.instance;

  bool signedIn = false;
  UserCredential? userCred;

  @override
  Widget build(BuildContext context) {
    User? user = _auth.currentUser;
    return Column(children: [
      SizedBox(height: 200),
      Container(
          width: 400,
          height: 200,
          child: Text(
              (signedIn)
                  ? "Signed in. User: ${user?.displayName}, ${user?.email}"
                  : "Not signed in.",
              style: TextStyle(
                  decoration: TextDecoration.none,
                  fontSize: 25,
                  color: Colors.blue))),
      MaterialButton(
          color: Colors.amber,
          child: Text("Sign In"),
          onPressed: () => signInWithGoogle(context))
    ]);
  }

  Future<void> signInWithGoogle(BuildContext context) async {
    final GoogleSignInAccount? googleUser = await GoogleSignIn().signIn();
    if (googleUser == null) throw Error();
    final googleAuth = await googleUser.authentication;
    UserCredential userCred =
        await _auth.signInWithCredential(GoogleAuthProvider.credential(
      accessToken: googleAuth.accessToken,
      idToken: googleAuth.idToken,
    ));
    setState(() {
      this.userCred = userCred;
      this.signedIn = true;
    });
  }
}
