// This file contains helper code that Flutter users should copy into their app
// It cannot be directly exported because it depends on flutter/services.dart

/*

/// COPY THIS CODE INTO YOUR FLUTTER APP
/// File: lib/westminster_flutter_helper.dart

import 'package:flutter/services.dart';
import 'package:dart_westminster_standards/dart_westminster_standards.dart';

/// Creates a Flutter-compatible asset loader for Westminster Standards
AssetLoader createFlutterAssetLoader({String? packageName}) {
  return (String assetPath) async {
    final paths = [
      if (packageName != null) 'packages/$packageName/$assetPath',
      assetPath,
    ];

    for (final fullPath in paths) {
      try {
        return await rootBundle.loadString(fullPath);
      } catch (e) {
        // Try next path
        continue;
      }
    }

    throw AssetLoadingException(
      'Failed to load asset using Flutter rootBundle. Tried paths:\n${paths.map((p) => '  - $p').join('\n')}',
      assetPath,
    );
  };
}

/// Convenience method to create Westminster Standards with Flutter asset loading
Future<WestminsterStandards> createWestminsterStandardsForFlutter({
  WestminsterDocument documents = WestminsterDocument.all,
  String packageName = 'dart_westminster_standards',
}) async {
  final assetLoader = createFlutterAssetLoader(packageName: packageName);
  return await WestminsterStandards.createWithLoader(assetLoader, documents);
}

/// Quick test function to verify Flutter asset loading
Future<void> testFlutterAssetLoading() async {
  try {
    final standards = await createWestminsterStandardsForFlutter();
    final q1 = standards.shorterCatechism.getQuestion(1);
    print('✅ Flutter asset loading works!');
    print('Q1: ${q1?.question}');
  } catch (e) {
    print('❌ Flutter asset loading failed: $e');
  }
}

*/
