import 'package:dart_westminster_standards/dart_westminster_standards.dart';

void main() async {
  print('=== Westminster Standards Error Handling Example ===\n');

  // 1. Handling invalid question numbers
  print('1. Handling Invalid Question Numbers:');

  final standards = await WestminsterStandards.create();

  // Try to get non-existent questions
  final invalidShorter = standards.shorterCatechism.getQuestion(999);
  final invalidLarger = standards.largerCatechism.getQuestion(999);

  print(
    '   Invalid Shorter Catechism Q999: ${invalidShorter == null ? 'null (handled correctly)' : 'error'}',
  );
  print(
    '   Invalid Larger Catechism Q999: ${invalidLarger == null ? 'null (handled correctly)' : 'error'}',
  );

  // Try to get valid questions
  final validShorter = standards.shorterCatechism.getQuestion(1);
  final validLarger = standards.largerCatechism.getQuestion(1);

  print(
    '   Valid Shorter Catechism Q1: ${validShorter != null ? 'found' : 'error'}',
  );
  print(
    '   Valid Larger Catechism Q1: ${validLarger != null ? 'found' : 'error'}',
  );
  print('');

  // 2. Handling invalid chapter numbers
  print('2. Handling Invalid Chapter Numbers:');

  final invalidChapter = standards.confession.getChapter(999);
  final validChapter = standards.confession.getChapter(1);

  print(
    '   Invalid Confession Chapter 999: ${invalidChapter == null ? 'null (handled correctly)' : 'error'}',
  );
  print(
    '   Valid Confession Chapter 1: ${validChapter != null ? 'found' : 'error'}',
  );
  print('');

  // 3. Handling empty search results
  print('3. Handling Empty Search Results:');

  // Search for non-existent terms
  final noResults = standards.shorterCatechism.exactStr('xyz123nonexistent');
  final someResults = standards.shorterCatechism.exactStr('God');

  print('   Search for non-existent term: ${noResults.length} results');
  print('   Search for "God": ${someResults.length} results');

  // Check if results are empty
  if (noResults.isEmpty) {
    print('   Empty results handled correctly');
  }
  print('');

  // 4. Handling range operations with invalid ranges
  print('4. Handling Invalid Ranges:');

  // Invalid ranges (start > end)
  final invalidRange = standards.shorterCatechism.range(10, 5);
  final validRange = standards.shorterCatechism.range(1, 5);

  print('   Invalid range (10-5): ${invalidRange.length} results');
  print('   Valid range (1-5): ${validRange.length} results');

  // Out of bounds ranges
  final outOfBoundsRange = standards.shorterCatechism.range(1000, 2000);
  print(
    '   Out of bounds range (1000-2000): ${outOfBoundsRange.length} results',
  );
  print('');

  // 5. Handling empty collections
  print('5. Handling Empty Collections:');

  // Test empty checks
  print('   Shorter Catechism is empty: ${standards.shorterCatechism.isEmpty}');
  print(
    '   Shorter Catechism is not empty: ${standards.shorterCatechism.isNotEmpty}',
  );
  print('   Confession is empty: ${standards.confession.isEmpty}');
  print('   Confession is not empty: ${standards.confession.isNotEmpty}');
  print('');

  // 6. Handling index access safely
  print('6. Safe Index Access:');

  try {
    final firstQuestion = standards.shorterCatechism[0];
    print('   First question accessed safely: ${firstQuestion.question}');
  } catch (e) {
    print('   Error accessing first question: $e');
  }

  try {
    final lastQuestion =
        standards.shorterCatechism[standards.shorterCatechism.length - 1];
    print('   Last question accessed safely: ${lastQuestion.question}');
  } catch (e) {
    print('   Error accessing last question: $e');
  }

  // This would throw an error - demonstrating bounds checking
  try {
    final outOfBounds = standards.shorterCatechism[999];
    print('   Out of bounds access: $outOfBounds');
  } catch (e) {
    print('   Out of bounds access correctly throws: ${e.runtimeType}');
  }
  print('');

  // 7. Handling proof text access
  print('7. Handling Proof Text Access:');

  final questionWithProofTexts = standards.shorterCatechism.getQuestion(1);
  if (questionWithProofTexts != null) {
    final proofTexts = questionWithProofTexts.allProofTexts;
    print('   Q1 proof texts: ${proofTexts.length}');

    if (proofTexts.isNotEmpty) {
      print('   First proof text: ${proofTexts.first.reference}');
    } else {
      print('   No proof texts found');
    }
  }
  print('');

  // 8. Handling section access
  print('8. Handling Section Access:');

  final chapter = standards.confession.getChapter(1);
  if (chapter != null) {
    final sections = chapter.sections;
    print('   Chapter 1 sections: ${sections.length}');

    if (sections.isNotEmpty) {
      final firstSection = sections.first;
      print(
        '   First section text length: ${firstSection.text.length} characters',
      );
    } else {
      print('   No sections found');
    }
  }
  print('');

  // 9. Handling bulk operations with empty results
  print('9. Handling Bulk Operations:');

  final allProofTexts = standards.allProofTexts;
  print('   Total proof texts: ${allProofTexts.length}');

  if (allProofTexts.isNotEmpty) {
    print('   First proof text: ${allProofTexts.first.reference}');
  } else {
    print('   No proof texts found in any document');
  }

  final allSections = standards.confession.allSections;
  print('   Total sections: ${allSections.length}');
  print('');

  // 10. Handling specific document loading
  print('10. Handling Specific Document Loading:');

  try {
    final confessionOnly = await WestminsterStandards.create(
      WestminsterDocument.confession,
    );
    print(
      '   Confession only loaded successfully: ${confessionOnly.confession.length} chapters',
    );
    print(
      '   Shorter Catechism not loaded: ${confessionOnly.shorterCatechism.isEmpty}',
    );
  } catch (e) {
    print('   Error loading confession only: $e');
  }
  print('');

  print('=== Error Handling Example Complete ===');
}
