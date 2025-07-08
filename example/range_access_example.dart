import 'package:dart_westminster_standards/dart_westminster_standards.dart';

/// Example demonstrating range-based access to Westminster Standards
///
/// This example shows how to:
/// - Get ranges of catechism questions (e.g., questions 1-10)
/// - Get ranges of confession chapters (e.g., chapters 1-5)
/// - Get specific items by numbers
/// - Use both synchronous and lazy loading approaches
void main() async {
  print('=== Westminster Standards Range Access Example ===\n');

  // Example 1: Get a range of Shorter Catechism questions (1-5)
  print('1. Shorter Catechism Questions 1-5:');
  final shorterRange = getWestminsterShorterCatechismRange(1, 5);
  for (final question in shorterRange) {
    print('   Q${question.number}: ${question.question}');
    print('   A: ${question.answer}');
    print('   Proof texts: ${question.allProofTexts.length}');
    print('');
  }

  // Example 2: Get a range of Larger Catechism questions (1-3)
  print('2. Larger Catechism Questions 1-3:');
  final largerRange = getWestminsterLargerCatechismRange(1, 3);
  for (final question in largerRange) {
    print('   Q${question.number}: ${question.question}');
    print('   A: ${question.answer}');
    print('   Proof texts: ${question.allProofTexts.length}');
    print('');
  }

  // Example 3: Get a range of Confession chapters (1-3)
  print('3. Confession Chapters 1-3:');
  final confessionRange = getWestminsterConfessionRange(1, 3);
  for (final chapter in confessionRange) {
    print('   Chapter ${chapter.number}: ${chapter.title}');
    print('   Sections: ${chapter.sections.length}');
    print(
      '   Total proof texts: ${chapter.sections.fold(0, (sum, section) => sum + section.allProofTexts.length)}',
    );
    print('');
  }

  // Example 4: Get specific questions by numbers
  print('4. Specific Shorter Catechism Questions (1, 3, 5):');
  final specificQuestions = getWestminsterShorterCatechismByNumbers([1, 3, 5]);
  for (final question in specificQuestions) {
    print('   Q${question.number}: ${question.question}');
  }
  print('');

  // Example 5: Get specific confession chapters by numbers
  print('5. Specific Confession Chapters (1, 5, 10):');
  final specificChapters = getWestminsterConfessionByNumbers([1, 5, 10]);
  for (final chapter in specificChapters) {
    print('   Chapter ${chapter.number}: ${chapter.title}');
  }
  print('');

  // Example 6: Using lazy loading for ranges
  print('6. Lazy Loading - Shorter Catechism Questions 10-12:');
  final lazyRange = await loadWestminsterShorterCatechismRangeLazy(10, 12);
  for (final question in lazyRange) {
    print('   Q${question.number}: ${question.question}');
  }
  print('');

  // Example 7: Using the enhanced WestminsterStandards object
  print(
    '7. Using WestminsterStandards Object - Shorter Catechism Questions 15-17:',
  );
  final standards = await WestminsterStandards.create();
  final enhancedRange = standards.shorterCatechism.range(15, 17);
  for (final question in enhancedRange) {
    print('   Q${question.number}: ${question.question}');
  }
  print('');

  // Example 8: Using the enhanced WestminsterStandards object for confession
  print('8. Using WestminsterStandards Object - Confession Chapters 4-6:');
  final enhancedConfessionRange = standards.confession.range(4, 6);
  for (final chapter in enhancedConfessionRange) {
    print('   Chapter ${chapter.number}: ${chapter.title}');
  }
  print('');

  // Example 9: Error handling - invalid ranges
  print('9. Error Handling - Invalid Range:');
  final invalidRange = getWestminsterShorterCatechismRange(999, 1000);
  print(
    '   Invalid range result: ${invalidRange.isEmpty ? "Empty list (as expected)" : "Unexpected data"}',
  );
  print('');

  // Example 10: Performance comparison
  print('10. Performance - Getting all questions vs range:');
  final allQuestions = getWestminsterShorterCatechism();
  final rangeQuestions = getWestminsterShorterCatechismRange(1, 10);
  print('   All questions: ${allQuestions.length}');
  print('   Range questions (1-10): ${rangeQuestions.length}');
  print('   Range is more efficient for specific needs!');
}
