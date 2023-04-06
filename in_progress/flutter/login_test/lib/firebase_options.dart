// File generated by FlutterFire CLI.
// ignore_for_file: lines_longer_than_80_chars, avoid_classes_with_only_static_members
import 'package:firebase_core/firebase_core.dart' show FirebaseOptions;
import 'package:flutter/foundation.dart'
    show defaultTargetPlatform, kIsWeb, TargetPlatform;

/// Default [FirebaseOptions] for use with your Firebase apps.
///
/// Example:
/// ```dart
/// import 'firebase_options.dart';
/// // ...
/// await Firebase.initializeApp(
///   options: DefaultFirebaseOptions.currentPlatform,
/// );
/// ```
class DefaultFirebaseOptions {
  static FirebaseOptions get currentPlatform {
    if (kIsWeb) {
      throw UnsupportedError(
        'DefaultFirebaseOptions have not been configured for web - '
        'you can reconfigure this by running the FlutterFire CLI again.',
      );
    }
    switch (defaultTargetPlatform) {
      case TargetPlatform.android:
        return android;
      case TargetPlatform.iOS:
        return ios;
      case TargetPlatform.macOS:
        throw UnsupportedError(
          'DefaultFirebaseOptions have not been configured for macos - '
          'you can reconfigure this by running the FlutterFire CLI again.',
        );
      case TargetPlatform.windows:
        throw UnsupportedError(
          'DefaultFirebaseOptions have not been configured for windows - '
          'you can reconfigure this by running the FlutterFire CLI again.',
        );
      case TargetPlatform.linux:
        throw UnsupportedError(
          'DefaultFirebaseOptions have not been configured for linux - '
          'you can reconfigure this by running the FlutterFire CLI again.',
        );
      default:
        throw UnsupportedError(
          'DefaultFirebaseOptions are not supported for this platform.',
        );
    }
  }

  static const FirebaseOptions android = FirebaseOptions(
    apiKey: 'AIzaSyCpM9OpumfGc9KkUhDnjLWVoxfwuTUd768',
    appId: '1:52987743700:android:def2641f6a1a66709e5a41',
    messagingSenderId: '52987743700',
    projectId: 'infomap-1dbef',
    databaseURL: 'https://infomap-1dbef.firebaseio.com',
    storageBucket: 'infomap-1dbef.appspot.com',
  );

  static const FirebaseOptions ios = FirebaseOptions(
    apiKey: 'AIzaSyAYr3OPUIVfp4brLX8qVNGF-fJpDE9O5eM',
    appId: '1:52987743700:ios:2af14227900606809e5a41',
    messagingSenderId: '52987743700',
    projectId: 'infomap-1dbef',
    databaseURL: 'https://infomap-1dbef.firebaseio.com',
    storageBucket: 'infomap-1dbef.appspot.com',
    androidClientId:
        '52987743700-0p020290c0qoqth4709m57o60t0n7kq7.apps.googleusercontent.com',
    iosClientId:
        '52987743700-um7dp9ej46q205dko5m60nhk4q3fmdup.apps.googleusercontent.com',
    iosBundleId: 'com.example.edumap',
  );
}
