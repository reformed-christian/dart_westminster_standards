import 'package:dart_westminster_standards/dart_westminster_standards.dart';

/// Basic Usage Example for Westminster Standards
/// This example shows the most common and straightforward ways to use the package
void main() async {
  print('Westminster Standards - Basic Usage Example\n');

  // Create a WestminsterStandards instance
  final standards = await WestminsterStandards.create();

  // Access the Westminster Confession
  print('=== WESTMINSTER CONFESSION ===');
  final firstChapter = standards.firstConfessionChapter;
  if (firstChapter != null) {
    print('Chapter ${firstChapter.number}: ${firstChapter.title}');
    print(
      'First section: ${firstChapter.sections.first.text.substring(0, 100)}...',
    );
  }

  // Access the Westminster Shorter Catechism
  print('\n=== WESTMINSTER SHORTER CATECHISM ===');
  final firstQuestion = standards.firstShorterCatechismQuestion;
  if (firstQuestion != null) {
    print('Q${firstQuestion.number}. ${firstQuestion.question}');
    print('A${firstQuestion.number}. ${firstQuestion.answer}');
  }

  // Access the Westminster Larger Catechism
  print('\n=== WESTMINSTER LARGER CATECHISM ===');
  final firstLargerQuestion = standards.firstLargerCatechismQuestion;
  if (firstLargerQuestion != null) {
    print('Q${firstLargerQuestion.number}. ${firstLargerQuestion.question}');
    print('A${firstLargerQuestion.number}. ${firstLargerQuestion.answer}');
  }

  // Search functionality
  print('\n=== SEARCH FUNCTIONALITY ===');
  final godQuestions = standards.shorterCatechism.exactStr('God');
  print(
    'Found ${godQuestions.length} questions containing "God" in the Shorter Catechism',
  );

  final godChapters = standards.confession.exactStr('God');
  print(
    'Found ${godChapters.length} chapters containing "God" in the Confession',
  );

  // Range access
  print('\n=== RANGE ACCESS ===');
  final questions1to5 = standards.shorterCatechism.range(1, 5);
  print('Questions 1-5: ${questions1to5.map((q) => q.number).toList()}');

  final chapters1to3 = standards.confession.range(1, 3);
  print('Chapters 1-3: ${chapters1to3.map((c) => c.number).toList()}');

  print('\nExample completed successfully!');
}
