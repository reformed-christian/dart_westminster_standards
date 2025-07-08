import 'package:dart_westminster_standards/dart_westminster_standards.dart';
import 'dart:async';

void main() async {
  print('=== Westminster Standards Performance Example ===\n');

  // 1. Loading performance
  print('1. Loading Performance:');

  final stopwatch = Stopwatch();

  // Time loading all documents
  stopwatch.start();
  final standards = await WestminsterStandards.create();
  stopwatch.stop();

  print('   Time to load all documents: ${stopwatch.elapsedMilliseconds}ms');
  print('   Total items loaded:');
  print('     Confession chapters: ${standards.confession.length}');
  print(
    '     Shorter Catechism questions: ${standards.shorterCatechism.length}',
  );
  print('     Larger Catechism questions: ${standards.largerCatechism.length}');
  print('');

  // 2. Search performance
  print('2. Search Performance:');

  // Time different search operations
  final searchTerms = ['God', 'salvation', 'grace', 'faith', 'church'];

  for (final term in searchTerms) {
    stopwatch.reset();
    stopwatch.start();

    final confessionResults = standards.confession.exactStr(term);
    final shorterResults = standards.shorterCatechism.exactStr(term);
    final largerResults = standards.largerCatechism.exactStr(term);

    stopwatch.stop();

    print('   Search for "$term": ${stopwatch.elapsedMicroseconds}μs');
    print(
      '     Results: ${confessionResults.length + shorterResults.length + largerResults.length}',
    );
  }
  print('');

  // 3. Bulk operations performance
  print('3. Bulk Operations Performance:');

  // Time getting all proof texts
  stopwatch.reset();
  stopwatch.start();
  final allProofTexts = standards.allProofTexts;
  stopwatch.stop();

  print('   Getting all proof texts: ${stopwatch.elapsedMicroseconds}μs');
  print('   Total proof texts: ${allProofTexts.length}');

  // Time getting all sections
  stopwatch.reset();
  stopwatch.start();
  final allSections = standards.confession.allSections;
  stopwatch.stop();

  print('   Getting all sections: ${stopwatch.elapsedMicroseconds}μs');
  print('   Total sections: ${allSections.length}');
}
