import 'package:westminster_standards/westminster_standards.dart';

/// Example demonstrating enhanced access to Westminster Standards
/// This shows how to use the WestminsterStandards object for convenient access
void main() async {
  print('=== Westminster Standards Enhanced Access Example ===\n');

  // Create a WestminsterStandards instance with all documents
  final standards = await WestminsterStandards.create();

  // Example 1: Enhanced access to individual documents
  print('1. Enhanced Access to Individual Documents:');
  print('Confession has ${standards.confession.length} chapters');
  print('Shorter Catechism has ${standards.shorterCatechism.length} questions');
  print('Larger Catechism has ${standards.largerCatechism.length} questions\n');

  // Example 2: Text-only access (excluding scripture references)
  print('2. Text-Only Access (excluding scripture references):');
  print('Confession text-only (first 300 characters):');
  print(standards.confessionTextOnly.substring(0, 300) + '...\n');

  print('Shorter Catechism text-only (first 300 characters):');
  print(standards.shorterCatechismTextOnly.substring(0, 300) + '...\n');

  print('Larger Catechism text-only (first 300 characters):');
  print(standards.largerCatechismTextOnly.substring(0, 300) + '...\n');

  // Example 3: Range-based text-only access
  print('3. Range-Based Text-Only Access:');
  print('Confession chapters 1-2 text-only:');
  print(standards.getConfessionRangeTextOnly(1, 2).substring(0, 400) + '...\n');

  print('Shorter Catechism questions 1-3 text-only:');
  print(standards.getShorterCatechismRangeTextOnly(1, 3) + '\n');

  print('Larger Catechism questions 1-2 text-only:');
  print(standards.getLargerCatechismRangeTextOnly(1, 2) + '\n');

  // Example 4: Specific numbers text-only access
  print('4. Specific Numbers Text-Only Access:');
  print('Confession chapters 1, 3, 5 text-only:');
  print(
    standards.getConfessionByNumbersTextOnly([1, 3, 5]).substring(0, 400) +
        '...\n',
  );

  print('Shorter Catechism questions 1, 3, 5 text-only:');
  print(standards.getShorterCatechismByNumbersTextOnly([1, 3, 5]) + '\n');

  // Example 5: All documents text-only
  print('5. All Documents Text-Only (first 500 characters):');
  print(standards.allTextOnly.substring(0, 500) + '...\n');

  // Example 6: Enhanced access through document objects
  print('6. Enhanced Access Through Document Objects:');
  print('Confession object text-only (first 300 characters):');
  print(standards.confession.textOnly.substring(0, 300) + '...\n');

  print('Shorter Catechism object text-only (first 300 characters):');
  print(standards.shorterCatechism.textOnly.substring(0, 300) + '...\n');

  print('Larger Catechism object text-only (first 300 characters):');
  print(standards.largerCatechism.textOnly.substring(0, 300) + '...\n');

  // Example 7: Range-based text-only through document objects
  print('7. Range-Based Text-Only Through Document Objects:');
  print('Confession chapters 1-2 text-only:');
  print(
    standards.confession.getRangeTextOnly(1, 2).substring(0, 400) + '...\n',
  );

  print('Shorter Catechism questions 1-3 text-only:');
  print(standards.shorterCatechism.getRangeTextOnly(1, 3) + '\n');

  // Example 8: Specific numbers text-only through document objects
  print('8. Specific Numbers Text-Only Through Document Objects:');
  print('Confession chapters 1, 3, 5 text-only:');
  print(
    standards.confession.getByNumbersTextOnly([1, 3, 5]).substring(0, 400) +
        '...\n',
  );

  print('Shorter Catechism questions 1, 3, 5 text-only:');
  print(standards.shorterCatechism.getByNumbersTextOnly([1, 3, 5]) + '\n');

  // Example 9: Search functionality
  print('9. Search Functionality:');
  final searchResults = standards.searchAll('grace');
  print('Found ${searchResults.length} results for "grace"');
  for (int i = 0; i < searchResults.take(3).length; i++) {
    final result = searchResults[i];
    print(
      '  ${i + 1}. ${result.documentType} #${result.number}: ${result.title}',
    );
  }
  print('');

  // Example 10: Individual item access
  print('10. Individual Item Access:');
  final firstQuestion = standards.getShorterCatechismQuestion(1);
  if (firstQuestion != null) {
    print('First Shorter Catechism Question:');
    print('Q${firstQuestion.number}. ${firstQuestion.question}');
    print('A${firstQuestion.number}. ${firstQuestion.answer}');
  }

  final firstChapter = standards.getConfessionChapter(1);
  if (firstChapter != null) {
    print('\nFirst Confession Chapter:');
    print('Chapter ${firstChapter.number}. ${firstChapter.title}');
    print(
      'First section: ${firstChapter.sections.first.text.substring(0, 100)}...',
    );
  }
  print('');

  // Example 11: Proof texts access
  print('11. Proof Texts Access:');
  print(
    'Total proof texts in Shorter Catechism: ${standards.allShorterCatechismProofTexts.length}',
  );
  print(
    'Total proof texts in Larger Catechism: ${standards.allLargerCatechismProofTexts.length}',
  );
  print(
    'Total proof texts in Confession: ${standards.allConfessionProofTexts.length}',
  );
  print(
    'Total proof texts across all documents: ${standards.allProofTexts.length}',
  );
}
